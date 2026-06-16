import json
from tqdm import tqdm
from deep_translator import GoogleTranslator

reply = input("Did you commit data/questions.json? (yn)>").lower()
if reply != "y":
    exit()

with open("data/questions.json", 'r') as f:
    questions = json.load(f)

translator = GoogleTranslator(source="de", target="en")

for q in tqdm(questions, desc="Translating", total=len(questions)):
    if q["text"]["en"] == "TODO":
        q["text"]["en"] = translator.translate(q["text"]["de"])

    if q["type"] == "guess":
        if q["unit"]["en"] == "TODO":
            q["unit"]["en"] = translator.translate(q["unit"]["de"])

    if q["explanation"]["en"] == "TODO":
        q["explanation"]["en"] = translator.translate(q["explanation"]["de"])

    if q["type"] == "multiple_choice" and any(a == "TODO" for a in q["answers"]["en"]):
        for i in range(len(q["answers"]["en"])):
            q["answwers"]["en"][i] = translator.translate(q["answers"]["de"][i])

with open("data/questions.json", 'w') as f:
    json.dump(questions, f, indent=4)
