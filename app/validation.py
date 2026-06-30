import os
import json
from typing import Tuple
from jsonschema import validate
from jsonschema.exceptions import ValidationError


class JsonValidator:
    _schema_filename: str

    def __init__(self, schema_filename: str):
        self._schema_filename = schema_filename

    def validate(self, json_filename: str) -> Tuple[bool, str]:
        with open(self._schema_filename, "r", encoding="utf-8") as file:
            schema = json.load(file)

        with open(json_filename, "r", encoding="utf-8") as file:
            data = json.load(file)

        try:
            validate(instance=data, schema=schema)
            return True, "ok"
        except ValidationError as e:
            return False, e.message


class QuestionValidator(JsonValidator):
    SCHEMA_FILENAME: str = os.path.join("data", "questions-schema.json")

    def __init__(self):
        super().__init__(self.SCHEMA_FILENAME)

    def validate(self, json_filename: str) -> Tuple[bool, str]:
        valid, message = super().validate(json_filename)
        if not valid:
            return valid, message

        with open(json_filename, "r", encoding="utf-8") as file:
            data = json.load(file)

        for idx, question in enumerate(data):
            if not os.path.exists(
                os.path.join("images", "questions", question["image"]["de"])
            ):
                return (False, f"German image for question #{idx} does not exist.")

            if not os.path.exists(
                os.path.join("images", "questions", question["image"]["en"])
            ):
                return (False, f"English image for question #{idx} does not exist.")

            if question["type"] == "multiple_choice":
                if not isinstance(question["right_answer_index"], int):
                    return (
                        False,
                        f"The right_answer_index for question #{idx} "
                        f"has to be an integer.",
                    )

                if question["right_answer_index"] < 0:
                    return (
                        False,
                        f"The right_answer_index for question #{idx} "
                        f"has to be greater of equal to zero.",
                    )

                if question["right_answer_index"] > len(question["answers"]):
                    return (
                        False,
                        f"The right_answer_index for question #{idx} has "
                        f"to be less than the amount.",
                    )

                if len(question["scores"]) != len(question["answers"]):
                    return (
                        False,
                        f"There must be as many scores as answers in question #{idx}."
                    )

            elif question["type"] == "guess":
                pass

        return True, "ok"
