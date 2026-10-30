"""Writes Board 3 lettering into story/pages.json."""
import json
from pathlib import Path

p = Path(__file__).resolve().parent / "pages.json"
d = json.loads(p.read_text(encoding="utf-8"))
img = lambda i: f"assets/panels/b3/p{i}.png"
d["b3"] = {"panels": [
    {"image": img(1), "text": [
        {"type": "caption", "text": "2008. The children had grown up and moved to town. Uncle Lam was gone. The street was quieter.",
         "at": [0.01, 0.04], "max_w": 0.19, "size": 30}]},
    {"image": img(2), "text": [
        {"type": "bubble", "text": "Your mother is very ill. You should come home.", "at": [0.5, 0.1], "tail": [0.51, 0.43], "max_w": 0.34, "size": 32},
        {"type": "bubble", "text": "...Home.", "at": [0.86, 0.36], "tail": [0.68, 0.4], "max_w": 0.2, "size": 32}]},
    {"image": img(3), "text": [
        {"type": "caption", "text": "Meizhou, China. Thirty-six years later, I was the stranger here.", "at": [0.02, 0.03], "max_w": 0.46, "size": 30}]},
    {"image": img(4), "text": [
        {"type": "bubble", "text": "You speak like an islander now.", "at": [0.2, 0.1], "tail": [0.27, 0.4], "max_w": 0.3, "size": 31},
        {"type": "bubble", "text": "I don't know where I belong anymore, Ma.", "at": [0.8, 0.1], "tail": [0.64, 0.24], "max_w": 0.3, "size": 31},
        {"type": "bubble", "text": "Home is where your children laugh. Go back to them.", "at": [0.2, 0.87], "tail": [0.27, 0.62], "max_w": 0.32, "size": 31}]},
    {"image": img(5), "text": [
        {"type": "caption", "text": "Somewhere over the ocean, I finally understood what she meant.", "at": [0.02, 0.03], "max_w": 0.32, "size": 30}]},
    {"image": img(6), "text": [
        {"type": "caption", "text": "Take care of this street, and it will take care of you.", "at": [0.01, 0.04], "max_w": 0.2, "size": 30},
        {"type": "bubble", "text": "We kept the lights on.", "at": [0.62, 0.92], "tail": [0.488, 0.76], "max_w": 0.26, "size": 34}]},
]}
p.write_text(json.dumps(d, ensure_ascii=False, indent=1), encoding="utf-8")
