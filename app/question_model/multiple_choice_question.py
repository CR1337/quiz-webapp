from app.question_model.question import Question
from dataclasses import dataclass
import random
from app.localization import LocalizedText
from typing import List, Tuple


@dataclass
class MultipleChoiceQuestion(Question):
    answers: List[LocalizedText]
    scores: List[int]
    right_answer_index : int

    def shuffle_answers(self):
        permutation = list(range(len(self.answers)))
        random.shuffle(permutation)

        shuffled_answers = [self.answers[i] for i in permutation]
        shuffled_scores = [self.scores[i] for i in permutation]
        new_right_answer_index = permutation.index(self.right_answer_index)

        self.answers = shuffled_answers
        self.scores = shuffled_scores
        self.right_answer_index = new_right_answer_index

    def get_max_points(self) -> int:
        return max(self.scores)

    def check(self, answer: int) -> Tuple[bool, int]:
        return answer == self.right_answer_index, self.scores[answer]
