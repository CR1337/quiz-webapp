import streamlit as st
from app.question_model.question import Question
from app.question_model.guess_question import GuessQuestion
from app.question_model.multiple_choice_question import MultipleChoiceQuestion
from app.pages.shared import render_score, render_progress, scroll_to_top
from app.localization import Localization
from app.state import QuizState


def render_solution(current_question: Question):
    render_progress()

    st.header(current_question.text[Localization.language()])

    if isinstance(current_question, GuessQuestion):
        st.subheader(
            f"{Localization.get('your_answer')}: {current_question.render_number_with_unit(st.session_state['answer'])}"
        )
        st.subheader(
            f"{Localization.get('correct_answer')}: {current_question.render_number_with_unit(current_question.answer)}"
        )

    elif isinstance(current_question, MultipleChoiceQuestion):
        st.subheader(
            f":primary[{Localization.get('your_answer')}: "
            f"{current_question.answers[st.session_state['answer']][Localization.language()]}]"
        )
        st.subheader(
            f"{Localization.get('correct_answer')}: "
            f"{current_question.answers[current_question.right_answer_index][Localization.language()]}"
        )

    st.divider()

    st.markdown(
        f":primary[**{current_question.explanation[Localization.language()]}**]"
    )

    st.divider()

    render_score(True)

    if st.button(Localization.get("next"), use_container_width=True, type="primary"):
        st.session_state["question_index"] += 1
        if st.session_state["question_index"] >= len(st.session_state["questions"]):
            st.session_state["question_index"] -= 1
            st.session_state["state"] = QuizState.RESULT
        else:
            st.session_state["state"] = QuizState.QUESTION
        scroll_to_top()
        st.rerun()
