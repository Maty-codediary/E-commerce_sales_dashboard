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
    filtered_df = df2[df['customer_state'].isin(state) & df2['customer_city'].isin(city)]

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

chart1, chart2 = st.columns(2)

category_df = filtered_df[delivered].groupby(by= ['category'], as_index = False)['revenue'].sum().sort_values(by='revenue', ascending=False).head(10)

with chart1:
    st.subheader('Top 10 category by revenue')
    fig = px.bar(category_df, x= 'revenue', y='category' , text=['R${:,.0f}'.format(x) for x in category_df['revenue']],
                 template = 'seaborn')
    st.plotly_chart(fig, use_container_width=True, height= 400)

state_df = filtered_df[delivered].groupby(by= ['customer_state'], as_index = False)['revenue'].sum().sort_values(by='revenue', ascending=False)
top_5_state = state_df.head(5)
other_total = state_df.iloc[5:]['revenue'].sum()
other_row = pd.DataFrame({'customer_state': ['Other'], 'revenue': [other_total]})
pie_df= pd.concat([top_5_state, other_row])
with chart2:
    st.subheader('Top 5 States by Revenue')
    fig= px.pie(pie_df,values= 'revenue', names= 'customer_state', hole = 0.5)
    fig.update_traces(textinfo='percent+label', textposition= 'outside')
    st.plotly_chart(fig, use_container_width=True)

cl1, cl2 = st.columns(2)
with cl1:
    with st.expander('Category_ViewData'):
        st.write(category_df.style.background_gradient(cmap='Blues'))
        csv = category_df.to_csv(index= False).encode('utf-8')
        st.download_button('Download Data', data= csv, file_name='Category.csv', mime='text/csv',
                           help = 'Click here to download the data as a CSV file')

with cl2:
    with st.expander('State_ViewData'):
        st.write(pie_df.style.background_gradient(cmap='Oranges'))
        csv = pie_df.to_csv(index= False).encode('utf-8')
        st.download_button('Download Data', data= csv, file_name='State.csv', mime='text/csv',
                           help = 'Click here to download the data as a CSV file')