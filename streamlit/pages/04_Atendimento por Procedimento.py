import streamlit as st
import requests
import pandas as pd 



def localidades(procedimento):
    full_data = pd.read_csv('./data/02_processed/full_data.csv')
    localidades = full_data[full_data['procedimento_principal'] == procedimento]['municipio_atendimento']
    localidades = localidades.unique()
    localidades = pd.Series(localidades, name='municipio')

    return localidades


st.write('## Localidades com Atendimento para Procedimento Específico')


st.write(''' O Atendimento por Procedimento permite ao cidadão digitar o procedimento desejado 
de forma que seja indicado pela aplicaçãoas localidades que realizam o procedimento desejado Caso de não ser possível 
identificar o procedimento com um alto nível de certeza, Serão indicadas ao cidadão as localidades 
nas quais são realizado atendimentos de emergência em clínica geral, de forma que um médico possa orientar o cidadão.''')

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
                    
                    st.dataframe(localidades("DIAGNOSTICO E/OU ATENDIMENTO DE URGENCIA EM CLINICA MEDICA"))

                else:
                    st.write(f"""Identificamos atendimento para o tratamento desejado nas seguintes localidades:""")
                
                    st.dataframe(localidades(response["assistant"]), hide_index=True)
    except:
        st.write("Ocorreu um erro no servidor, por favor aguarde alguns minutos e tente novamente")


            #st.write(response["assistant"])
            # atendimento para diabetes
            # acho que tenho malária
            # parto
            # tratamento para pneumonia
        
            
    

