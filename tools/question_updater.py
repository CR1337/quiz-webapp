import json
import copy


with open("data/questions.json", "r", encoding="utf-8") as file:
    qs = json.load(file)

with open("data/questions-backup.json", "w", encoding="utf-8") as file:
    json.dump(qs, file, indent=4)

for q in qs:
    if q["type"] == "guess":
        if "is_hm_time" not in q:
            q["is_hm_time"] = False

        assert "answer" in q

        if "min_scoring_guess" not in q:
            assert "min_guess" in q
            q["min_scoring_guess"] = (q["answer"] + q["min_guess"]) // 2

        if "max_scoring_guess" not in q:
            assert "max_guess" in q
            q["max_scoring_guess"] = (q["answer"] + q["max_guess"]) // 2

    else:
        if "scores" not in q:
            assert "score" in q
            assert "right_answer_index" in q
            q["scores"] = [0] * 4
            q["scores"][q["right_answer_index"]] = q["score"]
            del q["score"]

        assert "answers" in q
        answers_ = copy.deepcopy(q["answers"])
        q["answers"] = {"de": [], "en": []}
        for i in range(4):
            q["answers"]["de"].append(answers_[i]["de"])
            q["answers"]["en"].append(answers_[i]["en"])

with open("data/questions.json", "w", encoding="utf-8") as file:
    json.dump(qs, file, indent=4)
