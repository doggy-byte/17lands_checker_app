import streamlit as st

st.set_page_config(page_title="Unofficial 17Lands Metrics Quiz")

metrics_quiz = st.Page(page="metrics_quiz.py", title="Which is stronger?")

pg = st.navigation([metrics_quiz])
pg.run()