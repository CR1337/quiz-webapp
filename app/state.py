from enum import Enum


class QuizState(Enum):
    INIT = 0
    QUESTION = 1
    SOLUTION = 2
    RESULT = 3
