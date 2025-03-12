import streamlit as st

st.set_page_config(page_title="3rd-party 17Lands Data Apps", layout='wide')

about = st.Page(page="about.py", title="About")
metrics_quiz = st.Page(page="metrics_quiz.py", title="Which is stronger?")
cardwise_stats = st.Page(page="cardwise_deck_stats.py", title="Card-wise Deck Stats")
colorwise_stats = st.Page(page="colorwise_deck_stats.py", title="Color-wise Deck Stats")

pg = st.navigation([about, metrics_quiz, cardwise_stats, colorwise_stats])
pg.run()