from __future__ import annotations
from abc import ABC, abstractmethod
from typing import Any, List, Tuple, Optional
from app.localization import LocalizedText, LocalizedPath
from dataclasses import dataclass


@dataclass
class Question(ABC):
    index: int
    text: LocalizedText
    explanation: Optional[LocalizedText]
    image: Optional[LocalizedPath]
    image_caption: LocalizedText
    coupled_question_indices: List[int]

    @classmethod
    def get_max_points_for(cls, questions: List[Question]) -> int:
        return sum(q.get_max_points() for q in questions)

    @abstractmethod
    def get_max_points(self) -> int:
        raise NotImplementedError("@abstractmethod")

    @abstractmethod
    def check(self, answer: Any) -> Tuple[bool, int]:
        raise NotImplementedError("@abstractmethod")
