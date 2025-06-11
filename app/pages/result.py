import streamlit as st
from app.pages.shared import render_image
from app.localization import Localization


N_PREDICATES: int = 5


def render_result():
    score = st.session_state["score"]
    max_points = st.session_state["max_points"]
    predicate_index = min(int((score / max_points) * N_PREDICATES), N_PREDICATES - 1)
    if predicate_index < N_PREDICATES // 2:
        st.snow()
    else:
        st.balloons()
    st.header(Localization.get("thank_you"))
    st.subheader(
        Localization.get("score_announcement").format(
            score=score,
            max_points=max_points,
            predicate=Localization.get("predicates")[predicate_index],
            url="[www.destatis.de](https://destatis.de)",
        )
    )
    render_image("destatis.jpg")
