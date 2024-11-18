''''
Script used to processing the data, with involved transformation and filtering
'''
import pandas as pd

# data reading
raw_df = pd.read_csv('./data/01_raw/roraima_with_procedures.csv')

# converting ids to strings
raw_df['id_municipio_estabelecimento_aih'] = raw_df['id_municipio_estabelecimento_aih'].astype(str)
raw_df['id_municipio_paciente'] = raw_df['id_municipio_paciente'].astype(str)
raw_df['id_procedimento_principal'] = raw_df['id_procedimento_principal'].astype(str)

# removing id_municipio_estabelecimento_aih digit
raw_df['id_municipio_estabelecimento_aih'] = raw_df['id_municipio_estabelecimento_aih'].apply(lambda x: x[:-1])

# filtering cities by State: Roraima and Amazonas
filtered_df =raw_df[(raw_df['id_municipio_paciente'].str.startswith('14','13'))]

# mapping city names
mapping_df = filtered_df.copy()

city_data = pd.read_json('./data/01_raw/cities.json')
city_data['id'] = city_data['id'].astype(str)

city_names = city_data.set_index('id')['city'].to_dict() # creating a dictionaty for mapping
mapping_df['municipio_paciente'] = mapping_df['id_municipio_paciente'].map(city_names) # mapping the municipio_paciente
mapping_df['municipio_atendimento'] = mapping_df['id_municipio_estabelecimento_aih'].map(city_names) # mapping municipio_atendiemnto

# mapping procedures mames
procedure_names = pd.read_csv('./data/01_raw/procedure_names.csv', dtype=str)
procedure_dict = procedure_names.set_index('CÓDIGO')['PROCEDIMENTO'].to_dict() # creating a dictionaty for mapping

mapping_df['procedimento_principal'] = mapping_df['id_procedimento_principal'].map(procedure_dict) # mapping the procedimento

# dropping values that could't be identified
processed_df = mapping_df.copy()
processed_df.dropna(axis=0, how='any', inplace=True)

# dropping converted columns
processed_df.drop(axis=1, 
                  columns=['id_municipio_estabelecimento_aih', 
                           'id_municipio_paciente',
                           'id_procedimento_principal'],
                  inplace=True)

# saving processed data
processed_df.to_csv('./data/02_processed/full_data.csv', index=False)

print('Data Processing Done!')
