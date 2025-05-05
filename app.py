import streamlit as st
from app.main import render_main
from app.init import render_init
from app.question import render_question
from app.solution import render_solution
from app.result import render_result
from app.shared import render_back_to_home_button


current_question = render_main()

if st.session_state['state'] == 'init':
    render_init()

elif st.session_state['state'] == 'question': 
    render_question(current_question)
    
elif st.session_state['state'] == 'solution':
    render_solution(current_question)

elif st.session_state['state'] == 'result':
    render_result()

if st.session_state['state'] != 'init':
    render_back_to_home_button()
