import pandas as pd
import numpy as np
import re
import plotly.express as px
import folium
import streamlit as st
from PIL import Image

def print_figure(title, figure):
    st.markdown(title)
    st.plotly_chart(figure, 
                    use_container_width=True)
    
def print_dataframe(title, dataframe):
    st.markdown(title)
    st.dataframe(dataframe)

def clean_data(data):
    """Esta função possui a responsabilidade de limpar o dataframe
    - Remoção dos espaços vazios
    - Remoção dos dados NaNs
    - Conversão dos dados
    """
    #Remove os espaços vazios das colunas tipo texto
    for column in data.columns:
        if data[column].dtype == 'object':
            data[column] = data[column].str.strip()
    #Remove as linhas con dados NaN
    with_nan = data['ID'] == None
    for column in data.columns:
        if data[column].dtype == 'object':
            with_nan = with_nan | (data[column] == 'NaN')
    df = data[np.invert(with_nan)].reset_index(drop=True).copy()
    del(with_nan)
    #Converte os tipos de dados
    df['Delivery_person_Age'] = df['Delivery_person_Age'].astype('int')
    df['multiple_deliveries'] = df['multiple_deliveries'].astype('int')
    df['Delivery_person_Ratings'] = df['Delivery_person_Ratings'].astype('float')
    df['Order_Date'] = pd.to_datetime(df['Order_Date'], format='%d-%m-%Y')
    def clean_time_taken(row):
        return re.search(r'\d+', row['Time_taken(min)']).group(0)
    df['Time_taken(min)'] = df.apply(clean_time_taken, axis=1)
    df['Time_taken(min)'] = df['Time_taken(min)'].astype('int')
    df['week_of_year'] = df['Order_Date'].dt.isocalendar().week
    return df

def sidebar(df):
    """Função responsável por criar a side bar do dash"""
    
    image = Image.open('logo.png')
    st.sidebar.image(image, width=120)

    st.sidebar.markdown('# Cury Company')
    st.sidebar.markdown('## Fastest Delivery in Town')
    st.sidebar.markdown("""---""")
    st.sidebar.markdown('## Selecione uma data limite')
    date_slider = st.sidebar.slider(
        'Até qual valor',
        value=pd.datetime(2022, 3, 12),
        min_value=df['Order_Date'].min().to_pydatetime(),
        max_value=df['Order_Date'].max().to_pydatetime(),
        format='DD-MM-YYYY'
    )
    st.sidebar.markdown("""---""")
    traffic_options = st.sidebar.multiselect(
        'Quais as condições do trânsito',
        ['Low','Medium','High','Jam'],
        ['Low','Medium','High','Jam']
    )
    st.sidebar.markdown("""---""")
    st.sidebar.markdown('')
    return date_slider, traffic_options

# ==================================
# ===== Gráficos visão empresa =====
# ==================================
def orders_by_day( df ):
    df_aux = (df.loc[:,['Order_Date','ID']]
                .groupby('Order_Date', as_index=False)
                .count())
    fig = px.bar(df_aux, 'Order_Date', 'ID')
    return fig

def orders_by_traffic( df ):
    df_aux = df[['ID', 'Road_traffic_density']].groupby('Road_traffic_density', as_index=False).count()
    df_aux['perc'] = df_aux['ID'] / df_aux['ID'].sum()
    fig = px.pie(df_aux, 'Road_traffic_density', 'perc')
    return fig

def orders_density_by_traffic(df):
    df_aux = (df.loc[:,['City','Road_traffic_density','ID']]
                .groupby(['City','Road_traffic_density'], as_index=False)
                .count())
    fig = px.scatter(df_aux, 'City', 'Road_traffic_density', size='ID')
    return fig
            
def orders_by_week( df ):
    df_aux = (df.loc[:,['week_of_year','ID']]
                .groupby('week_of_year', as_index=False)
                .count())
    fig = px.line(df_aux, 'week_of_year', 'ID')
    return fig    

def orders_by_deliver_week ( df ):
    amount_orders_week = df[['week_of_year','ID']].groupby('week_of_year', as_index=False).count()
    amount_deliverers_week = df[['week_of_year','Delivery_person_ID']].groupby('week_of_year', as_index=False).nunique()
    df_aux = pd.merge(amount_orders_week, amount_deliverers_week, on='week_of_year')
    df_aux['order_by_deliver'] = df_aux['ID'] / df_aux['Delivery_person_ID']
    fig = px.line(df_aux, 'week_of_year', 'order_by_deliver')
    return fig

def orders_distribution(df):
    df_aux = (df.loc[:,['City', 'Road_traffic_density', 'Delivery_location_latitude', 'Delivery_location_longitude']]
                .groupby(['City', 'Road_traffic_density'])
                .median()
                .reset_index())
    map = folium.Map()
    for index, location in df_aux.iterrows():
        folium.Marker((location['Delivery_location_latitude'], location['Delivery_location_longitude']),
                       popup='Cidade: %s, Tráfico: %s' % (location['City'],location['Road_traffic_density'])).add_to(map)
    return map

# ====================================
# ===== Utils visão entregadores =====
# ====================================
def mean_by_delivery(df):
    return (df.loc[:,['ID','Delivery_person_Ratings']]
              .groupby('ID', as_index=False)
              .mean())

def mean_by_traffic(df):
    return (df.loc[:,['Road_traffic_density', 'Delivery_person_Ratings']]
              .groupby('Road_traffic_density', as_index=False)
              .agg(**{'Avaliação Média':('Delivery_person_Ratings', 'mean'),
                      'Avaliação STD':('Delivery_person_Ratings', 'std')}))

def mean_by_weather(df):
    return (df.loc[:, ['Weatherconditions', 'Delivery_person_Ratings']]
              .groupby('Weatherconditions')
              .agg(mean=('Delivery_person_Ratings', 'mean'), std=('Delivery_person_Ratings', 'std'))
              .reset_index())

def top_slower_deliveries(df):
    return (df.loc[:,['City','Delivery_person_ID','Time_taken(min)']]
              .groupby(['City','Delivery_person_ID'])
              .mean()
              .reset_index()
              .sort_values(['City','Time_taken(min)'], ascending=False)
              .groupby('City')
              .head(5)
              .reset_index())

def top_faster_deliveries(df):
    return (df.loc[:,['City','Delivery_person_ID','Time_taken(min)']]
              .groupby(['City','Delivery_person_ID'])
              .mean()
              .reset_index()
              .sort_values(['City','Time_taken(min)'])
              .groupby('City')
              .head(5)
              .reset_index())
# ====================================
# ===== Utils visão restaurantes =====
# ====================================
    
def mean_std_by_city(df):
    return (df.loc[:,['City','Time_taken(min)']]
              .groupby('City')
              .agg(**{'time_mean':('Time_taken(min)','mean'),
                      'time_std':('Time_taken(min)','std')})
              .reset_index())

def mean_std_by_type_order(df):
    return (df.loc[:,['City','Type_of_order','Time_taken(min)']]
              .groupby(['City','Type_of_order'])
              .agg(**{'time_mean':('Time_taken(min)','mean'),
                      'time_std':('Time_taken(min)','std')})
              .reset_index())

def mean_std_by_city_type_traffic(df):
    return (df.loc[:,['City','Road_traffic_density','Time_taken(min)']]
              .groupby(['City','Road_traffic_density'])
              .agg(**{'time_mean':('Time_taken(min)','mean'),
                      'time_std':('Time_taken(min)','std')})
              .reset_index())