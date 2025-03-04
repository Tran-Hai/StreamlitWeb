import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import streamlit as st
import pandas as pd
from data.DataProcessor import crawl_data, process_data
from visualization.charts import create_pie_chart, create_bar_chart
from utils.constants import ma_nguyen_nhan, ma_nguyen_nhan_goc, ma_hien_tuong
import warnings
warnings.filterwarnings('ignore')


st.set_page_config(page_title='Data Visualization', layout='wide')


st.title(':bar_chart: Data Visualization')
st.markdown('<style>div.block-container{padding-top:1rem;}</style>',unsafe_allow_html=True)


col1, col2 = st.columns((2))

# Getting the min and max date
startDate = pd.to_datetime('today').replace(day=1)
endDate = pd.to_datetime('today')


with col1:
    date1 = pd.to_datetime(st.date_input('Start Date', startDate))

with col2:
    date2 = pd.to_datetime(st.date_input('End Date', endDate))

date1 = date1.strftime('%d-%m-%Y')
date2 = date2.strftime('%d-%m-%Y')


# Fetch and process data
json_data = crawl_data(date1, date2)
df = process_data(json_data)


# Create sidebar for Line
st.sidebar.header("Choose your filter:")
line = st.sidebar.multiselect("Pick your line", df['Line'].unique())

if not line:
    df2 = df.copy()
else:
    df2 = df[df['Line'].isin(line)]


# Create charts
with col1:
    figure_nguyen_nhan = create_pie_chart(df2, 'Nguyên nhân', ma_nguyen_nhan, 'Nguyên nhân')
    st.plotly_chart(figure_nguyen_nhan, use_container_width=True)

with col2:
    fig_nguyen_nhan_goc = create_pie_chart(df2, 'Nguyên nhân gốc', ma_nguyen_nhan_goc, 'Nguyên nhân gốc')
    st.plotly_chart(fig_nguyen_nhan_goc, use_container_width=True)



cl1, cl2 = st.columns((2))

with cl1:
    with st.expander("View Data"):
        st.write(df2['Nguyên nhân'].value_counts())
        csv = df2['Nguyên nhân'].value_counts().to_csv(index=True).encode('utf-8')
        st.download_button('Download Data', data=csv, file_name='Nguyen nhan.csv', mime='text/csv', help='Click here to download the data as a CSV file')

with cl2:
    with st.expander("View Data"):
        st.write(df2['Nguyên nhân gốc'].value_counts())
        csv = df2['Nguyên nhân gốc'].value_counts().to_csv(index=True).encode('utf-8')
        st.download_button('Download Data', data=csv, file_name='Nguyen nhan goc.csv', mime='text/csv', help='Click here to download the data as a CSV file')




figure_hien_tuong = create_bar_chart(df2, 'Hiện tượng', ma_hien_tuong, 'Hiện tượng')
st.plotly_chart(figure_hien_tuong, use_container_width=True)

with st.expander('View Data'):
    st.write(df2['Hiện tượng'].value_counts())
    csv2 = df2['Hiện tượng'].value_counts().to_csv(index=True).encode('utf-8')
    st.download_button('Download Data', data=csv2, file_name='HienTuong.csv', mime='text/csv', help='Click here to download the data as a CSV file')
