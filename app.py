import streamlit as st
import plotly.express as px
import pandas as pd
import os
import warnings
warnings.filterwarnings('ignore')

st.set_page_config(page_title='Brazilian e-commerce',page_icon=':bar_chart:', layout='wide')
st.title(' :bar_chart: Where Should We Grow? Olist Sales & delivery insights')

@st.cache_data
def load_data():
    sales = pd.read_csv('data/processed/sales.csv')
    orders_status = pd.read_csv('data/processed/orders_status.csv')
    sales['purchase_at'] = pd.to_datetime(sales['purchase_at'])
    orders_status['purchase_at'] = pd.to_datetime(orders_status['purchase_at'])
    return sales, orders_status

sales, orders_status = load_data()
col1, col2 = st.columns((2))

startDate = pd.to_datetime(sales['purchase_at']).min()
endDate = pd.to_datetime(sales['purchase_at']).max()

with col1:
    date1 = pd.to_datetime(st.date_input('Start Date', startDate))

with col2:
    date2 = pd.to_datetime(st.date_input('End Date', endDate))

df = sales[(sales['purchase_at'] >=date1) & (sales['purchase_at'] <= date2)].copy()
st.sidebar.header('Choose you filter: ')
state = st.sidebar.multiselect('Pick your State', df['customer_state'].unique())
if not state:
    df2 = df.copy()
else:
    df2 = df[df['customer_state'].isin(state)]

city = st.sidebar.multiselect('Pick the City', df2['customer_city'].unique())

if not state and not city:
    filtered_df = df
elif not city:
    filtered_df = df[df['customer_state'].isin(state)]
elif not state:
    filtered_df = df[df['customer_city'].isin(city)]
else:
    filtered_df = df2[df['customer_state'].isin(state) & df['customer_city'].isin(city)]

delivered = filtered_df['order_status'] == 'delivered'
total_revenue = filtered_df[delivered]['revenue'].sum()
orders = filtered_df[delivered]['order_id'].nunique()

if not orders:
    AOV = '-'
else:
    AOV = (f'R$ {total_revenue/orders:,.2f}')
total_customers = filtered_df[delivered]['customer_unique_id'].nunique()


k1, k2, k3, k4 = st.columns(4)
k1.metric('Revenue', f'R$ {total_revenue:,.0f}')
k2.metric('Orders', f'{orders:,}')
k3.metric('AOV', AOV)
k4.metric('Customers', f'{total_customers:,}')


category_df = filtered_df[delivered].groupby(by= ['category'], as_index = False)['revenue'].sum()

with col1:
    st.subheader('Category wise Sales')
    