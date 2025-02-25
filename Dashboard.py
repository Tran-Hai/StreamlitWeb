import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
from map.MaHienTuong import ma_hien_tuong
from map.MaLinhKien import ma_linh_kien
from map.MaNguyenNhan import ma_nguyen_nhan
from map.MaNguyenNhanGoc import ma_nguyen_nhan_goc

#from DataCrawler import crawl_data
import subprocess
import json
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


@st.cache_data(show_spinner=False)
def crawl_data(start_date, end_date):
    res = subprocess.run(["node", "DataCrawler.js", start_date, end_date], capture_output=True, text=True, encoding='utf-8')
    if res.returncode != 0:
        st.error("Error running DataCrawler.js")
        st.stop()
    return res.stdout

df = crawl_data(date1.strftime('%d-%m-%Y'), date2.strftime('%d-%m-%Y'))

try:
    data_json = json.loads(df)
except json.JSONDecodeError:
    st.error("Failed to decode JSON from DataCrawler.js")
    st.stop()

df = pd.DataFrame(data_json)

columns_name = ['STT','Trạng thái', 'Số chỉ thị', 'Line', 'Tên thiết bị', 'Số quản lí thiết bị', 'Loại công trình',
                    'PP bảo dưỡng', 'Vùng thao tác', 'LK đồng bộ', 'LK không thể tháo rời', 'Mã xử lí', 'Hiện tượng',
                    'Nguyên nhân', 'Nguyên nhân gốc']

df.columns = columns_name




# Create sidebar for Line
st.sidebar.header("Choose your filter:")
line = st.sidebar.multiselect("Pick your line", df['Line'].unique())

if not line:
    df2 = df.copy()
else:
    df2 = df[df['Line'].isin(line)]

nguyen_nhan_df = df2.groupby(by=['Nguyên nhân'], as_index=False)['Line'].count()
custom_label = nguyen_nhan_df['Nguyên nhân'].map(ma_nguyen_nhan)
nguyen_nhan_df['custom label'] = custom_label
with col1:
    total_value = nguyen_nhan_df['Line'].sum()
    fig = go.Figure(data=[go.Pie(
        labels = nguyen_nhan_df['custom label'],
        values = nguyen_nhan_df['Line'],
        textposition = 'inside',
        hoverinfo='label+value',
        textinfo='percent',
        hole = 0.33,
        direction = 'clockwise'
    )])
    fig.update_layout(
        title = 'Nguyên nhân',
        showlegend=False,
        annotations = [
            dict(
                x=1.0,
                y=1.05,
                xref = 'paper',
                yref = 'paper',
                text=f'Total: {total_value}',
                showarrow=False,
                font=dict(size=19),
                align='left',
            )
        ]
    )

    st.plotly_chart(fig, use_container_width=True)




nguyen_nhan_goc_df = df2.groupby(by=['Nguyên nhân gốc'], as_index=False)['Line'].count()
custom_label = nguyen_nhan_goc_df['Nguyên nhân gốc'].map(ma_nguyen_nhan_goc)
nguyen_nhan_goc_df['custom label'] = custom_label
with col2:
    total_value = nguyen_nhan_goc_df['Line'].sum()
    fig = go.Figure(data=[go.Pie(
        labels = nguyen_nhan_goc_df['custom label'],
        values = nguyen_nhan_goc_df['Line'],
        textposition = 'inside',
        hoverinfo='label+value',
        textinfo='percent',
        hole = 0.33,
        direction = 'clockwise'
    )])
    fig.update_layout(
        title = 'Nguyên nhân gốc',
        showlegend=False,
        annotations = [
            dict(
                x=1.0,
                y=1.05,
                xref = 'paper',
                yref = 'paper',
                text=f'Total: {total_value}',
                showarrow=False,
                font=dict(size=19),
                align='left',
            )
        ]
    )
    st.plotly_chart(fig, use_container_width=True)


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


hien_tuong_df = df2.groupby(by=['Hiện tượng'], as_index=False)['Line'].count()
hien_tuong_df = hien_tuong_df.sort_values(by='Line', ascending=True)
custom_label = hien_tuong_df['Hiện tượng'].map(ma_hien_tuong)
hien_tuong_df['custom label'] = custom_label
fig2 = px.bar(hien_tuong_df, x='custom label', y='Line', template='seaborn')
fig2.update_xaxes(showticklabels=False)
fig2.update_yaxes(showticklabels=False)
fig2.update_xaxes(title = 'Hiện tượng')
fig2.update_yaxes(title='')
fig2.update_traces(hovertemplate='%{x}<br>%{y}')
st.plotly_chart(fig2, use_container_width=True, height=300)

with st.expander('View Data'):
    st.write(df2['Hiện tượng'].value_counts())
    csv2 = df2['Hiện tượng'].value_counts().to_csv(index=True).encode('utf-8')
    st.download_button('Download Data', data=csv2, file_name='HienTuong.csv', mime='text/csv', help='Click here to download the data as a CSV file')
