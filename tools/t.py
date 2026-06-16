import json
from tqdm import tqdm
from deep_translator import GoogleTranslator

with open("data/questions.json", 'r') as f:
    questions = json.load(f)

translator = GoogleTranslator(source="de", target="en")

for q in tqdm(questions, desc="Translating", total=len(questions)):
    if q["text"]["en"] == q["text"]["de"]:
        q["text"]["en"] = "TODO"

    if q["type"] == "guess":
        if q["unit"]["en"] == q["unit"]["de"]:
            q["unit"]["en"] = "TODO"

    if q["explanation"]["en"] == q["explanation"]["de"]:
        q["explanation"]["en"] = "TODO"

    if q["type"] == "multiple_choice" and any(a_de == a_en for a_de, a_en in zip(q["answers"]["de"], q["answers"]["de"])):
        for i in range(len(q["answers"]["en"])):
            q["answers"]["en"][i] = "TODO"

with open("data/questions.json", 'w') as f:
    json.dump(questions, f, indent=4)
