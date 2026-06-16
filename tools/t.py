import json
from tqdm import tqdm
from deep_translator import GoogleTranslator

with open("data/questions.json", 'r') as f:
    questions = json.load(f)

translator = GoogleTranslator(source="de", target="en")

for q in tqdm(questions, desc="Translating", total=len(questions)):
    q["text"]["en"] = "TODO"
    q["explanation"]["en"] = "TODO"

with open("data/questions.json", 'w') as f:
    json.dump(questions, f, indent=4)
