import streamlit as st
from app.question_model import Question, GuessQuestion, MultipleChoiceQuestion
from app.pages.shared import render_score, render_question_image, scroll_to_top
from app.localization import Localization
from app.state import QuizState


def render_solution(current_question: Question):
    render_score(True)
    
    st.subheader(current_question.text[Localization.language()])

    if current_question.image:
        render_question_image(current_question)

    if isinstance(current_question, GuessQuestion):
        right_answer = st.session_state['answer'] == current_question.answer
        st.caption(f"{Localization.get('your_answer')}: {st.session_state['answer']}")
        st.caption(f"{Localization.get('correct_answer')}: {current_question.answer}")

    elif isinstance(current_question, MultipleChoiceQuestion):
        right_answer = current_question.answers[Localization.language()][st.session_state['answer']] == current_question.answers[Localization.language()][current_question.right_answer_index]
        color = "green" if right_answer else "red"
        st.caption(f":{color}[{Localization.get('your_answer')}: {current_question.answers[Localization.language()][st.session_state['answer']]}]")
        st.caption(f"{Localization.get('correct_answer')}: {current_question.answers[Localization.language()][current_question.right_answer_index]}")

    with st.expander(Localization.get('explanation'), expanded=True):
        st.write(current_question.explanation[Localization.language()])

    if st.button(Localization.get('next'), use_container_width=True):
        st.session_state['question_index'] += 1
        if st.session_state['question_index'] >= len(st.session_state['questions']):
            st.session_state['question_index'] -= 1
            st.session_state['state'] = QuizState.RESULT
        else:
            st.session_state['state'] = QuizState.QUESTION
        scroll_to_top()
        st.rerun()
