
import os
import json
import streamlit as st
from streamlit_scroll_to_top import scroll_to_here
from app.question_model import Question
from app.localization import Localization
from app.validation import QuestionValidator
from app.state import QuizState


def render_main() -> Question | None:
    if st.session_state.get('language', None) is None:
        st.session_state['language'] = 'de'
        
    st.set_page_config(
        page_title=Localization.get('quiz'), 
        page_icon=os.path.join("images", "favicon.ico"), 
        layout="centered"
    )

    if 'scroll_to_top' not in st.session_state:
        st.session_state['scroll_to_top'] = False

    if st.session_state['scroll_to_top']:
        scroll_to_here(0, key='top')
        st.session_state['scroll_to_top'] = False
    st.write("")
    st.write("")

    # Enable for debugging:
    # st.json(st.session_state)

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
        </style>
        """, unsafe_allow_html=True
    )

    question_filename: str = (
        st.query_params.get('question_filename') 
        or os.path.join("data", "questions.json")
    )

    if st.session_state.get('question_index', None) is None:
        valid, message = QuestionValidator().validate(question_filename)
        if not valid:
            st.header(f"The question list in {question_filename} is invalid.")
            st.write(f"Error message: {message}")
            return None

        with open(question_filename, 'r') as file:
            question_list = json.load(file)
        
        st.session_state['question_index'] = 0
        st.session_state['questions'] = Question.many_from_dict(question_list)
        st.session_state['max_points'] = Question.get_max_points(st.session_state['questions'])
        st.session_state['score'] = 0
        st.session_state['state'] = QuizState.INIT
        st.session_state['answer'] = None
        st.session_state['last_score'] = None

    current_question = st.session_state['questions'][st.session_state['question_index']]

    return current_question