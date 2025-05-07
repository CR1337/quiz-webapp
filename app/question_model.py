from __future__ import annotations
from abc import ABC, abstractmethod
from typing import Any, Callable, Dict, List
from numbers import Number


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
            parameters |= {'min_guess': question_dict['min_guess']}
            parameters |= {'max_guess': question_dict['max_guess']}
            parameters |= {'step': question_dict['step']}
            if 'max_points' in question_dict:
                parameters |= {'max_points': question_dict['max_points']}
            if 'score_function' in question_dict:
                parameters |= {'score_function': eval(question_dict['score_function'])}
            return GuessQuestion(**parameters)
        
        elif question_type == 'multiple_choice':
            parameters |= {'answers': question_dict['answers']}
            parameters |= {'right_answer_index': question_dict['right_answer_index']}
            if 'score' in question_dict:
                parameters |= {'score': question_dict['score']}
            return MultipleChoiceQuestion(**parameters)
        
        else:
            raise ValueError(f"Unkown question type: {question_type}")

    @classmethod
    def many_from_dict(cls, question_list: List[Dict[str, Any]]) -> List[Question]:
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
    
    _answer: Number
    _score_function: ScoreFunction
    _min_guess: Number
    _max_guess: Number
    _step: Number
    _format: str
    _max_points: int

    def __init__(
        self, 
        text: Dict[str, str], 
        answer: Number, 
        min_guess: Number,
        max_guess: Number,
        step: Number,
        *,
        max_points: int  = 10,
        score_function: ScoreFunction | None = None,
        explanation: Dict[str, str] | None = None,
        image: Dict[str, str] | None = None,
        image_caption: Dict[str, str] | None = None
    ):
        self._answer = answer
        self._min_guess = min_guess
        self._max_guess = max_guess
        self._step = step
        self._format=f"%0.{self._get_decimal_places(step)}f"

        self._score_function = score_function or self._default_scoring_function
        self._max_points = max_points
        super().__init__(
            text, 
            explanation=explanation, 
            image=image, 
            image_caption=image_caption
        )

    def _default_scoring_function(self, true: Number, guess: Number) -> int:
        range_below = true - self._min_guess
        range_above = self._max_guess - true

        if guess < true:
            relative_error = (true - guess) / range_below
        else:
            relative_error = (guess - true) / range_above

        relative_error = min(max(relative_error, 0), 1)

        score = round(self._max_points * (1 - relative_error))
        return score

    def _get_decimal_places(self, step):
        step_str = f"{step:.16f}".rstrip('0')
        if '.' in step_str:
            return len(step_str.split('.')[-1])
        return 0

    def check(self, guess: Number) -> int:
        return self._score_function(self._answer, guess)
    
    @property
    def answer(self) -> Number:
        return self._answer
    
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
        self._answers = answers
        self._right_answer_index = right_answer_index
        self._score = score
        super().__init__(
            text, 
            explanation=explanation, 
            image=image, 
            image_caption=image_caption
        )

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
    