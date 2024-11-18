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


@router.get('/direcionador-investimento/')
async def direcionador_investimento():
    return best_cities\
            .rename(columns={'municipio_paciente': 'Municipio', 'score': 'Score de Investimento'})\
            .to_dict(orient='records')