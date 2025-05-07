import streamlit as st
from app.pages.main import render_main
from app.pages.init import render_init
from app.pages.question import render_question
from app.pages.solution import render_solution
from app.pages.result import render_result
from app.pages.shared import render_back_to_home_button
from app.state import QuizState


current_question = render_main()

if current_question is not None:
    if st.session_state['state'] == QuizState.INIT:
        render_init()

    elif st.session_state['state'] == QuizState.QUESTION: 
        render_question(current_question)
        
    elif st.session_state['state'] == QuizState.SOLUTION:
        render_solution(current_question)

    elif st.session_state['state'] == QuizState.RESULT:
        render_result()

    if st.session_state['state'] != QuizState.INIT:
        render_back_to_home_button()
