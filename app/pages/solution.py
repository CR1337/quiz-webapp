import streamlit as st
from app.question_model import Question, GuessQuestion, MultipleChoiceQuestion
from app.pages.shared import render_score, render_question_image, scroll_to_top
from app.localization import Localization
from app.state import QuizState


def render_solution(current_question: Question):
    render_score(True)
    
    st.write(current_question.text[Localization.language()])

    if isinstance(current_question, GuessQuestion):
        right_answer = st.session_state['answer'] == current_question.answer
        st.subheader(
            f"{Localization.get('your_answer')}: {st.session_state['answer']:.{current_question.decimal_places}f}"
        )
        st.subheader(
            f"{Localization.get('correct_answer')}: {current_question.answer}"
        )

    elif isinstance(current_question, MultipleChoiceQuestion):
        right_answer = (
            current_question.answers
            [Localization.language()][st.session_state['answer']] 
            == current_question.answers
            [Localization.language()][current_question.right_answer_index]
        )
        if right_answer:
            st.subheader(
                f":primary[{Localization.get('your_answer')}: "
                f"{current_question.answers[Localization.language()][st.session_state['answer']]}]"
            )
        else:
            st.subheader(
                f"{Localization.get('your_answer')}: "
                f"{current_question.answers[Localization.language()][st.session_state['answer']]}"
            )
        st.subheader(
            f"{Localization.get('correct_answer')}: "
            f"{current_question.answers[Localization.language()][current_question.right_answer_index]}"
        )

    with st.expander(Localization.get('explanation'), expanded=True):
        st.markdown(f":primary[**{current_question.explanation[Localization.language()]}**]")

    if st.button(Localization.get('next'), use_container_width=True, type='primary'):
        st.session_state['question_index'] += 1
        if (
            st.session_state['question_index'] 
            >= len(st.session_state['questions'])
        ):
            st.session_state['question_index'] -= 1
            st.session_state['state'] = QuizState.RESULT
        else:
            st.session_state['state'] = QuizState.QUESTION
        scroll_to_top()
        st.rerun()

    if st.button("ENDE"):
        st.session_state['state'] = QuizState.RESULT
        st.rerun()