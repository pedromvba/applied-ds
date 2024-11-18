import altair as alt
import streamlit as st


def scatter_trip_care_count(df):

    scatter = alt.Chart(df).mark_circle(size=60).encode(
        x=alt.X('Contagem de Deslocamentos:Q', title='Contagem de Deslocamentos'),
        y=alt.Y('Contagem de Atendimentos:Q', title='Contagem de Atendimentos'),
        tooltip=['Município', 'Contagem de Deslocamentos', 'Contagem de Atendimentos'],
        color=alt.value('green')
    ).interactive()

    return st.altair_chart(scatter, use_container_width=True)



def scatter_investiment(df):

    scatter = alt.Chart(df).mark_circle(size=150).encode(
        x=alt.X('numero_deslocamentos:Q', title='Número de Deslocamentos'),
        y=alt.Y('valor_total:Q', title='Valor Total dos Atendimentos'),
        tooltip=['municipio_paciente', 'numero_deslocamentos', 'valor_total'],
        color=alt.value('steelblue')
    ).interactive().properties(
    title='Número de deslocamentos por soma dos valores gastos com procedimentos',
    width=400,
    height=300
)

    return st.altair_chart(scatter, use_container_width=True)


