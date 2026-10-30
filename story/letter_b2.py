"""Writes Board 2 lettering into story/pages.json."""
import json
from pathlib import Path

p = Path(__file__).resolve().parent / "pages.json"
d = json.loads(p.read_text(encoding="utf-8"))
img = lambda i: f"assets/panels/b2/p{i}.png"
d["b2"] = {"panels": [
    {"image": img(1), "text": [
        {"type": "caption", "text": "1984. The whole street came.", "at": [0.015, 0.05], "max_w": 0.4}]},
    {"image": img(2), "text": [
        {"type": "bubble", "text": "Your daughter is marrying a shopkeeper.", "at": [0.21, 0.09], "tail": [0.3, 0.34], "max_w": 0.34, "size": 33},
        {"type": "bubble", "text": "My daughter is marrying a good man.", "at": [0.78, 0.11], "tail": [0.69, 0.33], "max_w": 0.32, "size": 33}]},
    {"image": img(3), "text": [
        {"type": "caption", "text": "Every Spring Festival we went to Chinatown. Smriti loved the lion dance more than I did.", "at": [0.56, 0.03], "max_w": 0.4, "size": 31}]},
    {"image": img(4), "text": [
        {"type": "bubble", "text": "Thinner! It's a dholl puri, not a dumpling!", "at": [0.5, 0.09], "tail": [0.67, 0.27], "max_w": 0.36, "size": 33},
        {"type": "bubble", "text": "Says the woman whose dumplings look like samosas.", "at": [0.17, 0.86], "tail": [0.27, 0.55], "max_w": 0.3, "size": 33}]},
    {"image": img(5), "text": [
        {"type": "caption", "text": "1990. Uncle Lam always said a shop full of children never goes broke.", "at": [0.02, 0.03], "max_w": 0.42, "size": 31},
        {"type": "bubble", "text": "Slow down! You'll knock over the rice!", "at": [0.8, 0.12], "tail": [0.6, 0.32], "max_w": 0.3, "size": 33}]},
    {"image": img(6), "text": [
        {"type": "caption", "text": "Spring Festival photo No. 18. Nobody invited the neighbours. They just came, every year. Somewhere along the way, they had become family, and this street had become home.", "at": [0.99, 0.025], "max_w": 0.35, "size": 30}]},
]}
p.write_text(json.dumps(d, ensure_ascii=False, indent=1), encoding="utf-8")
