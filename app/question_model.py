from __future__ import annotations
from abc import ABC, abstractmethod
from typing import Any, Callable, Dict, List, Tuple
from numbers import Number
import random


class Question(ABC):
    
    _text: Dict[str, str]
    _explanation: Dict[str, str] | None
    _image: Dict[str, str] | None
    _image_caption: Dict[str, str] | None

    @classmethod
    def from_dict(cls, question_dict: Dict[str, Any]) -> Question:
        question_type = question_dict['type']
        parameters = {'text': question_dict['text']}
        if 'explanation' in question_dict:
            parameters |= {'explanation': question_dict['explanation']}

        if 'image' in question_dict:
            parameters |= {'image': question_dict['image']}

        if 'image_caption' in question_dict:
            parameters |= {'image_caption': question_dict['image_caption']}

        if question_type == 'guess':
            parameters |= {'answer': question_dict['answer']}
            if 'max_points' in question_dict:
                parameters |= {'max_points': question_dict['max_points']}
            if 'score_function' in question_dict:
                parameters |= {
                    'score_function': eval(question_dict['score_function'])
                }
            return GuessQuestion(**parameters)
        
        elif question_type == 'multiple_choice':
            parameters |= {'answers': question_dict['answers']}
            parameters |= {
                'right_answer_index': question_dict['right_answer_index']
            }
            if 'score' in question_dict:
                parameters |= {'score': question_dict['score']}
            return MultipleChoiceQuestion(**parameters)
        
        else:
            raise ValueError(f"Unkown question type: {question_type}")

    @classmethod
    def many_from_dict(
        cls, 
        question_list: List[Dict[str, Any]]
    ) -> List[Question]:
        return [cls.from_dict(d) for d in question_list]
    
    @classmethod
    def get_max_points(cls, questions: List[Question]) -> int:
        score = 0
        for q in questions:
            if isinstance(q, GuessQuestion):
                score += q.max_points
            elif isinstance(q, MultipleChoiceQuestion):
                score += q.score
        return score

    def __init__(
            self, 
            text: str, 
            *, 
            explanation: Dict[str, str] | None = None, 
            image: Dict[str, str] | None = None, 
            image_caption: Dict[str, str] | None = None
        ):
        self._text = text
        self._explanation = explanation
        self._image = image
        self._image_caption = image_caption

    @abstractmethod
    def check(self, guess: Any) -> int:
        raise NotImplementedError("abstractmethod")
    
    @property
    def text(self) -> Dict[str, str]:
        return self._text
    
    @property
    def explanation(self) -> Dict[str, str] | None:
        return self._explanation
    
    @property
    def image(self) -> Dict[str, str] | None:
        return self._image
    
    @property
    def image_caption(self) -> Dict[str, str] | None:
        return self._image_caption


ScoreFunction = Callable[[int | float, int | float], int]


class GuessQuestion(Question):

    SLIDER_STEP_COUNT: int = 200
    SLIDER_SCALE_FACTOR: float = 5.0
    
    _answer: Number
    _score_function: ScoreFunction
    _initial_guess: Number
    _min_guess: Number
    _max_guess: Number
    _step: Number
    _format: str
    _max_points: int
    _decimal_places: int

    def __init__(
        self, 
        text: Dict[str, str], 
        answer: Number,
        *,
        max_points: int  = 10,
        score_function: ScoreFunction | None = None,
        explanation: Dict[str, str] | None = None,
        image: Dict[str, str] | None = None,
        image_caption: Dict[str, str] | None = None
    ):
        self._answer = answer
        self._min_guess, self._max_guess = self._compute_slider_range(answer)
        self._initial_guess = (self._max_guess + self._min_guess) / 2
        self._decimal_places = self._get_decimal_places(self._answer)
        self._step = (self._max_guess - self._min_guess) / self.SLIDER_STEP_COUNT
        self._format=f"%0.{self._decimal_places}f"

        self._score_function = score_function or self._default_scoring_function
        self._max_points = max_points
        super().__init__(
            text, 
            explanation=explanation, 
            image=image, 
            image_caption=image_caption
        )

    def _compute_slider_range(self, answer: Number) -> Tuple[Number, Number]:
        range_half = answer / self.SLIDER_SCALE_FACTOR
        offset = random.uniform(-1, 1) * range_half
        midpoint = answer + offset
        min_val = midpoint - range_half
        max_val = midpoint + range_half
        return min_val, max_val

    def _default_scoring_function(self, true: Number, guess: Number) -> int:
        distance = abs(guess - true)
        max_distance = max(abs(true - self._min_guess), abs(true - self._max_guess))
        normalized = distance / max_distance if max_distance != 0 else 0
        score = self._max_points * (1 - normalized) #** k
        return round(score)

    def _get_decimal_places(self, answer):
        step_str = f"{answer:.4f}".rstrip('0')
        if '.' in step_str:
            return len(step_str.split('.')[-1])
        return 0

    def check(self, guess: Number) -> int:
        return self._score_function(self._answer, guess)
    
    @property
    def answer(self) -> Number:
        return self._answer
    
    @property
    def initial_guess(self) -> Number:
        return self._initial_guess
    
    @property
    def max_guess(self) -> Number:
        return self._max_guess
    
    @property
    def min_guess(self) -> Number:
        return self._min_guess
    
    @property
    def step(self) -> Number:
        return self._step
    
    @property
    def format(self) -> str:
        return self._format
    
    @property
    def max_points(self) -> int:
        return self._max_points
    
    @property
    def decimal_places(self) -> int:
        return self._decimal_places


class MultipleChoiceQuestion(Question):
    
    _answers: Dict[str, List[str]]
    _right_answer_index: int
    _score: int

    def __init__(
        self, 
        text: Dict[str, str], 
        answers: Dict[str, List[str]],
        right_answer_index: int,
        *, 
        score: int = 10,
        explanation: Dict[str, str] | None = None,
        image: Dict[str, str] | None = None,
        image_caption: Dict[str, str] | None = None
    ):
        self._answers, self._right_answer_index = self._shuffle_answers(
            answers, right_answer_index
        )

        self._score = score
        super().__init__(
            text, 
            explanation=explanation, 
            image=image, 
            image_caption=image_caption
        )

    def _shuffle_answers(
        self, 
        answers: Dict[str, List[str]], 
        right_answer_index: int
    ) -> Tuple[Dict[str, List[str]], int]:
        first_key = list(answers.keys())[0]
        permutation = list(range(len(answers[first_key])))
        random.shuffle(permutation)

        shuffled_answers = {}
        for language in answers.keys():
            shuffled_answers |= {
                language: [answers[language][i] for i in permutation]
            }

        return shuffled_answers, permutation[right_answer_index]

    def check(self, answer: int) -> int:
        if answer == self._right_answer_index:
            return self._score
        else:
            return 0
    
    @property
    def answers(self) -> Dict[str, List[str]]:
        return self._answers
    
    @property
    def right_answer_index(self) -> int:
        return self._right_answer_index
    
    @property
    def score(self) -> int:
        return self._score
    