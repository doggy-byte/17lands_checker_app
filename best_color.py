import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import streamlit as st
import json
from common_functions import open_or_download_image, open_or_download_db


colors = ['WU', 'WB', 'WR', 'WG', 'UB', 'UR', 'UG', 'BR', 'BG', 'RG']
dfs = {}

for c in colors:
    df_tmp = open_or_download_db(st.secrets['best_color']['filename_base'].format(c))
    df_tmp = df_tmp[['Name', 'GIH WR', 'IWD']]
    df_tmp.columns = ['Name', 'GIHWR_{}'.format(c), 'IWD_{}'.format(c)]
    dfs[c] = df_tmp

df_join = None
for c in colors:
    if df_join is None:
        df_join = dfs[c].copy()
        continue
    df_join = pd.merge(df_join, dfs[c], on='Name', how='left')

df_join.dropna(subset=['GIHWR_{}'.format(c) for c in colors], inplace=True, how='all')

with open(st.secrets['best_color']['color_winrate']) as f:
    d_color_winrate = json.load(f)

list_color_winrate = [d_color_winrate[x] for x in colors]

if 'fig' not in st.session_state:
    st.session_state.fig, st.session_state.ax = plt.subplots()

def callback_next():
    df_sample = df_join.sample(1).reset_index()

    st.session_state.cardname = df_sample['Name'][0]
    st.session_state.GIHWR_list = df_sample[['GIHWR_{}'.format(c) for c in colors]].iloc[0]
    st.session_state.GIHWR_list_num = [np.float64(x[0:-1]) if type(x) is str else 0.0 for x in st.session_state.GIHWR_list]
    st.session_state.GIHWR_list_np = np.array(st.session_state.GIHWR_list_num)
    st.session_state.im = open_or_download_image(st.session_state.cardname)
    st.session_state.ax.clear()
    st.session_state.ax.plot(list_color_winrate, marker='*', linestyle='None', color='#FF5555')
    st.session_state.ax.legend(['Deck color winrate'])
    st.session_state.ax.set_ylim([40, 70])
    st.session_state.ax.set_xlabel('Deck color')
    st.session_state.ax.set_ylabel('Winrate')
    st.session_state.ax.set_xticks([x for x in range(0, 10)])
    st.session_state.ax.set_xticklabels(colors)
    st.session_state.ax.grid(axis='y')

def callback_answer():
    st.session_state.ax.clear()
    bar_colors = ['#6688EE'] * 10
    bar_colors[np.argmax(st.session_state.GIHWR_list_np)] = "#3333FF"
    st.session_state.ax.bar(height=st.session_state.GIHWR_list_np, x=colors, color=bar_colors)
    st.session_state.ax.plot(list_color_winrate, marker='*', linestyle='None', color='#FF5555')
    st.session_state.ax.legend(['Deck color winrate', 'Card GIH WR'])
    st.session_state.ax.set_ylim([40, 70])
    st.session_state.ax.set_xlabel('Deck color')
    st.session_state.ax.set_ylabel('Winrate')
    st.session_state.ax.grid(axis='y')

if not 'cardname' in st.session_state.keys():
    callback_next()


st.title('Best deck color')
col1, col2 = st.columns([1, 2])

with col1:
    st.button('Answer', on_click=callback_answer, use_container_width=True)
    st.image(st.session_state.im)
with col2:
    st.button('Next', on_click=callback_next, use_container_width=True)
    st.pyplot(st.session_state.fig)





