"""Writes Board 4 lettering into story/pages.json."""
import json
from pathlib import Path

p = Path(__file__).resolve().parent / "pages.json"
d = json.loads(p.read_text(encoding="utf-8"))
img = lambda i: f"assets/panels/b4/p{i}.png"
d["b4"] = {"panels": [
    {"image": img(1), "text": [
        {"type": "caption", "text": "Spring Festival, 2027. Fifty-five years after a boy with one suitcase first stood on this road.", "at": [0.008, 0.03], "max_w": 0.155, "size": 28},
        {"type": "caption", "text": "Wei had the plaster stripped away, so the old basalt walls Uncle Lam built could be seen again.", "at": [0.008, 0.29], "max_w": 0.155, "size": 28}]},
    {"image": img(2), "text": [
        {"type": "caption", "text": "Dumplings beside dholl puri. Nobody at this table could remember it any other way.", "at": [0.01, 0.03], "max_w": 0.4, "size": 30}]},
    {"image": img(3), "text": [
        {"type": "bubble", "text": "Grandpa... I got in. I'm going to study in China!", "at": [0.6, 0.11], "tail": [0.43, 0.24], "max_w": 0.32, "size": 32}]},
    {"image": img(4), "text": [
        {"type": "bubble", "text": "Happy Spring Festival, Mauritius!", "at": [0.3, 0.09], "tail": [0.36, 0.33], "max_w": 0.36, "size": 32},
        {"type": "bubble", "text": "Happy Spring Festival, Meizhou!", "at": [0.55, 0.9], "tail": [0.83, 0.66], "max_w": 0.32, "size": 32}]},
    {"image": img(5), "text": [
        {"type": "caption", "text": "Spring Festival photo No. 55. We needed a wider lens.", "at": [0.01, 0.03], "max_w": 0.36, "size": 30}]},
    {"image": img(6), "text": [
        {"type": "bubble", "text": "It brought me here. Let it bring you back.", "at": [0.36, 0.13], "tail": [0.25, 0.3], "max_w": 0.18, "size": 32},
        {"type": "caption", "text": "55 years. Two homes. One family.", "at": [0.99, 0.95], "max_w": 0.3, "size": 34}]},
]}
p.write_text(json.dumps(d, ensure_ascii=False, indent=1), encoding="utf-8")
