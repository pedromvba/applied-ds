import streamlit as st
import pandas as pd
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


FILE_PATH_DIFF = 'data/02_processed/different_cities.csv'
FILE_PATH_BEST_CITIES = 'data/02_processed/best_cities.csv'
diff_cities = read_data(FILE_PATH_DIFF)


# page
st.header('Direcionador de Investimento')
st.write('''
         
Nesta aba do aplicativo, temos como objetivo realizar a análise dos 
dados e obter insights sobre oportunidades de investimentos que possam tanto subsidiar
gestores da saúde na melhor alocação de recursos públicos, bem como evidenciar ao setor privado
oportunidades de investimento que possam trazer retornos.

Sobre o tema, a aba propõe identificar os procedimentos para os quais os 
cidadãos tem que se deslocar até outra localidade para serem atendidos.
         
Para isso é realizada a análise por procedimentos realizados fora do município do cidadão, com
foco no tipo de procedimento realizado, partindo-se da seguinte premissa:
         
Caso existisse infraestrutura de saúde adequada no município do cidadão, ele preferiria ser atendido
localmente a se deslocar. Nesse sentido, investimentos públicos deveriam ser direcionados para
atender as maiores demandas de forma a aumentar a eficiência do investimento público.

Por outro lado, e seguindo a mesma premissa, pode haver oportunidade de investimentos para o setor
privado também, considerando a conversão do custo de deslocamento (tempo, financeiro) em receitas para
o setor.

'''

)

st.write('### Análise de Procedimentos Realizados fora do Município do Cidadão')
st.write('''
Aqui o usuário deve identificar quais os procedimentos/ramos da saúde geram maior número de 
deslocamentos dos cidadãos''')

grouped_procedures = diff_cities.\
    groupby(['municipio_paciente', 'procedimento_principal'])['procedimento_principal'].\
    count().\
    reset_index(name='Contagem')

st.write('### Análise Geral')

total_grouped_procedures = diff_cities.\
    groupby('procedimento_principal')['procedimento_principal'].\
    count().\
    reset_index(name='Contagem')

top_procedures = total_grouped_procedures.sort_values('Contagem', ascending=False)

st.dataframe(top_procedures, hide_index=True)

st.write('### Análise por Cidade')
options = st.multiselect(
    label = 'Selecione uma ou mais Cidades para Análise',
    options=grouped_procedures['municipio_paciente'].unique()
)

if options:
    grouped_view = grouped_procedures[grouped_procedures['municipio_paciente']\
    .isin(options)]\
    .sort_values('Contagem', ascending=False)
    
    st.dataframe(grouped_view, hide_index=True)

st.write('### Identificação dos Municípios Mais Propensos ao Investimento')
st.write('''
A partir do gráfico abaixo que contrapõe o número dos deslocamentos pelo valor pago pelo SUS pelo 
atendimento do cidadão em outro município, pode-se indentificar os mais propensos ao investimento.
         
Assim, Municípios para os quais seus cidadão tenham se locomovido mais vezes para serem atendidos, e
que os valores desses atendimentos sejam maiores, tendem a ser municípios mais promissores para futuros
investimentos. Esses Municípios são os que se encontram mais próximos ao canto superior direito do
gráfico.
'''
)


city_grouped = diff_cities.groupby('municipio_paciente').agg(
    valor_total = ('valor_ato_profissional', 'sum'),
    numero_deslocamentos = ('municipio_paciente', 'count')
).reset_index()

scatter_investiment(city_grouped)

st.write('''
Abaixo segue a nota de cada Município, que vai de 0 a 10 no qual quanto maior a nota mais promissor 
para investimento''')

city_grouped['score'] = 10*(city_grouped['valor_total']*city_grouped['numero_deslocamentos'])/max((city_grouped['valor_total']*city_grouped['numero_deslocamentos']))

best_cities = city_grouped[['municipio_paciente', 'score']].sort_values('score', ascending=False)

st.dataframe(best_cities, 
             width=500,
             height=300,
             hide_index=True)


st.write('### Exportar Informações')

st.write('''
Caso deseje exportar as informações dos principais procedimentos realizado fora do Município do Cidadão
ou das cidades mais promissoras para os investimentos, favor utilizar o botão abaixo:
''')

st.download_button(label='Melhores Cidades Para Investimento',
                   data=best_cities.to_csv(index=False),
                   file_name='melhores_cidades_investimento.csv')

st.download_button(label='Procedimentos Mais Demandados',
                   data=top_procedures.to_csv(index=False),
                   file_name='procedimentos_mais_demandados.csv')

if options:
    st.download_button(label='Procedimentos Mais Demandados dos Municípios Selecionado',
                   data=grouped_view.to_csv(index=False),
                   file_name='procedimentos_mais_demandados.csv')