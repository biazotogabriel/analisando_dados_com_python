import pandas as pd
import streamlit as st
from haversine import haversine
from utils import clean_data, print_figure, print_dataframe, sidebar, mean_std_by_city, mean_std_by_type_order, mean_std_by_city_type_traffic

st.set_page_config(page_title='Restaurantes',
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
st.header('Marketplace - Visão Restaurantes')
tab1, tab2, tab3 = st.tabs(['Visão Gerencial', '_', '_'])
with tab1:
    with st.container():
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            col1.metric('Quantidade de entrgadores', len(df['Delivery_person_ID'].unique()))
        with col2:
            def get_distance(row):
                return haversine((row['Restaurant_latitude'],row['Restaurant_longitude']),
                                 (row['Delivery_location_latitude'], row['Delivery_location_longitude']),
                                 'km')
            df['distance'] = df.apply(get_distance, axis=1)
            col2.metric('Metric', '%.2f' % df['distance'].mean())
        with col3:
            avg_time = df.loc[df['Festival'] == 'Yes', 'Time_taken(min)'].mean()
            col3.metric('Tempo médio em festivais', '%.2f' % avg_time)
        with col4:
            avg_time = df.loc[df['Festival'] == 'No', 'Time_taken(min)'].mean()
            col4.metric('Tempo médio fora de festivais', '%.2f' % avg_time)
    st.markdown("""---""")
    print_dataframe('### Tempo médio e desvio padrão de entrega por cidade', mean_std_by_city(df))

    with st.container():
        col1, col2 = st.columns(2)
        with col1:
            print_dataframe('### Tempo médio e desvio padrão de entrega por cidade e tipo de pedido',
                            mean_std_by_type_order(df))
        with col2:
            print_dataframe('### Tempo médio e desvio padrão de entrega por cidade e tipo de tráfego',
                            mean_std_by_city_type_traffic(df))