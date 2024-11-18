import pandas as pd
import requests
import streamlit as st


@st.cache_data
def read_data(file_path):
    return pd.read_csv(file_path)

def convert_to_hours_minutes(total_seconds):
    hours = total_seconds//3600 
    minutes = (total_seconds%3600)//60 
    return f"{hours} horas e {minutes} minutos"

def diff_cities(df):
    different_cities = df[df['municipio_paciente']!= df['municipio_atendimento']]
    different_cities.to_csv('data/02_processed/different_cities.csv', index=False)

def routes(origin, destination, api_key):

    origin=origin+' Roraima Brasil'
    destination=destination+' Roraima Brasil'
    url = f"https://www.google.com/maps/embed/v1/directions?key={api_key}&origin={origin}&destination={destination}"

    #iframe in streamlit
    return st.markdown(f"""
        <iframe
            src="{url}"
            width="800"
            height="400"
            style="border:0;"
            allowfullscreen=""
            loading="lazy">
        </iframe>
    """, unsafe_allow_html=True)


def city_tuples(diff_df):
    pairs = []
    for origin_city in diff_df['municipio_paciente'].unique():
        for destination_city in diff_df['municipio_atendimento'].unique():
            if origin_city != destination_city:
                city_pair = sorted([origin_city, destination_city]) # sorted bc A to B  == B to A
                if city_pair not in pairs:
                    pairs.append(city_pair)
    return pd.DataFrame(pairs, columns=['Cidade A', 'Cidade B'])
    #return pairs


def get_travel_time(api_key, origin, destination, mode='driving'):
    endpoint = 'https://maps.googleapis.com/maps/api/distancematrix/json'
    params = {
        'origins': origin + ' Roraima Brasil',
        'destinations': destination + ' Roraima Brasil',
        'mode': mode,
        'key': api_key
    }
    
    try:
        response = requests.get(endpoint, params=params)
        response.raise_for_status()  # Levanta um erro para códigos de status HTTP 4xx/5xx
        data = response.json()
        
        if data['rows'][0]['elements'][0]['status'] == 'OK':
            duration = data['rows'][0]['elements'][0]['duration']['value']
            distance = data['rows'][0]['elements'][0]['distance']['value']
            return duration, distance
        else:
            return "Erro ao obter os dados.", None
    except requests.RequestException as e:
        return f"Erro na requisição: {e}", None
    

def merging_distance_time(original_df, distance_time_df):

    metrics_df = original_df.copy()

    # creating a primary key for merging
    metrics_df['key'] = metrics_df.apply(lambda row: tuple(sorted([row['municipio_paciente'], row['municipio_atendimento']])), axis=1)
    distance_time_df['key'] = distance_time_df.apply(lambda row: tuple(sorted([row['origin_city'], row['destination_city']])), axis=1)

    # merging data
    merged_df = pd.merge(metrics_df, distance_time_df, on='key', suffixes=('_metrics', '_results'))

    # dropping irrelevant data
    merged_df = merged_df.drop(['key', 'origin_city', 'destination_city'], axis = 1)

    return merged_df