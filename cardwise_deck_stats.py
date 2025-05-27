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
    'cardname':'CardName',
    'cardname_jp':'CardNameJP',
    'cardColor':'CardColor',
    'rarity':'CardRarity',
    'deckbuild_id':'Decks',
    'main_colors':'1stMainColor',
    'second_main_colors':'2ndMainColor',
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
    'isNonbasicLand':'#NonbasicLand',
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
    'CardName',
    'CardNameJP',
    'Decks', 
    '1stMainColor',
    '2ndMainColor',
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
    '#NonbasicLand',
    '#Common',
    '#Uncommon',
    '#RareMythic',
    'KillTurns'
]

def callback_all():
    callback_load_data()
    callback_change_view()

def callback_load_data():
    df = open_or_download_db(st.secrets[st.session_state.set_cardstats][st.session_state.format_cardstats]['cardwise'])
    df['cardColor'].fillna('Colorless', inplace=True)
    df = df.rename(columns = d_rename)
    st.session_state.df_cardstats = df
    st.session_state.metrics_cardstats = [x for x in st.session_state.metrics_cardstats if x in list(df.columns)]
    st.session_state.list_columns_cardstats = list(df.columns)

def callback_change_view():
    df_view = st.session_state.df_cardstats.copy()

    df_view = df_view[(df_view['CardRarity'].isin(st.session_state.rarity_cardstats))&\
                    (df_view['CardColor'].isin(st.session_state.color_cardstats))&\
                    (df_view['Decks']>=st.session_state.mingame_cardstats)]
    if st.session_state.cardname_cardstats is not None and len(st.session_state.cardname_cardstats) > 0:
        df_view = df_view[(df_view['CardName'].str.contains(st.session_state.cardname_cardstats, case=False))|(df_view['CardNameJP'].str.contains(st.session_state.cardname_cardstats, case=False))]
    df_view = df_view[st.session_state.metrics_cardstats]
    st.session_state.df_view_cardstats = df_view

df_metdef = open_or_download_db('metrics_definitions.csv')

if 'set_cardstats' not in st.session_state:
    st.session_state.set_cardstats = st.secrets['sets_cardstats'][0]

if 'format_cardstats' not in st.session_state:
    st.session_state.format_cardstats = 'PremierDraft'

if 'wins_cardstats' not in st.session_state:
    st.session_state.wins_cardstats = 'Platinum+ Rank & 3+ Wins'

if 'mingame_cardstats' not in st.session_state:
    st.session_state.mingame_cardstats = 100

if 'metrics_cardstats' not in st.session_state:
    st.session_state.metrics_cardstats = initial_columns

if 'df_cardstats' not in st.session_state:
    callback_load_data()

if 'rarity_cardstats' not in st.session_state:
    st.session_state.rarity_cardstats = list(st.session_state.df_cardstats['CardRarity'].unique())

if 'color_cardstats' not in st.session_state:
    st.session_state.color_cardstats = list(st.session_state.df_cardstats['CardColor'].unique())

if 'cardname_cardstats' not in st.session_state:
    st.session_state.cardname_cardstats = ''

if 'metrics_cardstats' not in st.session_state:
    st.session_state.metrics_cardstats = st.session_state.list_columns_cardstats

if 'df_cardstats' not in st.session_state:
    callback_load_data()

if 'df_view_cardstats' not in st.session_state:
    callback_change_view()

st.title("Card-wise Deck Stats")

st.markdown("Data was aggregated from [17Lands public dataset](https://www.17lands.com/public_datasets).")

fil1, fil2, fil3 = st.columns(3)
with fil1:
    st.selectbox('Set', st.secrets['sets_cardstats'], index=0, on_change=callback_all, key='set_cardstats')
with fil2:
    st.selectbox('Format', ['PremierDraft'], index=0, on_change=callback_all, key='format_cardstats')
with fil3:
    st.selectbox('Threshold', ['Platinum+ Rank & 3+ Wins'], index=0, on_change=callback_all, key='wins_cardstats')

with st.expander('Filters'):
    fil4, fil5, fil6 = st.columns(3)
    with fil4:
        st.selectbox('Minimum Decks', [1, 100, 500, 1000], index=1, on_change=callback_change_view, key='mingame_cardstats')
    with fil5:
        st.multiselect('Rarity', ['common', 'uncommon', 'rare', 'mythic'], ['common', 'uncommon', 'rare', 'mythic'], 
                    on_change=callback_change_view, key='rarity_cardstats')
    with fil6:
        st.multiselect('Color', ['W', 'U', 'B', 'R', 'G', 'Multicolor', 'Colorless'], ['W', 'U', 'B', 'R', 'G', 'Multicolor', 'Colorless'], 
                    on_change=callback_change_view, key='color_cardstats')

    st.text_input('Name', on_change=callback_change_view, key='cardname_cardstats')
    st.multiselect('Metrics', st.session_state.list_columns_cardstats, default=[x for x in initial_columns if x in st.session_state.df_view_cardstats], 
                on_change=callback_change_view, key='metrics_cardstats')

with st.expander('Metrics Definitions'):
    st.markdown('- カード枚数に関する統計はそのカード自体を含みます。')
    st.markdown('- ゲーム展開に関する統計はそのカードを引かなかった・プレイしなかったゲームも含みます。')
    st.dataframe(df_metdef)

gb = GridOptionsBuilder.from_dataframe(st.session_state.df_view_cardstats)
gb.configure_columns([x for x in st.session_state.df_view_cardstats.columns if st.session_state.df_view_cardstats[x].dtype==np.float64], 
    type=["numericColumn", "customNumericFormat"], precision=1)
gb.configure_column("CardName", pinned="left")
gb.configure_column("CardNameJP", pinned="left")

gridOptions = gb.build()

AgGrid(st.session_state.df_view_cardstats, 
       gridOptions=gridOptions,
       columns_auto_size_mode=ColumnsAutoSizeMode.FIT_CONTENTS)



