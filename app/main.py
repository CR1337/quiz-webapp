
import json
import streamlit as st
from model.question import Question
from app.localization import Localization


def render_main() -> Question:
    if st.session_state.get('language', None) is None:
        st.session_state['language'] = 'de'
        
    st.set_page_config(page_title=Localization.get('quiz'), page_icon="❓", layout="centered")

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

    question_filename: str = st.query_params.get('question_filename') or "questions.json"

    if st.session_state.get('question_index', None) is None:
        st.session_state['question_index'] = 0
        with open(question_filename, 'r') as file:
            question_list = json.load(file)
        st.session_state['questions'] = Question.many_from_dict(question_list)
        st.session_state['max_points'] = Question.get_max_points(st.session_state['questions'])
        st.session_state['score'] = 0
        st.session_state['state'] = 'init'  # init, question, solution, result
        st.session_state['answer'] = None
        st.session_state['last_score'] = None

    current_question = st.session_state['questions'][st.session_state['question_index']]

    return current_question