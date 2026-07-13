import os
import json
from typing import Any


class Config:

    @classmethod
    def load(cls):
        with open(os.path.join("data", "config.json"), "r") as f:
            cls._config = json.load(f)

    @classmethod
    def get(cls, key: str) -> Any:
        return cls._config[key]
