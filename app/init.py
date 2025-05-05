import streamlit as st
from app.shared import render_image
from app.localization import Localization


def render_init():
    render_image(f"title_{Localization.language()}.jpg")
    left_column, right_column = st.columns(spec=[0.9, 0.1])

    with left_column:
        if st.button(Localization.get('start_quiz'), use_container_width=True):
            st.session_state['state'] = "question"
            st.rerun()

    with right_column:
        if st.session_state['language'] == 'de':
            if st.button("", icon="🇬🇧", use_container_width=True):
                st.session_state['language'] = 'en'
                st.rerun()
        else:
            if st.button("", icon="🇩🇪", use_container_width=True):
                st.session_state['language'] = 'de'
                st.rerun()
