import streamlit as st
import pandas as pd


# Page Color

# initializing session state to track file_state parameter shared between pages
if 'file_state' not in st.session_state:
    st.session_state['file_state'] = 0


app_name = 'Monitor da Saúde'

# Project Cover

# Basic Information
st.title(f'{app_name}')

st.subheader(f'Bem vindo ao {app_name}! 🏥')

st.image('images/Capa.jpg')

st.write(f'''O projeto {app_name} tem como objetivo identificar municípios com potencial 
         de investimento em infraestrutura de saúde, baseado, tanto no deslocamento dos cidadãos 
         em busca de atendimento do SUS quanto nos procedimentos realizados em cada localidade. 
         Ainda, permite que cidadãos verifiquem o Município mais próximo com o melhor atendimento do SUS.''')

st.write('''
O sistema de saúde público no Brasil é bastante abrangente, tanto em termos de procedimentos que podem 
ser realizados gratuitamente quanto no espaço geográfico que ele deve cobrir, considerando as dimensões do Brasil. 
Ao mesmo tempo, devido a essas características, bem como a definição na Constituição Nacional de que a saúde é
direito do cidadão, o sistema de saúde brasileiro necessita de um bom planejamento de investimentos. Nesse sentido, 
é importe que os gestores da saúde consigam ter uma visão resumida dos atendimentos realizados, bem como dos investimentos 
despendidos, de forma a planejar as despesas nos anos posteriores.

Além disso, uma das realidades que acomete o povo brasileiro é a infraestrutura de saúde mais 
simples longe das capitais, fazendo com que o público tenha que se deslocar grandes distâncias 
para ser atendido nas capitais. 

Assim, de forma a subsidiar o planejamento de gestores dos Ministério da Saúde para o ano posterior, 
bem como indicar localidades nas quais há espaço para incremento/investimento em infraestrutura de 
saúde, o aplicativo criado apresenta de forma compreensível e prática tais informações para que sejam 
utilizada por Prefeituras, parlamentares/candidatos, ONGs e Empresários do Setor da Saúde 
no suporte das justificativas das busca de seus objetivos, sejam eles votos, recursos financeiros, etc.
         
Por fim, de forma a apoiar o cidadão, o aplicativo indica o Município mais próximo e com o melhor atendimento
ao cidadão, de forma que em caso de deslocamento, esse seja mais efetivo.
''')

# creating backgroud color session state
if 'backgroud_state' not in st.session_state:
    st.session_state['backgroud_state'] = '#FFFFFF'

#initializing with white and picking a new color
background_color = st.color_picker(
    label='Caso deseje alterar a cor do aplicativo para um maior conforto visual, escolha e aplique uma nova cor abaixo:',
    value=st.session_state['backgroud_state'])

#updating session state
st.session_state['backgroud_state'] = background_color

# applying the backgroud color
st.markdown(
    f'''
    <style>
    [data-testid="stApp"] {{
        background-color: {st.session_state['backgroud_state']}
    }}
    </style>
    ''',
    unsafe_allow_html=True)


# Usefull Links
st.subheader('Links Úteis')

st.write('''

[Github do Projeto](https://github.com/pedromvba/applied-ds-tp1)

[Dados do Projeto](https://drive.google.com/file/d/1sNKzhx4-ATKZ2tqLI8mPeVx1YYeMMoiv/view?usp=share_link).
         
[Inspiração para o Projeto - Medium](https://medium.com/data-hackers/explorando-dados-do-sus-com-sql-e9c6cfc08cc2)

Contato do Desenvolvedor: pedromvba@gmail.com         
         
''')