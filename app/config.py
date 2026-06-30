import os
import json
from typing import Any


class Config:

    with open(os.path.join("data", "config.json"), "r") as f:
        _config = json.load()

    @classmethod
    def get(cls, key: str) -> Any:
        return cls._config[key]
