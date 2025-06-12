import os
import streamlit as st
from app.question_model import Question
from app.localization import Localization
from app.state import QuizState
from app.colors import Color, BLUE, GRAY, GREEN
from streamlit.delta_generator import DeltaGenerator


BADGE_HTML_FILENAME: str = os.path.join("app", "html", "badge.html.template")


@st.cache_data(show_spinner=False)
def load_badge_html():
    with open(BADGE_HTML_FILENAME, "r") as file:
        return file.read()


badge_html_template = load_badge_html()


def render_score(display_delta: bool = False):
    index = st.session_state["question_index"]
    question = st.session_state["questions"][index]

    if display_delta:
        left_column, right_column = st.columns(2)

        left_column.metric(
            label=f"{Localization.get('score_delta')} {index + 1}",
            value=f"{st.session_state['last_score']}/{question.max_points}",
        )

        right_column.metric(
            label=Localization.get("your_new_score"),
            value=f"{st.session_state['score']}/{st.session_state['max_points']}",
        )

    else:
        st.metric(
            label=Localization.get("your_score"),
            value=f"{st.session_state['score']}/{st.session_state['max_points']}",
        )


def custom_badge(parent: DeltaGenerator, text: str, icon: str, color: Color):
    r, g, b = color
    parent.html(badge_html_template.format(text=text, icon=icon, r=r, g=g, b=b))


def render_progress():
    index = st.session_state["question_index"]
    question_amount = len(st.session_state["questions"])

    columns = st.columns(question_amount)
    for idx, column in enumerate(columns):
        if idx < index:
            icon = "check"
            color = GREEN
        elif idx == index and st.session_state["state"] == QuizState.QUESTION:
            icon = "arrow_downward"
            color = BLUE
        elif idx == index and st.session_state["state"] == QuizState.SOLUTION:
            icon = "check"
            color = GREEN
        else:
            icon = "question_mark"
            color = GRAY

        custom_badge(column, f"{idx + 1}", icon=icon, color=color)


def render_image(image: str, caption: str | None = None, directory: str = "images"):
    st.image(os.path.join(directory, image), caption)


def render_question_image(question: Question):
    render_image(
        question.image[Localization.language()],
        question.image_caption[Localization.language()],
        os.path.join("images", "questions"),
    )


def render_back_to_home_button():
    def reset():
        st.session_state["question_index"] = None
        st.session_state.score = 0
        st.session_state["state"] = QuizState.INIT
        st.session_state["answer"] = None
        st.rerun()

    @st.dialog(Localization.get("really_stop"))
    def back_to_home_dialog():
        left_column, right_column = st.columns(2)
        if left_column.button(Localization.get("no"), use_container_width=True):
            st.rerun()
        elif right_column.button(Localization.get("yes"), use_container_width=True):
            reset()

    st.divider()
    if st.button(
        Localization.get("back_to_home"),
        use_container_width=True,
        type="primary"
        if st.session_state["state"] == QuizState.RESULT
        else "secondary",
    ):
        if st.session_state["state"] == QuizState.RESULT:
            reset()
        else:
            back_to_home_dialog()


def scroll_to_top():
    st.session_state["scroll_to_top"] = True
