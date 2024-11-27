import os
import streamlit as st
import pandas as pd
import numpy as np
from dotenv import load_dotenv
from services.processing_functions import *
from services.plots import *


def localidades_and_rating(procedimento):
    full_data = pd.read_csv('./data/02_processed/full_data.csv')
    localidades = full_data[full_data['procedimento_principal'] == procedimento]
    localidades['metric'] = localidades['municipio_atendimento'].map(
        localidades['municipio_atendimento'].value_counts(normalize=True)
    )
    localidades['metric'] = 100*localidades['metric'].apply(lambda x: np.sqrt(x))
    localidades['rating'] = localidades['metric'].apply(lambda x: '5' if x > 80 else '4' if x > 20 else '3' if x > 10 else '2' if x > 5 else '1')
    
    localidades = localidades[["municipio_atendimento", "metric", "rating"]]
    localidades = localidades.drop_duplicates().sort_values(by='metric', ascending=False)
    localidades['Qualidade do Atendimento'] = localidades['rating'].astype(int).apply(lambda x: '⭐'*x)
    localidades = localidades[['municipio_atendimento', 'rating', 'Qualidade do Atendimento']]
    localidades.columns = ['Município', 'Rating', 'Qualidade do Atendimento']
    

    return localidades

def map_travel(origin, gmaps_key, radius=None, destination=None):

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


origin = st.text_input(label = 'Insira o nome da sua localidade dentro do Estado de Roraima')

st.write('Informe se você já sabe o procedimento que deseja realizar ou não.')
options = ["Já sei o meu Procedimento","Não sei o meu Procedimento"]
selection = st.pills("Selecione uma opção abaixo:", options, selection_mode="single")


if selection == "Já sei o meu Procedimento":

    if prompt:= st.chat_input('Que tipo de tratamento você precisa?'):
        with st.chat_message("user",avatar='👤'):
            st.markdown(prompt)
        try:
            with st.chat_message("assistant", avatar='🤖'):
                with st.spinner("Estou pensando"):

                    req = requests.post(
                        url = 'http://localhost:8000/procedimento/',
                        json = {'message': prompt})
                    response = req.json()

                    if response["assistant"] == "DIAGNOSTICO E/OU ATENDIMENTO DE URGENCIA EM CLINICA MEDICA":
                        st.write("""Não conseguimos identificar um procedimento para sua solicitação, favor 
                                procurar um atendimento de urgência em uma das seguintes localidades:""")
                        
                        clinica_medica = localidades_and_rating("DIAGNOSTICO E/OU ATENDIMENTO DE URGENCIA EM CLINICA MEDICA")

                        st.dataframe(clinica_medica[['Município', 'Qualidade do Atendimento']], hide_index=True)

                        clinica_medica['Rating'] = pd.to_numeric(clinica_medica['Rating'])
                        top3_clinica = clinica_medica.nlargest(3, 'Rating')

                        st.write('Verifique abaixo as rotas para as 3 melhores localidades para o seu atendimento')

                        for city in top3_clinica['Município']:
                            
                            st.write(f"**{city}**")
                            st.write(f"Rating: {top3_clinica.loc[top3_clinica['Município'] == city, 'Rating'].values[0]}")
                            destination = city
                            routes(origin, destination, gmaps_key)

                    else:
                        st.write(f"""Identificamos atendimento para {response["assistant"].lower()} nas seguintes localidades:""")


                        localidades = localidades_and_rating(response["assistant"])
                        st.dataframe(localidades[['Município', 'Qualidade do Atendimento']], hide_index=True)
                        

                        localidades['Rating'] = pd.to_numeric(localidades['Rating'])
                        top3 = localidades.nlargest(3, 'Rating')

                        st.write('Verifique abaixo as rotas para as 3 melhores localidades para o seu atendimento')

                        for city in top3['Município']:
                            
                            st.write(f"**{city}**")
                            st.write(f"Rating: {top3.loc[top3['Município'] == city, 'Rating'].values[0]}")
                            destination = city
                            routes(origin, destination, gmaps_key)

        except:
            st.write("Ocorreu um erro no servidor, por favor aguarde alguns minutos e tente novamente")


elif selection == "Não sei o meu Procedimento":

    radius = st.slider(
        label = 'Insira a distância máxima que deseja percorrer em quilômetros',
        step=1,
        min_value=0,
        max_value=800
    )


    if origin and radius != 0:

        map_travel(origin=origin, radius=radius, gmaps_key=gmaps_key)
