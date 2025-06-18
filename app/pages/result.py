import os
import streamlit as st
from app.pages.shared import render_image
from app.localization import Localization


N_PREDICATES: int = min(
    len(Localization.get_for_language('predicates', 'de')),
    len(Localization.get_for_language('predicates', 'en'))
)


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
            predicate=Localization.get("predicates")[predicate_index]
        )
    )
    png_filename = f"result_{Localization.language()}.png"
    jpg_filename = f"result_{Localization.language()}.jpg"
    if os.path.exists(os.path.join("images", png_filename)):
        render_image(png_filename)
    else:
        render_image(jpg_filename)    
