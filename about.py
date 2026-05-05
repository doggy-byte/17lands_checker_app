import streamlit as st
import streamlit.components.v1 as components
from common_functions import open_or_download_db

st.title("このサイトについて/使い方")

st.markdown("MTGアリーナのリミテッドのプレイに役立つデータサイトです。")
st.markdown("データは[17Lands](https://www.17lands.com/)より取得しています。")

st.markdown("## 使い方解説動画")

st.markdown("### 指標クイズ")

components.html("""<iframe width="560" height="315" src="https://www.youtube.com/embed/nCmoqUwHUBw?si=8od0nrykSJphMbb2" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" referrerpolicy="strict-origin-when-cross-origin" allowfullscreen></iframe>""", height=330)

st.markdown("### カード別デッキ特徴統計/デッキカラー別特徴統計")

components.html("""<iframe width="560" height="315" src="https://www.youtube.com/embed/_lHgSKlhqm0?si=iguGzKVu7UGPXOij" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" referrerpolicy="strict-origin-when-cross-origin" allowfullscreen></iframe>""", height=330)

st.markdown("## 更新履歴")

df_update = open_or_download_db('update_log.csv', force_download=True)
df_update = df_update.sort_values(by='Date', ascending=False)

st.dataframe(
    df_update
)


