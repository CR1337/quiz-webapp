import os
from itertools import count
import zipfile
import streamlit as st
from app.config import Config
from app.pages.shared import render_image, scroll_to_top
from app.localization import Localization
from app.state import QuizState


def render_importer():
    if not Config.get("question_importer"):
        return

    file = st.file_uploader("Quizdatei hochladen", ".zip")
    if file:
        with zipfile.ZipFile(file, "r") as zip_file:
            for filename in zip_file.namelist():
                with zip_file.open(filename, "r") as in_file:
                    with open(filename, "w") as out_file:
                        out_file.write(in_file.read())

        st.session_state.clear()
        st.rerun()


def render_title():
    st.header(Localization.get("intro").format(
        number=len(st.session_state["questions"])
    ))


def render_images():
    for i in count():
        png_filename = f"title{i}_{Localization.language()}.png"
        jpg_filename = f"title{i}_{Localization.language()}.jpg"

        if os.path.exists(os.path.join("images", png_filename)):
            render_image(png_filename)

        elif os.path.exists(os.path.join("images", jpg_filename)):
            render_image(jpg_filename)

        else:
            break


def render_explanation():
    intro_explanation = Localization.get("intro_explanation")
    if len(intro_explanation) > 0:
        st.text(intro_explanation)
        st.divider()


def render_buttons():
    left_column, right_column = st.columns(spec=[0.9, 0.1])

    with left_column:
        if st.button(
            Localization.get("start_quiz"),
            use_container_width=True,
            type="primary"
        ):
            st.session_state["state"] = QuizState.QUESTION
            st.session_state["slider_moved"] = False
            scroll_to_top()
            st.rerun()

    with right_column:
        if st.button(Localization.flag(Localization.other_language()), use_container_width=True):
            st.session_state["language"] = Localization.other_language()
            st.rerun()


def render_init():
    render_title()
    st.divider()
    render_images()
    st.divider()
    render_explanation()
    render_buttons()
    render_importer()
