from app.question_model.question import Question
from app.question_model.multiple_choice_question import MultipleChoiceQuestion
from app.question_model.guess_question import GuessQuestion

from typing import Any, Dict, List


class QuestionFactory:

    @classmethod
    def from_dict(cls, question_dict: Dict[str, Any]) -> Question:
        question_type = question_dict["type"]
        del question_dict["type"]

        match question_type:
            case "guess":
                return GuessQuestion(**question_dict)

            case "multiple_choice":
                return MultipleChoiceQuestion(**question_dict)

            case _:
                raise ValueError(f"Unkown question type: {question_type}")

    @classmethod
    def many_from_dict(cls, question_list: List[Dict[str, Any]]) -> List[Question]:
        return [cls.from_dict(d) for d in question_list]
