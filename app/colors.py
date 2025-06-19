import os
import json
from typing import Dict, Tuple

Color = Tuple[int, int, int]

class Colors:
    COLORS_FILENAME: str = os.path.join("data", "colors.json")
    with open(COLORS_FILENAME, "r") as file:
        _colors: Dict[str, Color] = {k: tuple(c) for k, c in json.load(file).items()}

    @classmethod
    def get(cls, key: str) -> Color:
        return cls._colors[key]

