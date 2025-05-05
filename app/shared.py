import os
import streamlit as st
from model.question import Question
from app.localization import Localization


def render_score(display_delta: bool = False):
    st.metric(
        label=Localization.get('your_score'),
        value=f"{st.session_state['score']} / {st.session_state['max_points']}",
        delta=f"{st.session_state['last_score']}" if display_delta else None,
        delta_color=(
            ("normal" if st.session_state['last_score'] > 0 else "inverse") 
            if display_delta 
            else "normal"
        )
    )
    index = st.session_state['question_index']
    question_amount = len(st.session_state['questions'])
    if st.session_state['state'] == 'solution':
        progress_index = index + 1
    else:
        progress_index = index
    st.progress(
        progress_index / question_amount, 
        f"{Localization.get('question')} {index + 1}/{question_amount}"
    )


def render_image(image: str, caption: str | None = None, directory: str = "images"):
    st.image(os.path.join(directory, image), caption)


def render_question_image(question: Question):
    if st.session_state['state'] == "question":
        expander_args = {
            'label': "",
            'expanded': True
        }   
    else:
        expander_args = {
            'label': Localization.get('show_image'),
            'expanded': False
        }  
    with st.expander(**expander_args):
        render_image(
            question.image[Localization.language()], 
            question.image_caption[Localization.language()], 
            os.path.join("images", "questions")
        )


def render_back_to_home_button():
    st.divider()
    if st.button(Localization.get('back_to_home'), use_container_width=True):
        st.session_state['question_index'] = 0
        st.session_state.score = 0
        st.session_state['state'] = 'init'
        st.session_state['answer'] = None
        st.rerun()