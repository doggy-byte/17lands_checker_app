import streamlit as st

st.set_page_config(page_title="Unofficial 17Lands Metrics Quiz")

about = st.Page(page="about.py", title="About")
metrics_quiz = st.Page(page="metrics_quiz.py", title="Which is stronger?")
#cardwise_stats = st.Page(page="cardwise_deck_stats.py", title="Cardwise Deck Stats")

pg = st.navigation([about, metrics_quiz])
pg.run()