import streamlit as st
from app.localization import Localization


def render_result():
    score = st.session_state['score']
    max_points = st.session_state['max_points']
    if score > max_points / 2:
        st.balloons()
    else:
        st.snow()
    st.header(Localization.get('score_announcement').format(
        score=score, max_points=max_points)
    )
