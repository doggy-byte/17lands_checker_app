import streamlit as st
from common_functions import open_or_download_db

st.title("About")

st.markdown("This is a collection of support apps for Magic: The Gathering Arena Premier Draft play.")
st.markdown("Statistics data was retrieved from [17Lands](https://www.17lands.com/).")

st.markdown("### Update Log")

df_update = open_or_download_db('update_log.csv', force_download=True)
df_update = df_update.sort_values(by='Date', ascending=False)

st.dataframe(
    df_update
)


