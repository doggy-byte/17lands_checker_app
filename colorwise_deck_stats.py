import streamlit as st
from st_aggrid import AgGrid, GridOptionsBuilder, ColumnsAutoSizeMode, JsCode, GridUpdateMode
import pandas as pd
import numpy as np
from PIL import Image
from pathlib import Path
from common_functions import open_or_download_image, open_or_download_db
pd.options.display.float_format = '{:.1f}'.format

st.markdown("""
        <style>
               .block-container {
                    padding-top: 1rem;
                    padding-bottom: 1rem;
                    padding-left: 1rem;
                    padding-right: 1rem;
                    margin-left: 1rem;
                    margin-right: 1rem;
                }
        </style>
        """, unsafe_allow_html=True)

d_rename = {
    'main_colors':'MainColor',
    'deckbuild_id':'Decks',
    'num_turns':'Turns',
    'kill_turns':'KillTurns',
    'on_play':'%OnPlay',
    'num_mulligans':'Mulligans',
    'color_count':'#Color',
    'avgMV':'AvgMV',
    'maxMV':'MaxMV',
    'isCard':'#Cards',
    'isCommon':'#Common',
    'isUncommon':'#Uncommon',
    'isRare':'#Rare',
    'isMythic':'#Mythic',
    'isRM':'#RareMythic',
    'isCreature':'#Creature',
    'isLightCreature':'#Creature_MV<=2',
    'isHeavyCreature':'#Creature_MV>=5',
    'isNonCreature':'#NonCreature',
    'isArtifact':'#Artifact',
    'isInstant':'#Instant',
    'isSorcery':'#Sorcery',
    'isInSor':'#InstantSorcery',
    'isEnchantment':'#Enchantment',
    'isLand':'#Land',
    'cntWhite':'#White',
    'cntBlue':'#Blue',
    'cntBlack':'#Black',
    'cntRed':'#Red',
    'cntGreen':'#Green',
    'cntMulticolor':'#Multicolor',
    'cntColorless':'#Colorless',
    'includeWhite':'%IncludeWhite',
    'includeBlue':'%IncludeBlue',
    'includeBlack':'%IncludeBlack',
    'includeRed':'%IncludeRed',
    'includeGreen':'%IncludeGreen',
    'includeMulticolor':'%IncludeMulticolor',
    'includeColorless':'%IncludeColorless'
}

initial_columns = [
    'MainColor',
    'Decks', 
    'AvgMV',
    'MaxMV',
    '#Creature',
    '#Creature_MV<=2',
    '#Creature_MV>=5',
    '#NonCreature',
    '#Artifact',
    '#InstantSorcery',
    '#Enchantment',
    '#Land',
    '#Common',
    '#Uncommon',
    '#RareMythic',
    'KillTurns'
]

def callback_all():
    callback_load_data()
    callback_change_view()

def callback_load_data():
    df = open_or_download_db(st.secrets[st.session_state.set_colorstats][st.session_state.format_colorstats]['colorwise'])
    df = df.rename(columns = d_rename)
    st.session_state.df_colorstats = df
    st.session_state.metrics_colorstats = [x for x in st.session_state.metrics_colorstats if x in list(df.columns)]
    st.session_state.list_columns_colorstats = list(df.columns)

def callback_change_view():
    df_view = st.session_state.df_colorstats.copy()

    df_view = df_view[df_view['Decks']>=st.session_state.mingame_colorstats]
    df_view = df_view[st.session_state.metrics_colorstats]
    st.session_state.df_view_colorstats = df_view

df_metdef = open_or_download_db('metrics_definitions.csv')

if 'set_colorstats' not in st.session_state:
    st.session_state.set_colorstats = st.secrets['sets_colorstats'][0]

if 'format_colorstats' not in st.session_state:
    st.session_state.format_colorstats = 'PremierDraft'

if 'wins_colorstats' not in st.session_state:
    st.session_state.wins_colorstats = 'Platinum+ Rank & 3+ Wins'

if 'mingame_colorstats' not in st.session_state:
    st.session_state.mingame_colorstats = 100

if 'metrics_colorstats' not in st.session_state:
    st.session_state.metrics_colorstats = initial_columns

if 'df_colorstats' not in st.session_state:
    callback_load_data()

if 'metrics_colorstats' not in st.session_state:
    st.session_state.metrics_colorstats = st.session_state.list_columns_colorstats

if 'df_colorstats' not in st.session_state:
    callback_load_data()

if 'df_view_colorstats' not in st.session_state:
    callback_change_view()

st.title("Color-wise Deck Stats")

st.markdown("Data was aggregated from [17Lands public dataset](https://www.17lands.com/public_datasets).")

fil1, fil2, fil3 = st.columns(3)
with st.expander('Filters'):
    with fil1:
        st.selectbox('Set', st.secrets['sets_colorstats'], index=0, on_change=callback_all, key='set_colorstats')
    with fil2:
        st.selectbox('Format', ['PremierDraft'], index=0, on_change=callback_all, key='format_colorstats')
    with fil3:
        st.selectbox('Threshold', ['Platinum+ Rank & 3+ Wins'], index=0, on_change=callback_all, key='wins_colorstats')
    fil4, fil5, fil6 = st.columns(3)
    with fil4:
        st.selectbox('Minimum Decks', [1, 100, 500, 1000], index=1, on_change=callback_change_view, key='mingame_colorstats')
    st.multiselect('Metrics', st.session_state.list_columns_colorstats, default=initial_columns, 
                on_change=callback_change_view, key='metrics_colorstats')

with st.expander('Metrics Definitions'):
    st.dataframe(df_metdef)

gb = GridOptionsBuilder.from_dataframe(st.session_state.df_view_colorstats)
gb.configure_columns([x for x in st.session_state.df_view_colorstats.columns if st.session_state.df_view_colorstats[x].dtype==np.float64], 
    type=["numericColumn", "customNumericFormat"], precision=1)
gb.configure_column("MainColor", pinned="left")

gridOptions = gb.build()

AgGrid(st.session_state.df_view_colorstats, 
       gridOptions=gridOptions,
       columns_auto_size_mode=ColumnsAutoSizeMode.FIT_CONTENTS)




