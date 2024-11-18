import os
from fastapi import APIRouter
from dotenv import load_dotenv
from services.processing_functions import *
from api.models.atendimento_model import AtendimentoInputModel, AtendimentoResponseModel


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

city_grouped = diff_cities.groupby('municipio_paciente').agg(
    valor_total = ('valor_ato_profissional', 'sum'),
    numero_deslocamentos = ('municipio_paciente', 'count')
).reset_index()
city_grouped['score'] = 10*(city_grouped['valor_total']*city_grouped['numero_deslocamentos'])/max((city_grouped['valor_total']*city_grouped['numero_deslocamentos']))
best_cities = city_grouped[['municipio_paciente', 'score']].sort_values('score', ascending=False)


router = APIRouter()


@router.post("/atendimento-proximo/")
async def atendimento_proximo(body: AtendimentoInputModel) -> AtendimentoResponseModel:

    origin = body.origem
    radius = body.raio

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
                    response = {'atendimento': care_city, 'tempo_viagem': convert_to_hours_minutes(duration)}
                    break
            
            if not found_city:
                response = 'Cidade não encotrada, favor aumentar o raio.'
        except:
            response = 'Localidade de origem não identificada, favor inserir o nome do Município como ponto de Origem'
    
    return response