import streamlit as st
from common_functions import download_gcs_folder

@st.cache_resource
def initial_download():
    print("Downloading initial images...")
    download_gcs_folder("streamlit-17lands-checker-app", "card_images/", "card_images/")
    download_gcs_folder("streamlit-17lands-checker-app", "card_images_ja/", "card_images_ja/")
    print("Finished Download!")

st.set_page_config(page_title="17Landsデータアプリ", layout='wide')

initial_download()

about = st.Page(page="about.py", title="このサイトについて/使い方")
metrics_quiz = st.Page(page="metrics_quiz.py", title="指標クイズ")
cardwise_stats = st.Page(page="cardwise_deck_stats.py", title="カード別デッキ特徴統計")
colorwise_stats = st.Page(page="colorwise_deck_stats.py", title="デッキカラー別特徴統計")

pg = st.navigation([about, metrics_quiz, cardwise_stats, colorwise_stats])
pg.run()

