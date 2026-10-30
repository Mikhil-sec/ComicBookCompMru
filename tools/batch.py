"""Run a JSON file of Muse jobs in dependency order.

    .venv/Scripts/python tools/batch.py story/jobs_sheets.json [--only id1,id2] [--dry]

Job file:
    {"vars": {"STYLE": "...", ...},
     "jobs": [{"id": "wei_21", "kind": "edit", "refs": ["assets/sheets/wei_14.png"],
               "out": "assets/sheets/wei_21.png", "size": "1536x1024", "prompt": "... {STYLE}"}]}

A job runs once every ref file exists, so a job whose ref is another job's output
waits for that job. Jobs whose output already exists are skipped, which makes
re-running after a failure cheap. Spending still goes through muse.reserve(), so
the hard cap and ledger lock apply.
"""
import argparse
import json
import sys
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import muse  # noqa: E402

ROOT = muse.ROOT
WORKERS = 3


def fill(text, variables):
    for k, v in variables.items():
        text = text.replace("{" + k + "}", v)
    return text


def run(job, variables):
    prompt = fill(job["prompt"], variables)
    body = {"model": muse.MODEL, "prompt": prompt, "n": 1,
            "size": job.get("size", "1536x1024"), "output_format": "png"}
    refs = job.get("refs", [])
    if job["kind"] == "edit":
        body["images"] = [{"image_url": muse.data_url(ROOT / r)} for r in refs]
        path = "/images/edits"
    else:
        path = "/images/generations"
    total = muse.reserve(1)
    muse.save(muse.post(path, body), ROOT / job["out"], job["kind"], prompt, refs, total)
    return job["id"]


def main():
    p = argparse.ArgumentParser()
    p.add_argument("jobfile")
    p.add_argument("--only", help="comma-separated job ids")
    p.add_argument("--dry", action="store_true", help="show what would run, spend nothing")
    a = p.parse_args()

    spec = json.loads((ROOT / a.jobfile).read_text(encoding="utf-8"))
    variables = spec.get("vars", {})
    jobs = spec["jobs"]
    if a.only:
        wanted = set(a.only.split(","))
        jobs = [j for j in jobs if j["id"] in wanted]
    pending = [j for j in jobs if not (ROOT / j["out"]).exists()]
    print(f"{len(pending)} job(s) to run, ~${len(pending) * muse.PRICE_PER_IMAGE:.2f}; "
          f"ledger ${muse.spent():.2f} of ${muse.BUDGET:.2f}")
    if a.dry:
        for j in pending:
            print(f"  {j['id']}: {j['kind']} refs={j.get('refs', [])} -> {j['out']}")
        return

    failed = set()
    with ThreadPoolExecutor(WORKERS) as pool:
        while pending:
            ready = [j for j in pending
                     if all((ROOT / r).exists() for r in j.get("refs", []))]
            if not ready:
                blocked = [j["id"] for j in pending]
                print(f"Stopped: waiting on missing refs or failed jobs: {blocked}")
                break
            futures = {pool.submit(run, j, variables): j for j in ready}
            for f in as_completed(futures):
                j = futures[f]
                try:
                    print(f"done: {f.result()}")
                except SystemExit as e:  # muse.py exits on budget stop / HTTP errors
                    print(f"FAILED {j['id']}: {e}")
                    failed.add(j["id"])
            pending = [j for j in pending
                       if not (ROOT / j["out"]).exists() and j["id"] not in failed]
    print(f"ledger now ${muse.spent():.2f}; failed: {sorted(failed) or 'none'}")


if __name__ == "__main__":
    main()
