import os
from itertools import count
import streamlit as st
from app.pages.shared import render_image, scroll_to_top
from app.localization import Localization
from app.state import QuizState


def render_init():
    st.header(
        Localization.get("intro").format(number=len(st.session_state["questions"]))
    )
    st.divider()
    for i in count():
        png_filename = f"title{i}_{Localization.language()}.png"
        jpg_filename = f"title{i}_{Localization.language()}.jpg"
        if os.path.exists(os.path.join("images", png_filename)):
            render_image(png_filename)
        elif os.path.exists(os.path.join("images", jpg_filename)):
            render_image(jpg_filename)
        else:
            break
    st.divider()

    left_column, right_column = st.columns(spec=[0.9, 0.1])

    with left_column:
        if st.button(
            Localization.get("start_quiz"), use_container_width=True, type="primary"
        ):
            st.session_state["state"] = QuizState.QUESTION
            scroll_to_top()
            st.rerun()

    with right_column:
        if st.session_state["language"] == "de":
            if st.button("", icon="🇬🇧", use_container_width=True):
                st.session_state["language"] = "en"
                st.rerun()
        else:
            if st.button("", icon="🇩🇪", use_container_width=True):
                st.session_state["language"] = "de"
                st.rerun()
