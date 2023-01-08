import streamlit as st
from PIL import Image

st.set_page_config(page_title='Home',
                   page_icon='✊',
                   layout='wide')

image = Image.open('logo.png')
st.sidebar.image(image, width=120)
st.sidebar.markdown('# Cury Company')
st.sidebar.markdown('## Fastest Delivery in Town')

st.markdown(
    """
    ### Growth Dashboard foi construído para acompanhar as estatísticas de cresciemnto 
    - Visão empresa:
        - Visão Gerencial: Métricas gerais de comportamento
        - Visão Tática: Indicadores semanais de crescimento
        - Visão Geográfica: Insights de geolocalização
    - Visão entregador:
        - Acompanhamento dos indicadores semanais de crescimento
    - Visão restaurantes
        - Indicadores semanais de crescimento dos restaurantes
""")