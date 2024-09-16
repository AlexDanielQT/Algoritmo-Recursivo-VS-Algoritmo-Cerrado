import pandas as pd
import plotly.express as px
import streamlit as st

def create_charts(df1, df2):
    charts = {}

    # Gráfico para 'forma_recursiva'
    fig_recursiva = px.line(df1, x='n', y='forma_recursiva_time_us', title='Tiempo de Ejecución de Forma Recursiva')
    fig_recursiva.update_traces(line=dict(color='red'))
    charts['Forma Recursiva'] = fig_recursiva

    # Gráfico para 'forma_matematica_time_us'
    fig_matematica_con_condicionales = px.line(df1, x='n', y='forma_matematica_time_us', title='Tiempo de Ejecución de Forma Matemática con Condicionales')
    fig_matematica_con_condicionales.update_traces(line=dict(color='blue'))
    charts['Forma Matemática con Condicionales'] = fig_matematica_con_condicionales

    # Gráfico para 'forma_matematica_time_us2'
    fig_matematica_sin_condicionales = px.line(df2, x='n', y='forma_matematica_time_us2', title='Tiempo de Ejecución de Forma Matemática sin Condicionales')
    fig_matematica_sin_condicionales.update_traces(line=dict(color='green'))
    charts['Forma Matemática sin Condicionales'] = fig_matematica_sin_condicionales

    # Unir df1 y df2 para comparar las fórmulas matemáticas
    df_combined = pd.merge(df1[['n', 'forma_matematica_time_us']], df2[['n', 'forma_matematica_time_us2']], on='n')

    # Transformar el DataFrame a formato largo
    df_long = pd.melt(df_combined, id_vars=['n'], value_vars=['forma_matematica_time_us', 'forma_matematica_time_us2'],
                      var_name='variable', value_name='value')
    
    # Gráfico para comparación de tiempos de ejecución entre fórmulas matemáticas
    fig_comparativo_matematico = px.line(df_long, x='n', y='value', color='variable', 
                                         title='Comparación de Tiempos de Ejecución de Fórmulas Matemáticas', 
                                         labels={'value': 'Tiempo Promedio (μs)', 'variable': 'Versión'})
    fig_comparativo_matematico.update_traces(marker=dict(size=0))  # No mostrar puntos
    fig_comparativo_matematico.update_layout(legend_title="Versión", xaxis_title="n", yaxis_title="Tiempo Promedio (μs)")
    charts['Comparación Matemática'] = fig_comparativo_matematico

    # Gráfico para comparación entre recursivo y matemático sin condicionales
    df_comparacion_recursiva_matematica = pd.merge(df1[['n', 'forma_recursiva_time_us']], df2[['n', 'forma_matematica_time_us2']], on='n')
    df_comparacion_long = pd.melt(df_comparacion_recursiva_matematica, id_vars=['n'], value_vars=['forma_recursiva_time_us', 'forma_matematica_time_us2'],
                                  var_name='variable', value_name='value')
    
    fig_comparativo_recursiva_matematica = px.line(df_comparacion_long, x='n', y='value', color='variable',
                                                  title='Comparación entre Tiempo de Ejecución de Forma Recursiva y Matemática sin Condicionales',
                                                  labels={'value': 'Tiempo Promedio (μs)', 'variable': 'Algoritmo'})
    fig_comparativo_recursiva_matematica.update_traces(marker=dict(size=0))  # No mostrar puntos
    fig_comparativo_recursiva_matematica.update_layout(legend_title="Algoritmo", xaxis_title="n", yaxis_title="Tiempo Promedio (μs)")
    charts['Comparación Recursiva vs Matemática'] = fig_comparativo_recursiva_matematica

    return charts

# Leer datos de los archivos CSV
df1 = pd.read_csv('time1.csv')
df2 = pd.read_csv('time2.csv')

# Crear gráficos
charts = create_charts(df1, df2)

# Configuración de Streamlit
st.title("Análisis de Tiempo de Ejecución de Algoritmos")

# Mostrar gráficos en Streamlit
for title, chart in charts.items():
    st.subheader(title)
    st.plotly_chart(chart, use_container_width=True)
