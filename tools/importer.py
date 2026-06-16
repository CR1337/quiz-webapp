import os
import sys
import json
import base64
from itertools import count

filename = sys.arv[1]
with open(filename, 'r') as f:
    data = json.load(f)
questions = data["QUESTIONS"]
config = data["CONFIG"]

front_image_bytes = base64.b64decode(config["front_image_b64"])
back_image_bytes = base64.b64decode(config["back_image_b64"])

for suffix in ["png", "jpg", "jpeg"]:
    for i in count():
        title_path_de = os.path.join("images", f"title{i}_de.{suffix}")
        if os.path.exists(title_path_de):
            os.remove(title_path_de)
        title_path_en = os.path.join("images", f"title{i}_en.{suffix}")
        if os.path.exists(title_path_en):
            os.remove(title_path_en)
    os.remove(os.path.join("images", f"result_de.{suffix}"))
    os.remove(os.path.join("images", f"result_en.{suffix}"))

with open(os.path.join("images", "title0_de.png"), 'wb') as f:
    f.write(front_image_bytes)

with open(os.path.join("images", "title0_en.png"), 'wb') as f:
    f.write(front_image_bytes)

with open(os.path.join("images", "result_de.png"), 'wb') as f:
    f.write(back_image_bytes)

with open(os.path.join("images", "result_en.png"), 'wb') as f:
    f.write(back_image_bytes)

del config["front_image_b64"]
del config["back_image_b64"]

with open(os.path.join("data", "localization.json"), 'r') as f:
    localization = json.load(f)

if config["intro_explanation"]["de"] == "":
    localization["intro_explanation"]["de"] = None
else:
    localization["intro_explanation"]["de"] = config["intro"]["de"]

if config["intro_explanation"]["en"] == "":
    localization["intro_explanation"]["en"] = None
else:
    localization["intro_explanation"]["en"] = config["intro"]["en"]

localization["intro"]["de"] = config["title"]["de"]
localization["intro"]["en"] = config["title"]["en"]

with open(os.path.join("data", "localization.json"), 'w') as f:
    json.dump(localization, f)

del config["title"]
del config["intro"]

with open(os.path.join("data", "config.json"), 'w') as f:
    json.dump(config, f)

image_filenames = os.listdir(os.path.join("images", "questions"))
for filename in image_filenames:
    full_filename = os.path.join("images", "questions", filename)
    if os.path.exists(full_filename):
        os.remove(full_filename)

for question in questions:
    image_bytes = base64.b64decode(question["image_b64"])
    image_filename = os.path.join("images", "questions", question["image"]["de"])
    if question["image_caption"]["de"] == "":
        question["image_caption"]["de"] = None
    if question["image_caption"]["en"] == "":
        question["image_caption"]["en"] = None
    with open(image_filename, 'wb') as f:
        f.write(image_bytes)

    del question["image_b64"]

with open(os.path.join("data", "questions.json"), "w") as f:
    json.dump(questions, f)
