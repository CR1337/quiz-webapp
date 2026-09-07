from app.question_model.question import Question
from dataclasses import dataclass, field
from numbers import Number
from app.localization import LocalizedText, Localization
import math
from typing import Tuple, ClassVar


@dataclass
class GuessQuestion(Question):
    MINUTES_PER_HOUR: ClassVar[int] = 60
    BASE_10: ClassVar[int] = 10

    answer: Number
    min_guess: Number
    max_guess: Number
    min_scoring_guess: Number
    max_scoring_guess: Number
    max_points: int
    unit: LocalizedText
    is_hm_time: bool

    decimal_places: int = field(init=False)
    step_count: int = field(init=False)
    step_size: Number = field(init=False)
    initial_guess: Number = field(init=False)
    format_: str = field(init=False)

    def __post_init__(self):
        answer_str = f"{self.answer:.4f}".rstrip("0")
        if "." in answer_str:
            self.decimal_places = len(answer_str.split(".")[-1])
        else:
            self.decimal_places = 0

        self.step_count = int((self.max_guess - self.min_guess) * self.BASE_10 ** self.decimal_places)
        self.step_size = (self.max_guess - self.min_guess) / self.step_count

        self.initial_guess = round((self.max_guess + self.min_guess) / 2, self.decimal_places)

        if self.unit[Localization.language()]:
            safe_unit = self.unit[Localization.language()].replace("%", "%%")
            self.format_ = f"%0.{self.decimal_places}f {safe_unit}"
        else:
            self.format_ = f"%0.{self.decimal_places}f"

    def render_number_with_unit(self, number: Number) -> str:
        string = ""

        if self.is_hm_time:
            fractional, hours = math.modf(number)
            minutes = round(fractional * self.MINUTES_PER_HOUR)
            hours = int(hours)
            minutes = int(minutes)

            if minutes == 0:
                string = f"{hours} {Localization.get('hours')}"
            else:
                string = f"{hours} {Localization.get('hours')} {Localization.get('and')} {minutes} {Localization.get('minutes')}"

        else:
            string = f"{number:.{self.decimal_places}f}"

            if Localization.language() == "de":
                string = string.replace(".", ",")

            if self.unit[Localization.language()]:
                safe_unit = self.unit[Localization.language()]
                string += f" {safe_unit}"

        return string

    def get_max_points(self) -> int:
        return self.max_points

    def check(self, user_answer: Number) -> Tuple[bool, int]:
        return self.min_scoring_guess <= user_answer <= self.max_scoring_guess, self._scoring(user_answer)

    def _scoring(self, user_answer: Number) -> int:
        if user_answer < self.min_scoring_guess or user_answer > self.max_scoring_guess:
            return 0

        distance = abs(user_answer - self.answer)
        max_distance = (
            abs(self.max_scoring_guess - self.answer)
            if user_answer > self.answer
            else abs(self.min_scoring_guess - self.answer)
        )

        return round(self.max_points * ((max_distance - distance) / max_distance))
