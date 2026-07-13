import os
import glob
import json
import streamlit as st
from streamlit_scroll_to_top import scroll_to_here
from app.question_model.question_factory import QuestionFactory
from app.question_model.question import Question
from app.localization import Localization
from app.config import Config
from app.validation import QuestionValidator
from app.state import QuizState
from app.question_selection import QuestionSelector


def configure_page():
    # set favicon
    favicon_files = glob.glob(os.path.join("images", "favicon.*"))
    favicon_path = favicon_files[0] if favicon_files else None

    # set page config
    st.set_page_config(
        page_title=Localization.get("quiz"),
        page_icon=favicon_path,
        layout="centered",
    )

    # configure scroll to top
    if "scroll_to_top" not in st.session_state:
        st.session_state["scroll_to_top"] = False

    if st.session_state["scroll_to_top"]:
        scroll_to_here(0, key="top")
        st.session_state["scroll_to_top"] = False

    # remove streamlit buttons
    st.write("")
    st.write("")
    st.markdown(
        r"""
        <style>
        .stAppDeployButton {
            visibility: hidden;
        }
        button[aria-label="Fullscreen"] {
            display: none !important;
        }
        span[data-testid="stHeaderActionElements"] {
            display: none !important;
        }
        span:has(> span[aria-label="check icon"]) {
            color: yellow;
            font-weight: bold;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )


def initialize_questions():
    question_filename: str = st.query_params.get("question_filename") or os.path.join(
        "data", "questions.json"
    )

    if st.session_state.get("question_index", None) is None:
        valid, message = QuestionValidator().validate(question_filename)
        if not valid:
            st.header(f"The question list in {question_filename} is invalid.")
            st.write(f"Error message: {message}")
            return None

        with open(question_filename, "r") as file:
            question_list = json.load(file)

        question_list = QuestionSelector.select_questions(question_list)

        st.session_state["question_index"] = 0
        st.session_state["questions"] = QuestionFactory.many_from_dict(question_list)
        st.session_state["max_points"] = Question.get_max_points_for(
            st.session_state["questions"]
        )
        st.session_state["score"] = 0
        st.session_state["state"] = QuizState.INIT
        st.session_state["slider_moved"] = False
        st.session_state["answer"] = None
        st.session_state["last_score"] = None

    current_question = st.session_state["questions"][st.session_state["question_index"]]

    return current_question


def render_main() -> Question | None:
    Localization.load()
    Config.load()
    configure_page()
    return initialize_questions()
