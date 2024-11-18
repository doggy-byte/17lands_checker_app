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

set_name = 'DSK'
metrics = 'GIH WR'

list_metrics = [
    "# Seen",
    "ALSA",
    "# Picked",
    "ATA",
    "# GP",
    "%% GP",
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
    st.session_state.set_mquiz = 'FDN'

if 'format_mquiz' not in st.session_state:
    st.session_state.format_mquiz = 'PremierDraft'

if 'color_mquiz'not in st.session_state:
    st.session_state.color_mquiz = 'All'

if 'metrics' not in st.session_state:
    st.session_state.metrics = 'GIH WR'

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
        df_sample = df_filtered[df_filtered[st.session_state.metrics].notnull()].sample(2).reset_index()
    else:
        df_sample = df[(df[st.session_state.metrics].notnull())&(df['GIH WR'].notnull())].sample(2).reset_index()

    st.session_state.nameA = df_sample['Name'][0]
    st.session_state.nameB = df_sample['Name'][1]
    #st.session_state.qnameA = st.session_state.nameA.replace('//', '').replace(' ', '+')
    #st.session_state.qnameB = st.session_state.nameB.replace('//', '').replace(' ', '+')
    st.session_state.metricsA = df_sample[st.session_state.metrics][0]
    st.session_state.metricsB = df_sample[st.session_state.metrics][1]
    #st.session_state.imA = Image.open('card_images/{}/{}.png'.format(set_name, st.session_state.qnameA))
    #st.session_state.imB = Image.open("card_images/{}/{}.png".format(set_name, st.session_state.qnameB))
    st.session_state.imA = open_or_download_image(st.session_state.nameA)
    st.session_state.imB = open_or_download_image(st.session_state.nameB)
    st.session_state.answerA = '{}=____'.format(st.session_state.metrics)
    st.session_state.answerB = '{}=____'.format(st.session_state.metrics)

def callback_answer():
    st.session_state.answerA = '{}={}'.format(st.session_state.metrics, st.session_state.metricsA)
    st.session_state.answerB = '{}={}'.format(st.session_state.metrics, st.session_state.metricsB)

if not 'nameA' in st.session_state.keys():
    callback_next()

st.title("Which is stronger?")

fil1, fil2, fil3, fil4 = st.columns(4)
with fil1:
    st.session_state.set_mquiz = st.selectbox('Set', ['DSK', 'FDN'])
with fil2:
    st.session_state.format_mquiz = st.selectbox('Format', ['PremierDraft'])
with fil3:
    st.session_state.color_mquiz = st.selectbox('Color', ['All', 'WU', 'WB', 'WR', 'WG', 'UB', 'UR', 'UG', 'BR', 'BG', 'RG'])
with fil4:
    st.session_state.metrics = st.selectbox('Metrics', list_metrics, index=12)

#st.session_state.filename_db = st.selectbox('select file', filenames_db)

#st.session_state.filter = st.text_input(label='Filter', value='')
col1, col2 = st.columns(2)
with col1:
    st.button('Answer', on_click=callback_answer, use_container_width=True)
    st.markdown('### ' + st.session_state.answerA)
    st.image(st.session_state.imA)

with col2:
    st.button('Next', on_click=callback_next, use_container_width=True)
    st.markdown('### ' + st.session_state.answerB)
    st.image(st.session_state.imB)


