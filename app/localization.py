import os
import json
import streamlit as st


class Localization:
    LOCALIZATION_FILENAME: str = os.path.join("data", "localization.json")

    with open(LOCALIZATION_FILENAME, "r", encoding="utf-8") as file:
        _localization = json.load(file)

    @classmethod
    def get(cls, key: str):
        language = st.session_state["language"]
        return cls._localization[key][language]

    @classmethod
    def language(cls) -> str:
        return st.session_state["language"]
