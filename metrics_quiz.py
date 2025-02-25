import streamlit as st
import pandas as pd
from PIL import Image
from pathlib import Path
from common_functions import open_or_download_image, open_or_download_db

#if 'filename_db' not in st.session_state:
#    st.session_state.df = pd.read_csv('dashboard_data/DSK_PremierDraft_All_20241001.csv')

#p = Path('dashboard_data')
#g = p.glob('*.csv')
#filenames_db = list(g)

#filenames_db = st.secrets['metrics_quiz']['filenames_db']

st.session_state.filter = ''

list_metrics = [
    "# Seen",
    "ALSA",
    "# Picked",
    "ATA",
    "# GP",
    "% GP",
    "GP WR",
    "# OH",
    "OH WR",
    "# GD",
    "GD WR",
    "# GIH",
    "GIH WR",
    "# GNS",
    "GNS WR",
    "IWD"
]

if 'set_mquiz' not in st.session_state:
    st.session_state.set_mquiz = st.secrets['sets'][-1]

if 'format_mquiz' not in st.session_state:
    st.session_state.format_mquiz = 'PremierDraft'

if 'color_mquiz'not in st.session_state:
    st.session_state.color_mquiz = 'All'

if 'metrics' not in st.session_state:
    st.session_state.metrics = ['GIH WR']

if 'filter' not in st.session_state:
    st.session_state.filter = ''

def callback_next():
    df = open_or_download_db(st.secrets[st.session_state.set_mquiz][st.session_state.format_mquiz][st.session_state.color_mquiz])
    #if 'filename_db' not in st.session_state:
    #    df = open_or_download_db(filenames_db[0])
    #else:
    #    df = open_or_download_db(st.session_state.filename_db)

    if len(st.session_state.filter) > 0:
        df_filtered = df.query(st.session_state.filter)
        df_sample = df_filtered[df_filtered[st.session_state.metrics].notnull().all()].sample(2).reset_index()
    else:
        df_sample = df[df[st.session_state.metrics].notnull().all(axis=1)].sample(2).reset_index()

    st.session_state.nameA = df_sample['Name'][0]
    st.session_state.nameB = df_sample['Name'][1]
    #st.session_state.qnameA = st.session_state.nameA.replace('//', '').replace(' ', '+')
    #st.session_state.qnameB = st.session_state.nameB.replace('//', '').replace(' ', '+')
    st.session_state.metricsA = list(df_sample[list(st.session_state.metrics)].iloc[0])
    st.session_state.metricsB = list(df_sample[list(st.session_state.metrics)].iloc[1])
    #st.session_state.imA = Image.open('card_images/{}/{}.png'.format(set_name, st.session_state.qnameA))
    #st.session_state.imB = Image.open("card_images/{}/{}.png".format(set_name, st.session_state.qnameB))
    st.session_state.imA = open_or_download_image(st.session_state.nameA)
    st.session_state.imB = open_or_download_image(st.session_state.nameB)
    st.session_state.answerA = ''
    for i, met in enumerate(st.session_state.metrics):
        st.session_state.answerA += '#### {}=___\n'.format(met)
    st.session_state.answerB = ''
    for i, met in enumerate(st.session_state.metrics):
        st.session_state.answerB += '#### {}=___\n'.format(met)

def callback_answer():
    st.session_state.answerA = ''
    for i, met in enumerate(st.session_state.metrics):
        if i >= len(st.session_state.metricsA):
            continue
        st.session_state.answerA += '#### {}={}\n'.format(met, st.session_state.metricsA[i])
    st.session_state.answerB = ''
    for i, met in enumerate(st.session_state.metrics):
        if i >= len(st.session_state.metricsB):
            continue
        st.session_state.answerB += '#### {}={}\n'.format(met, st.session_state.metricsB[i])
    #st.session_state.answerB = ''
    #st.session_state.answerB = '{}={}'.format(st.session_state.metrics, st.session_state.metricsB)

if not 'nameA' in st.session_state.keys():
    callback_next()

st.title("Which is stronger?")

st.markdown("Metrics data was retrieved from [17Lands](https://www.17lands.com/) after 12 days of embargo period.")

fil1, fil2, fil3, fil4 = st.columns(4)
with fil1:
    st.session_state.set_mquiz = st.selectbox('Set', st.secrets['sets'])
with fil2:
    st.session_state.format_mquiz = st.selectbox('Format', ['PremierDraft'])
with fil3:
    st.session_state.color_mquiz = st.selectbox('Deck Color', ['All', 'WU', 'WB', 'WR', 'WG', 'UB', 'UR', 'UG', 'BR', 'BG', 'RG'])
with fil4:
    #st.session_state.metrics = st.selectbox('Metrics', list_metrics, index=12)
    st.session_state.metrics = st.multiselect('Metrics', list_metrics, default='GIH WR')

#st.session_state.filename_db = st.selectbox('select file', filenames_db)

#st.session_state.filter = st.text_input(label='Filter', value='')
col1, col2 = st.columns(2)
with col1:
    st.button('Answer', on_click=callback_answer, use_container_width=True)
    st.markdown('' + st.session_state.answerA)
    st.image(st.session_state.imA)

with col2:
    st.button('Next', on_click=callback_next, use_container_width=True)
    st.markdown('' + st.session_state.answerB)
    st.image(st.session_state.imB)


