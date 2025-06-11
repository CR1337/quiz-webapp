import streamlit as st
from numbers import Number
from itertools import cycle
from app.question_model import Question, GuessQuestion, MultipleChoiceQuestion
from app.pages.shared import (
    render_score,
    render_progress,
    render_question_image,
    scroll_to_top,
)
from app.localization import Localization
from app.state import QuizState


def check_answer(current_question: Question, answer: Number):
    score = current_question.check(answer)
    st.session_state["score"] += score
    st.session_state["state"] = QuizState.SOLUTION
    st.session_state["last_score"] = score
    st.rerun()


def render_question(current_question: Question):
    render_score()
    render_progress()

    st.subheader(current_question.text[Localization.language()])

    if current_question.image:
        render_question_image(current_question)

    if isinstance(current_question, GuessQuestion):
        guess = st.slider(
            " ",
            min_value=float(current_question.min_guess),
            max_value=float(current_question.max_guess),
            value=float(current_question.initial_guess),
            step=float(current_question.step),
            format=current_question.format,
            label_visibility="hidden",
        )
        if st.button(
            Localization.get("submit_guess"), use_container_width=True, type="primary"
        ):
            st.session_state["answer"] = guess
            scroll_to_top()
            check_answer(current_question, guess)

    elif isinstance(current_question, MultipleChoiceQuestion):
        columns = st.columns(2)
        for answer_index, (answer, column) in enumerate(
            zip(current_question.answers[Localization.language()], cycle(columns))
        ):
            with column:
                if st.button(answer, use_container_width=True, type="primary"):
                    st.session_state["answer"] = answer_index
                    scroll_to_top()
                    check_answer(current_question, answer_index)
