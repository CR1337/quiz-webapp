import streamlit as st
from app.question_model import Question, GuessQuestion, MultipleChoiceQuestion
from app.pages.shared import render_score, render_progress, scroll_to_top
from app.localization import Localization
from app.state import QuizState


def render_solution(current_question: Question):
    render_progress()

    st.header(current_question.text[Localization.language()])

    

    if isinstance(current_question, GuessQuestion):
        if current_question.unit[Localization.language()] is not None:
            safe_unit = current_question.unit[Localization.language()]
        else:
            safe_unit = ""

        st.subheader(
            f"{Localization.get('your_answer')}: {st.session_state['answer']:.{current_question.decimal_places}f} {safe_unit}"
        )
        st.subheader(f"{Localization.get('correct_answer')}: {current_question.answer} {safe_unit}")

    elif isinstance(current_question, MultipleChoiceQuestion):
        st.subheader(
            f":primary[{Localization.get('your_answer')}: "
            f"{current_question.answers[Localization.language()][st.session_state['answer']]}]"
        )
        st.subheader(
            f"{Localization.get('correct_answer')}: "
            f"{current_question.answers[Localization.language()][current_question.right_answer_index]}"
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
