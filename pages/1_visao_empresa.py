import pandas as pd
import streamlit as st
from streamlit_folium import folium_static
from utils import clean_data, orders_by_day, orders_by_traffic, orders_density_by_traffic, orders_by_week, orders_by_deliver_week, orders_distribution, print_figure, sidebar

st.set_page_config(page_title='Empresa',
                   page_icon='✊',
                   layout='wide')

data = pd.read_csv('dataset/train.csv')
df = clean_data(data)
del(data)

# =============================
# Barra lateral
# =============================
date_slider, traffic_options = sidebar(df)
df = df.loc[df['Order_Date'] <= date_slider, :]
df = df.loc[df['Road_traffic_density'].isin(traffic_options), :]

# =============================
# Layout do streamlit
# =============================
tab1, tab2, tab3 = st.tabs(['Visão Gerencial', 'Visão Tática', 'Visão Geográfica'])

with tab1:
    with st.container():
        print_figure('Orders by day', orders_by_day(df))
    with st.container():
        col1, col2 = st.columns(2)    
        with col1:
            print_figure('Orders by traffic', orders_by_traffic(df))
        with col2:
            print_figure('Orders density by traffic density', orders_density_by_traffic(df))
    
with tab2:
    print_figure('Orders by week', orders_by_week(df))
    print_figure('Orders by deliver and week', orders_by_deliver_week(df))

with tab3:
    st.header('Orders distribution')
    map = orders_distribution(df)
    folium_static(map)