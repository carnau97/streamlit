import streamlit as st
import pandas as pd
from functions import (procesar_obtener_predicciones, carga_artefactos, 
                       represento_curva_roc, conf_matrix_metrics)

st.set_page_config('Modelo churn')

pipeline, modelo = carga_artefactos() # se necesitan para ambas pestañas

tab1, tab2 = st.tabs(["Predicciones", "Métricas"])

with tab1:

    st.header("Predicciones modelo de churn") # título
    
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
                    options=["SI", "NO"], index = 1) 
        
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
        
    
    
with tab2:
    
    st.header("Métricas modelo de churn") # título
    
    st.write("")
    
    file = st.file_uploader("Carga un fichero con la estructura requerida para el modelo:")
    
    st.write("")
    
    if file:
        
        data = pd.read_csv(file)
        
        y = data['target']
        X = data.drop('target', axis = 1)
        
        y_prob = procesar_obtener_predicciones(X, pipeline, modelo)
        
        col1, col2 = st.columns([1,1])
        
        with col1:
        
            st.write("")
            st.write("")

            
            fig = represento_curva_roc(y, y_prob, "Curva ROC")
            st.pyplot(fig) # para que mantenga el tamaño de figsize
        
        with col2:
        
            umbral = st.slider(
                        label="Selecciona un umbral:",
                        min_value=0.0, max_value=1.0,
                        value=0.5)
            
            col3, col4 = st.columns([2.5,1])
            
            with col3:
            
                precision, recall, cm = conf_matrix_metrics(y, y_prob, umbral)
            
                st.pyplot(cm)
                
            with col4:
                
                st.write("")

                #st.write("Precision " + str(int(round(precision*100, 2))) + "%")
                #st.write("Recall " + str(int(round(precision*100, 2))) + "%")
                
                # Para poner el texto mas pequeño (st.markdown te permite formatear)
                st.markdown(f"<p style='font-size: 14px;'>Precision {int(round(precision * 100, 2))}%</p>", unsafe_allow_html=True)
                st.markdown(f"<p style='font-size: 14px;'>Recall {int(round(recall * 100, 2))}%</p>", unsafe_allow_html=True)
        
    
    
    
    