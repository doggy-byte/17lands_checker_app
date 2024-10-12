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

filenames_db = [
    "DSK_PremierDraft_All_20241011.csv",
    "DSK_PremierDraft_WU_20241011.csv",
    "DSK_PremierDraft_WB_20241011.csv",
    "DSK_PremierDraft_WR_20241011.csv",
    "DSK_PremierDraft_WG_20241011.csv",
    "DSK_PremierDraft_UB_20241011.csv",
    "DSK_PremierDraft_UR_20241011.csv",
    "DSK_PremierDraft_UG_20241011.csv",
    "DSK_PremierDraft_BR_20241011.csv",
    "DSK_PremierDraft_BG_20241011.csv",
    "DSK_PremierDraft_RG_20241011.csv"
]

st.session_state.filter = ''

set_name = 'DSK'
metrics = 'GIH WR'

if 'filter' not in st.session_state:
    st.session_state.filter = ''

def callback_next():
    if 'filename_db' not in st.session_state:
        df = open_or_download_db(filenames_db[0])
    else:
        df = open_or_download_db(st.session_state.filename_db)

    if len(st.session_state.filter) > 0:
        df_filtered = df.query(st.session_state.filter)
        df_sample = df_filtered[df_filtered['GIH WR'].notnull()].sample(2).reset_index()
    else:
        df_sample = df[df['GIH WR'].notnull()].sample(2).reset_index()

    st.session_state.nameA = df_sample['Name'][0]
    st.session_state.nameB = df_sample['Name'][1]
    #st.session_state.qnameA = st.session_state.nameA.replace('//', '').replace(' ', '+')
    #st.session_state.qnameB = st.session_state.nameB.replace('//', '').replace(' ', '+')
    st.session_state.metricsA = df_sample[metrics][0]
    st.session_state.metricsB = df_sample[metrics][1]
    #st.session_state.imA = Image.open('card_images/{}/{}.png'.format(set_name, st.session_state.qnameA))
    #st.session_state.imB = Image.open("card_images/{}/{}.png".format(set_name, st.session_state.qnameB))
    st.session_state.imA = open_or_download_image(st.session_state.nameA)
    st.session_state.imB = open_or_download_image(st.session_state.nameB)
    st.session_state.answerA = 'GIHWR=____'
    st.session_state.answerB = 'GIHWR=____'

def callback_answer():
    st.session_state.answerA = 'GIHWR={}'.format(st.session_state.metricsA)
    st.session_state.answerB = 'GIHWR={}'.format(st.session_state.metricsB)

if not 'nameA' in st.session_state.keys():
    callback_next()

st.title("Which is stronger?")
st.session_state.filename_db = st.selectbox('select file', filenames_db)
#st.session_state.filter = st.text_input(label='Filter', value='')
col1, col2 = st.columns(2)
with col1:
    st.markdown('### ' + st.session_state.answerA)
    st.button('Answer', on_click=callback_answer, use_container_width=True)
    st.image(st.session_state.imA)

with col2:
    st.markdown('### ' + st.session_state.answerB)
    st.button('Next', on_click=callback_next, use_container_width=True)
    st.image(st.session_state.imB)


