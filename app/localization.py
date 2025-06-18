import os
import json
import streamlit as st
from typing import Any


class Localization:
    LOCALIZATION_FILENAME: str = os.path.join("data", "localization.json")

    with open(LOCALIZATION_FILENAME, "r", encoding="utf-8") as file:
        _localization = json.load(file)

    @classmethod
    def get_for_language(cls, key: str, language: str) -> Any:
        return cls._localization[key][language]

    @classmethod
    def get(cls, key: str) -> Any:
        language = st.session_state["language"]
        return cls.get_for_language(key, language)

    @classmethod
    def language(cls) -> str:
        return st.session_state["language"]
