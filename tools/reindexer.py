import json
from tqdm import tqdm

reply = input("Did you commit data/questions.json? (yn)>").lower()
if reply != "y":
    exit()

with open("data/questions.json", 'r') as f:
    questions = json.load(f)

for i, q in tqdm(enumerate(questions), desc="Translating", total=len(questions)):
    q["index"] = i

with open("data/questions.json", 'w') as f:
    json.dump(questions, f, indent=4)
