import streamlit as st

st.set_page_config(page_title="Unofficial 17Lands Metrics Quiz")

metrics_quiz = st.Page(page="metrics_quiz.py", title="Which is stronger?")
best_color = st.Page(page="best_color.py", title="Best Deck Color")

pg = st.navigation([metrics_quiz, best_color])
pg.run()