import os
import json
import streamlit as st
from numbers import Number
from typing import Any, Dict


LocalizedText = Dict[str, str]
LocalizedPath = Dict[str, str]


class Localization:
    LOCALIZATION_FILENAME: str = os.path.join("data", "localization.json")

    if st.session_state.get("language", None) is None:
        st.session_state["language"] = "de"

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

    @classmethod
    def flag(cls, language: str) -> str:
        return {
            "de": "🇩🇪",
            "en": "🇬🇧"
        }[language]

    @classmethod
    def other_language(cls) -> str:
        return {
            "de": "en",
            "en": "de"
        }[cls.language()]
