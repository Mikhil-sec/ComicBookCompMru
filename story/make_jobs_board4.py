"""Builds story/jobs_board4.json (Board 4: Home, 2027)."""
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
b2 = json.loads((HERE / "jobs_board2.json").read_text(encoding="utf-8"))
V = {k: b2["vars"][k] for k in ("STYLE", "PANEL", "NORELIGION")}
V["WEI"] = "Wei is a 69-year-old Chinese (Hakka) grandfather with short white-grey hair and a single small mole below his RIGHT eye, shown on his character sheet."
V["SMRITI"] = "Smriti is a 67-year-old Indo-Mauritian grandmother with silver hair in a low bun and glasses on her head, shown on her character sheet."
V["MIRA"] = "Mira is their 18-year-old granddaughter, of mixed Chinese and Indo-Mauritian heritage, with a long black ponytail, shown on her character sheet."
S = "assets/sheets/"

jobs = [
    {"id": "shop_2027", "kind": "edit", "refs": ["assets/plates/shop_2008.png"],
     "out": "assets/plates/shop_2027.png", "size": "1792x768",
     "prompt": "Show this exact same two-storey shop from the exact same camera position, angle, lens and framing, 19 years later, in "
               "2027, lovingly restored. KEEP UNCHANGED: the building's shape, size and position; the upper floor, balcony and side "
               "staircase; the four doors; the signboard position; the frangipani's position; the distant mountains and the tall "
               "boulder-topped peak; the art style and muted colour grading. CHANGES: (1) on the GROUND FLOOR the plaster has been "
               "removed to reveal the original rough grey basalt stone blocks from 1972, cleaned and neatly pointed as a proud heritage "
               "feature; (2) the upper floor is freshly painted warm white, with sage-green wooden shutters beside the windows; (3) the "
               "four doors are refinished in deep red lacquered wood; (4) a new hand-carved wooden signboard in the style of the "
               "original, reading 'LAM STORE' and 林記; (5) a row of red lanterns hangs along the balcony railing; (6) the frangipani is "
               "now enormous and old, its canopy spreading over the balcony and the road, covered in blossoms; (7) a neat paved footpath "
               "with a low basalt-stone planter in front of the shop; (8) small solar panels on the roof; (9) the road is smooth tarmac "
               "with a few more modern houses in the distance. Warm golden late-afternoon light. No people. No text other than the "
               "sign. No watermark."},
    {"id": "b4p1", "kind": "edit", "refs": ["assets/plates/shop_2027.png"],
     "out": "assets/panels/b4/p1.png", "size": "1792x768",
     "prompt": "KEEP the building, sign, tree, road, background and camera angle exactly as in this plate. Scene: Spring Festival eve, "
               "2027, golden hour turning to dusk, the red lanterns glowing. A happy crowd of every Mauritian community (Indo-Mauritian, "
               "Creole, Sino-Mauritian, Franco-Mauritian; grandparents, parents, teenagers, small children) walks along the road and "
               "gathers in front of the shop, carrying covered dishes, trays of food and gift boxes, greeting each other, children "
               "running with small red lanterns. Festive, warm, joyful. Leave calm sky at the top-left for a caption. {NORELIGION} "
               "{PANEL} {STYLE}"},
    {"id": "b4p2", "kind": "edit", "refs": [S + "wei_69.png", S + "smriti_67.png", S + "mira_18.png"],
     "out": "assets/panels/b4/p2.png", "size": "1536x1024",
     "prompt": "The images are character sheets of Wei ({WEI}), Smriti ({SMRITI}) and Mira ({MIRA}). Scene: the Spring Festival "
               "reunion dinner in the backyard behind the shop, 2027, at night, under strings of warm lights and red lanterns, with "
               "the big frangipani tree overhead. One very long table seen from a slightly high angle down its length, packed with "
               "food from every kitchen: steaming dumplings, noodles, a whole fish, dholl puri flatbreads, bowls of curry, rougaille, "
               "sesame balls and cakes. About sixteen people of every Mauritian community, from babies to grandparents, laugh, pass "
               "dishes and talk across the table. At the far head of the table sit Wei in his red mandarin-collar jacket and Smriti in "
               "her green saree, beaming; Mira sits beside them. Joyful, abundant, warm. Leave calm space at the top-left for a "
               "caption. {NORELIGION} {PANEL} {STYLE}"},
    {"id": "b4p3", "kind": "edit", "refs": [S + "mira_18.png", S + "wei_69.png"],
     "out": "assets/panels/b4/p3.png", "size": "1536x1024",
     "prompt": "The images are character sheets of Mira ({MIRA}) and Wei ({WEI}). Scene: at the reunion dinner table at night, "
               "lantern light. Medium close-up. Mira, standing, holds up an official university letter on white paper toward her "
               "grandfather with both hands, beaming with a thrilled, slightly teary smile. The letter's heading is clearly readable "
               "in large print: 'SCHOLARSHIP OFFER' and below it 奖学金; the rest of the letter is small illegible lines. Wei, seated in "
               "his red mandarin-collar jacket, looks up at her, stunned, his mouth slightly open, a hand rising to his chest. Leave "
               "calm space above Mira's head for a speech bubble. {PANEL} {STYLE}"},
    {"id": "b4p4", "kind": "edit", "refs": [S + "wei_69.png", S + "smriti_67.png", S + "mira_18.png"],
     "out": "assets/panels/b4/p4.png", "size": "1536x1024",
     "prompt": "The images are character sheets of Wei ({WEI}), Smriti ({SMRITI}) and Mira ({MIRA}). Scene: at the dinner table at "
               "night, a video call. Mira holds up a tablet at arm's length. We see the tablet's screen in the foreground: on it, "
               "about six Hakka Chinese relatives of different ages crowd into the frame in a room in Meizhou decorated with red "
               "lanterns and paper cuttings, waving and laughing. Behind the tablet, on the Mauritian side, Wei, Smriti and Mira "
               "squeeze their faces together with three laughing neighbours of different Mauritian communities, all waving back at "
               "the screen. Joyful, crowded, funny. Leave calm space at the top for speech bubbles. {NORELIGION} {PANEL} {STYLE}"},
    {"id": "b4p5", "kind": "edit", "refs": ["assets/plates/shop_2027.png", S + "wei_69.png", S + "smriti_67.png", S + "mira_18.png"],
     "out": "assets/panels/b4/p5.png", "size": "1536x1024",
     "prompt": "The first image is the restored shop in 2027. The other images are character sheets of Wei ({WEI}), Smriti ({SMRITI}) "
               "and Mira ({MIRA}). Scene: Spring Festival morning, 2027, the 55th annual group photograph in front of the shop. The "
               "camera is closer than the plate, framing the basalt ground floor, the red doors, the LAM STORE sign and the lanterns. "
               "A huge, happy crowd of about thirty people of every Mauritian community squeezes into the photo, several rows deep, "
               "some standing on the bench, kids on shoulders, people leaning in from the edges. In the centre front, Wei sits on a "
               "wooden chair with Smriti standing beside him, her hand on his shoulder; Mira kneels in front of them. Everyone faces "
               "the camera, laughing. Warm morning light. Leave calm space at the top-left for a caption. {NORELIGION} {PANEL} {STYLE}"},
    {"id": "b4p6", "kind": "edit", "refs": [S + "mira_18.png", S + "wei_69.png", S + "smriti_67.png", S + "wei_14.png"],
     "out": "assets/panels/b4/p6.png", "size": "1792x768",
     "prompt": "The images are character sheets of Mira ({MIRA}), Wei ({WEI}), Smriti ({SMRITI}), and Wei as a boy in 1972 (only "
               "as the reference for the small brown cardboard suitcase tied with string). Scene: the departure hall of a modern "
               "airport in Mauritius, 2027, daytime, huge glass windows with a passenger plane and palm trees outside, sunlight "
               "pouring in. Wide shot. In the centre middle-ground, Mira walks toward the departure gate, seen mostly FROM BEHIND, her "
               "ponytail swinging, a backpack on one shoulder and in her right hand the OLD small brown cardboard suitcase tied with "
               "string, exactly like the boy's on his sheet: a mirror of his arrival in 1972. She turns her head back over her shoulder "
               "with a brave, teary smile. In the left foreground, seen from behind, Wei in his red jacket and Smriti in her green "
               "saree stand close together; Wei raises one hand in a wave, Smriti leans her head on his shoulder. Bittersweet, hopeful, "
               "luminous. No readable signs or text. Leave calm space at the top-left for a caption. {PANEL} {STYLE}"},
]

(HERE / "jobs_board4.json").write_text(
    json.dumps({"vars": V, "jobs": jobs}, ensure_ascii=False, indent=1), encoding="utf-8")
print(f"{len(jobs)} jobs written")
