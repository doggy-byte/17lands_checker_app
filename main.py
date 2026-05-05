import streamlit as st

st.set_page_config(page_title="17Landsデータアプリ", layout='wide')

about = st.Page(page="about.py", title="このサイトについて/使い方")
metrics_quiz = st.Page(page="metrics_quiz.py", title="指標クイズ")
cardwise_stats = st.Page(page="cardwise_deck_stats.py", title="カード別デッキ特徴統計")
colorwise_stats = st.Page(page="colorwise_deck_stats.py", title="デッキカラー別特徴統計")

pg = st.navigation([about, metrics_quiz, cardwise_stats, colorwise_stats])
pg.run()