import os.path as osp
import os
import json
import requests
from PIL import Image
import streamlit as st
from st_files_connection import FilesConnection
import pandas as pd


def open_or_download_image(cardname):
    os.makedirs('card_images', exist_ok=True)

    qname = cardname.replace('/', '_').replace(' ', '+')
    
    file_path = 'card_images/' + qname + '.png'
    
    if osp.exists(file_path):
        return Image.open(file_path)
        
    d = json.loads(requests.get('https://api.scryfall.com/cards/named?fuzzy={}'.format(qname)).text)

    image_uri = d['image_uris']['border_crop']
    im = requests.get(image_uri)
    with open(file_path, 'wb') as f:
        f.write(im.content)
        
    return Image.open(file_path)


def open_or_download_db(filename):
    os.makedirs('dashboard_data', exist_ok=True)

    file_path = 'dashboard_data/' + filename
    
    if osp.exists(file_path):
        return pd.read_csv(file_path)
        
    conn = st.connection('gcs', type=FilesConnection)
    df = conn.read("streamlit-17lands-checker-app/{}".format(filename), input_format="csv", ttl=600)
    
    df.to_csv(file_path, index=None)
        
    return df


def open_or_download_json(filename):
    os.makedirs('dashboard_data', exist_ok=True)

    file_path = 'dashboard_data/' + filename
    
    if osp.exists(file_path):
        with open(file_path, 'r') as f:
            return json.load(f)
        
    conn = st.connection('gcs', type=FilesConnection)
    j = conn.read("streamlit-17lands-checker-app/{}".format(filename), input_format="json", ttl=600)
    
    with open(file_path, 'w') as f:
        json.dump(j, f)
        
    return j