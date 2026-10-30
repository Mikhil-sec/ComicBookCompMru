"""Small driver for Meta's Muse Image API (muse-image-1.0).

Usage (from the repo root):
    .venv/Scripts/python tools/muse.py check
    .venv/Scripts/python tools/muse.py gen  "prompt" -o out/test.png [--size 1024x1536] [--n 1]
    .venv/Scripts/python tools/muse.py edit "prompt" -r ref1.png -r ref2.png -o out/panel.png

Meta has no hard spend cap, so this script enforces one: HARD_CAP_USD is a
constant, and .env can only lower it. The cost of each call is reserved in
muse_ledger.json BEFORE the request is sent and is never refunded, so a crash,
timeout or safety-filtered image can only make the ledger overestimate spending.
Every call is also logged with its prompt in prompts_log.jsonl.
"""
import argparse
import base64
import json
import mimetypes
import os
import sys
import threading
import time
from datetime import datetime
from pathlib import Path

import httpx
from dotenv import load_dotenv
from PIL import Image

ROOT = Path(__file__).resolve().parent.parent
BASE_URL = "https://api.meta.ai/v1"
MODEL = "muse-image-1.0"
PRICE_PER_IMAGE = 0.01
HARD_CAP_USD = 5.00  # never exceeded; .env may only set a lower budget
MAX_N_PER_CALL = 4
LEDGER = ROOT / "muse_ledger.json"
PROMPT_LOG = ROOT / "prompts_log.jsonl"

load_dotenv(ROOT / ".env")
BUDGET = min(HARD_CAP_USD, float(os.environ.get("MUSE_BUDGET_USD", HARD_CAP_USD)))


def api_key():
    key = os.environ.get("MODEL_API_KEY", "")
    if not key or key == "paste_your_key_here":
        sys.exit("MODEL_API_KEY missing: put it in .env (see .env.example).")
    return key


def client():
    return httpx.Client(
        base_url=BASE_URL,
        headers={"Authorization": f"Bearer {api_key()}"},
        timeout=300,
    )


def spent():
    if not LEDGER.exists():
        return 0.0
    try:
        return float(json.loads(LEDGER.read_text())["spent_usd"])
    except (ValueError, KeyError) as e:
        sys.exit(f"Ledger {LEDGER.name} is unreadable ({e}); refusing to spend. Fix it by hand.")


def reserve(n):
    """Check the cap and record the cost before the request goes out.

    Holds an exclusive lock file so parallel runs can't both read the same
    balance and under-count.
    """
    if not 1 <= n <= MAX_N_PER_CALL:
        sys.exit(f"--n must be between 1 and {MAX_N_PER_CALL}.")
    lock = LEDGER.with_suffix(".lock")
    for _ in range(100):
        try:
            fd = os.open(lock, os.O_CREAT | os.O_EXCL | os.O_WRONLY)
            break
        except FileExistsError:
            time.sleep(0.1)
    else:
        sys.exit(f"Ledger lock {lock.name} stuck; delete it if no other muse.py is running.")
    try:
        total = round(spent() + n * PRICE_PER_IMAGE, 2)
        if total > BUDGET + 1e-9:
            sys.exit(f"Budget stop: spent ${spent():.2f}, this call needs ${n * PRICE_PER_IMAGE:.2f}, cap is ${BUDGET:.2f}.")
        LEDGER.write_text(json.dumps({"spent_usd": total, "updated": datetime.now().isoformat()}, indent=2))
        return total
    finally:
        os.close(fd)
        os.remove(lock)


def data_url(path):
    mime = mimetypes.guess_type(path)[0] or "image/png"
    return f"data:{mime};base64,{base64.b64encode(Path(path).read_bytes()).decode()}"


def save(resp_json, out, kind, prompt, refs, total):
    out = Path(out).resolve()
    out.parent.mkdir(parents=True, exist_ok=True)
    saved = []
    for i, item in enumerate(resp_json.get("data", [])):
        path = out if i == 0 else out.with_stem(f"{out.stem}_{i}")
        path.write_bytes(base64.b64decode(item["b64_json"]))
        with Image.open(path) as im:
            saved.append({"file": str(path.relative_to(ROOT)), "px": f"{im.width}x{im.height}"})
    with PROMPT_LOG.open("a", encoding="utf-8") as f:
        f.write(json.dumps({
            "time": datetime.now().isoformat(), "kind": kind, "model": MODEL,
            "prompt": prompt, "refs": refs, "outputs": saved,
        }, ensure_ascii=False) + "\n")
    print(json.dumps({"saved": saved, "spent_usd": total, "budget_usd": BUDGET}, indent=2))


MIN_INTERVAL_S = 1.0  # spacing between request starts; Meta's limit is 150 req/min
RETRY_STATUSES = {429, 503}  # rate-limited / retryable backend error: not billed by Meta
_throttle = threading.Lock()
_last_start = 0.0


def post(path, body):
    """POST with throttling. Retries only on 429/503; never on timeouts, since a
    timed-out request may already have been generated and billed."""
    global _last_start
    for attempt in range(4):
        with _throttle:
            wait = _last_start + MIN_INTERVAL_S - time.monotonic()
            if wait > 0:
                time.sleep(wait)
            _last_start = time.monotonic()
        with client() as c:
            r = c.post(path, json=body)
        if r.status_code == 200:
            return r.json()
        if r.status_code in RETRY_STATUSES and attempt < 3:
            try:
                delay = float(r.headers.get("retry-after", ""))
            except ValueError:
                delay = 5 * 2 ** attempt
            print(f"HTTP {r.status_code}, retrying in {delay:.0f}s")
            time.sleep(delay)
            continue
        sys.exit(f"HTTP {r.status_code}: {r.text[:800]}")


def main():
    p = argparse.ArgumentParser()
    sub = p.add_subparsers(dest="cmd", required=True)
    sub.add_parser("check", help="verify the API key (free)")
    for name in ("gen", "edit"):
        s = sub.add_parser(name)
        s.add_argument("prompt")
        s.add_argument("-o", "--out", required=True)
        s.add_argument("--size", default="1024x1536", help="WxH, sets aspect ratio")
        s.add_argument("--n", type=int, default=1)
        if name == "edit":
            s.add_argument("-r", "--ref", action="append", required=True, help="reference image (repeatable, max 10)")
    a = p.parse_args()

    if a.cmd == "check":
        with client() as c:
            r = c.get("/models")
        print(f"HTTP {r.status_code}")
        print(r.text[:1500])
        print(f"Local ledger: spent ${spent():.2f} of ${BUDGET:.2f} budget")
        return

    body = {"model": MODEL, "prompt": a.prompt, "n": a.n, "size": a.size, "output_format": "png"}
    if a.cmd == "gen":
        path = "/images/generations"
    else:
        if len(a.ref) > 10:
            sys.exit("At most 10 reference images.")
        body["images"] = [{"image_url": data_url(r)} for r in a.ref]
        path = "/images/edits"
    total = reserve(a.n)  # last step before the paid request
    save(post(path, body), a.out, a.cmd, a.prompt, a.ref if a.cmd == "edit" else [], total)


if __name__ == "__main__":
    main()
