import pandas as pd
import streamlit as st
from utils import clean_data, print_figure, print_dataframe, sidebar, mean_by_delivery, mean_by_traffic, mean_by_weather, top_slower_deliveries, top_faster_deliveries

st.set_page_config(page_title='Entregadores',
                   page_icon='✊',
                   layout='wide')

data = pd.read_csv('dataset/train.csv')
df = clean_data(data)
del(data)

data = pd.read_csv('dataset/train.csv')

# =============================
# Barra lateral
# =============================
date_slider, traffic_options = sidebar(df)
df = df.loc[df['Order_Date'] <= date_slider, :]
df = df.loc[df['Road_traffic_density'].isin(traffic_options), :]
# =============================
# Layout do streamlit
# =============================
st.header('Marketplace - Visão Entregadores')
tab1, tab2, tab3 = st.tabs(['Visão Gerencial', '_', '_'])
with tab1:
    with st.container():
        col1, col2, col3, col4 = st.columns(4, gap='large')
        with col1:
            col1.metric('Menor de idade', df['Delivery_person_Age'].min())        
        with col2:
            col2.metric('Maior de idade', df['Delivery_person_Age'].max())
        with col3:
            col3.metric('Pior condição de veiculo', df['Vehicle_condition'].min())
        with col4:
            col4.metric('Melhor condição de veiculo', df['Vehicle_condition'].max())
    with st.container():
        st.markdown("""---""")
        col1, col2 = st.columns(2)
        with col1:
            print_dataframe('##### Avaliação média por entregador', mean_by_delivery(df))
        with col2:
            print_dataframe('##### Avaliação média por trânsito', mean_by_traffic(df))            
            print_dataframe('##### Avaliação média por clima', mean_by_weather(df))
    with st.container():
        st.markdown("""---""")
        st.title('Velocidade de entrega')
        col1, col2 = st.columns(2)
        with col1:
            print_dataframe('##### Top entregadores mais lentos', top_slower_deliveries(df))
        with col2:
            print_dataframe('##### Top entregadores mais rápidos', top_faster_deliveries(df))