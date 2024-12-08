import streamlit as st
import pandas as pd
from functions import  procesar_obtener_predicciones, carga_artefactos

st.set_page_config('Modelo churn')
st.header("Predicciones modelo de churn") # título

# Cargamos artefactos (se queda en cache)
pipeline, modelo = carga_artefactos()

st.write("")

with st.sidebar:

    antiguedad = st.slider(
                label="Selecciona el año de contratación",
                min_value=1980, max_value=2024,
                value=2018)
    
    num_dt = st.number_input(
                label="Selecciona el nº de líneas impagadas",
                min_value=0, max_value=10,
                value=0)
        
    incidencia = st.selectbox(
                label="¿Ha tenido alguna incidencia?",
                options=["SI", "NO"], index = 1) # index=1 indica que el valor por defecto es el segundo
    
    financiacion = st.selectbox(
                label="¿Tiene alguna financiación?",
                options=["SI", "NO"], index = 1)
            
    descuento = st.selectbox(
                label="¿Tiene algún descuento?",
                options=["SI", "NO"], index = 1)
            
    
    conexion = st.selectbox(
                label="Tipo de conexión",
                options=["ADSL", "FIBRA"], index = 1)
            
    
    tv = st.selectbox(
                label="Tipo de pack de televisión contratado",
                options=["tv-futbol", "tv-familiar", "tv-total"])
            

# df se obtiene de los inputs del cliente

df = pd.DataFrame({'antiguedad':[antiguedad],
                   'num_dt':[num_dt],
                   'incidencia':[incidencia],
                   'financiacion':[financiacion],
                   'descuentos':[descuento],
                   'conexion':[conexion],
                   'TV':[tv],
                   })

st.write("Con los siguientes datos:")
st.write(df)

prob = round(procesar_obtener_predicciones(df, pipeline, modelo)[:,1][0] * 100, 2)

st.write("La probabilidad de darse de baja es: ")

if prob > 50:
    st.write("🚨" + str(prob) + "%")
    
else:
    st.write(str(prob) + "%")
    



