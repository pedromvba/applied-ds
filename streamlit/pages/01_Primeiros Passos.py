import streamlit as st
import pandas as pd
from services.processing_functions import *
import time



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



st.header('Introdução - Comece por Aqui 👋🏼')

st.subheader('Dados Embarcados na Solução')
st.write('''

Os dados foram obtidos diretamente da API da Base dos Dados. Essa API coleta e mantém dados de interesse
público, como por exemplo, os da Saúde, diretamente de bases oficiais. Ou seja, no caso em análise,
os dados oficiais de saúde foram coletados pela API da Base dos Dados diretamente do Datasus e posteriormente
importados neste projeto.''')

# Data Sample
df = pd.read_csv('./data/02_processed/full_data.csv')

st.write('#### Amostra dos Dados')
st.dataframe(df.head(10), hide_index=True)

# Data Dictionary
st.write('#### Dicionário dos Dados')
st.write('''
      
Quantidade de Procedimentos: quantidade de procedimentos realizados no atendimento

Mês: mês de realização do atendimento

Ano: ano de realização do atendimento

Sigla UF : Estado no qual foi realizado o atendimento

Valor Ato Profissional: valor do procedimento realizado

Município Paciente: Município de domicílio do paciente

Município Atendimento: Município no qual o paciente foi atendido

Procedimento Principal: principal atendimento realizado
         
''')  
st.write('____')

st.write('### Adicionar mais Dados')

st.write('''Caso queira adicionar mais dados ao projeto, favor utilizar o botão abaixo inserindo um arquivo
em formato .csv, respeitando o seguinte schema:
         

| quantidade_procedimentos | mes | ano  | sigla_uf | valor_ato_profissional | municipio_paciente | municipio_atendimento | procedimento_principal|
|--------------------------|-----|------|----------|------------------------|--------------------|-----------------------|-----------------------|
| 1                        | 2   | 2023 | RR       | 1317.32                | Boa Vista          | Boa Vista             | ARTROPLASTIA  |
| 2                        | 2   | 2023 | RR       | 0.0                    | Boa Vista          | Boa Vista             | ARTROPLASTIA  |
| 2                        | 2   | 2023 | RR       | 0.0                    | Boa Vista          | Boa Vista             | ARTROPLASTIA  |
| 1                        | 2   | 2023 | RR       | 12.39                  | Boa Vista          | Boa Vista             | ARTROPLASTIA  |
| 2                        | 2   | 2023 | RR       | 0.0                    | Boa Vista          | Boa Vista             | ARTROPLASTIA  |

'''
)

uploaded_file = st.file_uploader(
                label='Favor inserir seu arquivo .csv aqui.',
                type='csv'
                )

if uploaded_file:

    uploaded_df = pd.read_csv(uploaded_file, encoding='utf-8')
    original_df = pd.read_csv('data/02_processed/full_data.csv', encoding='utf-8')

    if list(uploaded_df.columns) != list(original_df.columns):
        st.write('o schema dos dados não é compatível com o solicitado acima')
    
    else:
        full_df = pd.concat([original_df, uploaded_df])
        full_df.to_csv('data/02_processed/full_data.csv', index=False)

        diff_cities(full_df)

        # progress bar
        progress_bar = st.progress(0, text='Estamos Processando os seus Dados!')
        for percent in range(100):
            time.sleep(0.01)
            progress_bar.progress(percent + 1, text='Estamos Processando os seus Dados!')
        
        time.sleep(1)
        progress_bar.empty()

        time.sleep(0.3)
        st.write('''
                 
                Pronto, seus dados foram processados! Favor continuar para as abas Primeiros Passos
                ou Oportunidades
                
                '''
        )