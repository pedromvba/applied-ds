import os
import streamlit as st
import pandas as pd
from dotenv import load_dotenv
from services.processing_functions import *
from services.plots import *


# applying the backgroud color saved in the session state
background_color = st.session_state['backgroud_state']

st.markdown(
    f'''
    <style>
    [data-testid="stApp"] {{
        background-color: {background_color}
    }}
    </style>
    ''',
    unsafe_allow_html=True)


# reading data and keeping them in memory
@st.cache_data
def read_data(file_path):
    return pd.read_csv(file_path)

# importing environment variables and creating others
load_dotenv()
FILE_PATH_DIFF = 'data/02_processed/different_cities.csv'
FILE_PATH_FULL= 'data/02_processed/full_data.csv'
gmaps_key = os.getenv('GMAPS_API_KEY')

# loading data
diff_cities = read_data(FILE_PATH_DIFF)
full_data = read_data(FILE_PATH_FULL)


# calculating trip and care counts
trip_count = diff_cities['municipio_paciente'].value_counts().reset_index()
trip_count.columns = ['Município', 'Contagem de Deslocamentos']

care_count = full_data['municipio_atendimento'].value_counts().reset_index()
care_count.columns = ['Município', 'Contagem de Atendimentos']


# page
st.header('Melhor Atendimento Mais Próximo')
st.write('''
         
Nesta aba do aplicativo, temos como objetivo direcionar o cidadão para o Município com melhor infraestrutura
de saúde mais próximo dele. Partimos do pressuposto que Municípios que realizam muitos atendimentos pelo SUS
possuem uma infraestrutura de saúde mais robusta do que os que realizam poucos e cujos cidadãos costumam se
locomover para serem atendidos pelo SUS.
         
Assim, elencamos os Municípios preferíveis para que o cidadão seja atendido com base nesse histórico e 
na raio de distância que o usuário informar.

Após a indicação do melhor Município para atendimento, a melhor rota será traçada automaticamente pelo Google Maps.
    '''
)


st.write('## Indicando Cidade com Melhor Atendimento Mais Próxima')

origin = st.text_input(
    label = 'Insira o nome da sua localidade dentro do Estado de Roraima',
)

radius = st.slider(
    label = 'Insira a distância máxima que deseja percorrer em quilômetros',
    step=1,
    min_value=0,
    max_value=800
)


if origin and radius != 0:

    try:
        found_city = False

        city_options = care_count['Município'].unique()
        for city in city_options:
            destination = city
            duration, distance = get_travel_time(gmaps_key, origin, destination)
            if int(distance)/1000<= radius:
                care_city = city
                found_city = True
                st.write(f' A cidade com o melhor atendimento é: {care_city}')
                st.write(f' O tempo de viagem calculado é de: {convert_to_hours_minutes(duration)}')
                
                st.write('#### Rota Traçada')
                routes(origin, care_city, gmaps_key)
                st.write(care_city) 
                break
        
        if not found_city:
            st.write('Cidade não encotrada, favor aumentar o raio.')
        
    
    except:
        st.write('Localidade de origem não identificada, favor inserir o nome do Município como ponto de Origem')
