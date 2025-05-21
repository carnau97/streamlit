#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Oct 25 19:57:22 2024

@author: carmenarnau
"""

import streamlit as st

st.set_page_config('Prueba') # nombre que le pones a la pestaña
st.header("Streamlit de prueba") # título
st.write("")
st.write("Hacemos una aplicación web de prueba") # texto


st.sidebar.markdown("## Menú lateral") # título del menú lateral

# Para que haga los siguientes menús al lateral:
    
with st.sidebar:

    deslizante = st.slider(
            label="Selecciona un número",
            min_value=1, max_value=10,
            value=5) # valor por defecto

    
    opciones_num = st.number_input('Otra forma de seleccionar un número',min_value=1, 
                                        max_value=10, value = 5)



    st.write("Número seleccionado: ", str(opciones_num))

    

# # Lo que está fuera del st.sidebar, estará en el menú principal

cbox = st.checkbox('Selecciona para mostrar más información')

st.markdown("<br>", unsafe_allow_html=True)  # Agrega un salto de línea
# Otra opcion es poner st.write("")


if cbox: # cbox toma el valor True si se pulsa

    seleccion_cat = st.selectbox(
    'Selecciona una categoría',
    options=["Categoría 1", "Categoría 2", "Categoría 3"])

    st.write(seleccion_cat + " seleccionada ✅")
    

# # Creamos un contador: 
# contador = 0
# if st.button("Incrementar"):
#     contador = contador + 1
    
# if st.button("Reiniciar"):
#     contador = 0
    
# st.write("Valor del contador: " + str(contador))


# Sin session state no se guarda el resultado de la interacion previa porque se vuelve a lanzar contador = 0


# Inicializar el estado del contador en session_state
if "contador" not in st.session_state:
    st.session_state["contador"] = 0

# Botón para incrementar el contador
if st.button("Incrementar"):
    st.session_state["contador"]+= 1

# Botón para reiniciar el contador
if st.button("Reiniciar"):
    st.session_state["contador"] = 0

st.write("Valor del contador: " + str(st.session_state["contador"]))



