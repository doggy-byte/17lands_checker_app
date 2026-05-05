import os.path as osp
import os
import json
import time
import requests
from PIL import Image
import streamlit as st
from st_files_connection import FilesConnection
import pandas as pd
from io import BytesIO


def download_gcs_folder(bucket_name, gcs_folder_path, local_dir):
    """
    GCS上の特定のフォルダ（prefix）配下の全ファイルをダウンロードする
    """
    # 1. GCS Connectionの初期化
    conn = st.connection('gcs', type=FilesConnection)
    
    # 2. ローカルの保存先ディレクトリを作成
    if not os.path.exists(local_dir):
        os.makedirs(local_dir)
    
    # 3. 指定したフォルダ内のファイル一覧を取得
    # 注意: list_objects(path) は指定パスで始まるファイルをリストします
    full_gcs_path = f"{bucket_name}/{gcs_folder_path}"
    files = conn.fs.ls(full_gcs_path)
    
    downloaded_files = []
    
    for file_path in files:
        # ディレクトリ自体を除外（GCS上の空のディレクトリなど）
        if conn.fs.isdir(file_path):
            continue
            
        file_name = os.path.basename(file_path)
        local_file_path = os.path.join(local_dir, file_name)
        
        # 4. ファイルを読み込んでローカルに書き出し
        with conn.open(file_path, "rb") as f:
            content = f.read()
            with open(local_file_path, "wb") as local_f:
                local_f.write(content)
        
        downloaded_files.append(local_file_path)
    
    return downloaded_files


def get_card_data_ja(cardname):
    base_url = "https://api.scryfall.com/cards/named?fuzzy={}"
    
    response = requests.get(base_url.format(cardname))
    
    if not response.ok:
        print('EN response not OK')
        return None
    
    en_data = response.json()
    oracle_id = en_data.get('oracle_id')
    
    # API負荷軽減のための待機 (Scryfallの推奨ルール)
    time.sleep(0.1)
    
    search_url = "https://api.scryfall.com/cards/search"
    search_params = {
        'q': f'oracleid:{oracle_id} lang:ja',
        'order': 'released',
        'unique': 'cards' 
    }
    
    ja_res = requests.get(search_url, params=search_params)
    
    if ja_res.ok:
        ja_search_result = ja_res.json()
        return ja_search_result['data'][0]
    else:
        print('JA response not OK')
        return None


def open_or_download_image(cardname: str, lang='ja'):
    os.makedirs('card_images', exist_ok=True)
    os.makedirs('card_images_ja', exist_ok=True)

    write_flg = True

    #fname = cardname.replace('/', '_').replace(' ', '+').replace('&', '+').replace(',', '')
    qname = cardname.split(' // ')[0].replace('/', '').replace(' ', '+').replace('&', '+').replace(',', '')

    if lang == 'en':
        file_path = 'card_images/' + qname + '.png'
    if lang == 'ja':
        file_path = 'card_images_ja/' + qname + '.png'
    
    if osp.exists(file_path):
        return Image.open(file_path)
    
    if lang == 'en':
        d = json.loads(requests.get('https://api.scryfall.com/cards/named?fuzzy={}'.format(qname)).text)
    if lang == 'ja':
        d = get_card_data_ja(qname)
        if d is None:
            d = json.loads(requests.get('https://api.scryfall.com/cards/named?fuzzy={}'.format(qname)).text)
            write_flg = False

    time.sleep(0.1)

    if d is None:
        return None

    if 'layout' in d.keys() and d['layout'] == 'transform':
        d = d['card_faces'][0]

    if 'image_uris' not in d.keys():
        return None

    image_uri = d['image_uris']['border_crop']
    im = requests.get(image_uri)

    if not im.ok:
        return None

    if write_flg:
        with open(file_path, 'wb') as f:
            f.write(im.content)
        
    return Image.open(BytesIO(im.content))


def open_or_download_db(filename, force_download=False):
    os.makedirs('dashboard_data', exist_ok=True)

    file_path = 'dashboard_data/' + filename
    
    if osp.exists(file_path) and not force_download:
        return pd.read_csv(file_path)
        
    conn = st.connection('gcs', type=FilesConnection)
    #df = conn.read("streamlit-17lands-checker-app/{}".format(filename), input_format="csv", ttl=600)
    #df.to_csv(file_path, index=None)
    #return df
    try:
        df = conn.read("streamlit-17lands-checker-app/{}".format(filename), input_format="csv", ttl=600)
        df.to_csv(file_path, index=None)
        return df
    except Exception as e:
        print("Failed open_or_download_db: {}".format(filename))
        return None


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