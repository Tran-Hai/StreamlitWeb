import pandas as pd
import json
import streamlit as st
import subprocess

@st.cache_data(show_spinner=False)
def crawl_data(start_date, end_date):
    res = subprocess.run(["node", "scripts/Crawler.js", start_date, end_date], capture_output=True, text=True, encoding='utf-8')
    if res.returncode != 0:
        st.error("Error when crawling data")
        st.stop()
    return res.stdout



def process_data(data):
    data_json = json.loads(data)
    df = pd.DataFrame(data_json)

    columns_name = ['STT','Trạng thái', 'Số chỉ thị', 'Line', 'Tên thiết bị', 'Số quản lí thiết bị', 'Loại công trình',
                    'PP bảo dưỡng', 'Vùng thao tác', 'LK đồng bộ', 'LK không thể tháo rời', 'Mã xử lí', 'Hiện tượng',
                    'Nguyên nhân', 'Nguyên nhân gốc']
    
    df.columns = columns_name

    return df