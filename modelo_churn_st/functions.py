import streamlit as st
import numpy as np
from datetime import datetime
import pickle
from sklearn.metrics import auc, confusion_matrix, precision_score, recall_score, roc_curve
import seaborn as sns
import matplotlib.pyplot as plt

@st.cache_resource
def carga_artefactos():
    
    pipeline = pickle.load(open('ficheros_modelo/pipeline.pkl', 'rb')) # scaler
    modelo = pickle.load(open('ficheros_modelo/model.pkl', 'rb')) # modelo entrenado
    
    return pipeline, modelo



def procesar_obtener_predicciones(df, pipeline, modelo):
    
    df['financiacion'] = np.where(df['financiacion']=="SI", 1, 0)
    df['incidencia'] = np.where(df['incidencia']=="SI", 1, 0)
    df['descuentos'] = np.where(df['descuentos']=="SI", 1, 0)
    año_actual = datetime.now().year
    df['antiguedad'] = año_actual - df['antiguedad']

    X_fin = pipeline.transform(df)
    prediccion = modelo.predict_proba(X_fin)
    
    return prediccion



def represento_curva_roc(y, y_prob, title):
    
    fpr, tpr, threshold = roc_curve(y, y_prob[:, 1])
    roc_auc = auc(fpr, tpr)

    fig, ax = plt.subplots()
    ax.set_title(title)
    ax.plot(fpr, tpr, 'b', label = 'AUC = %0.2f' % roc_auc)
    ax.legend(loc = 'lower right')
    ax.plot([0, 1], [0, 1],'r--')
    ax.set_xlim([0, 1])
    ax.set_ylim([0, 1])
    ax.set_ylabel('True Positive Rate')
    ax.set_xlabel('False Positive Rate')
    
    return fig 
    
    
    
def conf_matrix_metrics(y, y_prob, umbral):
    
    
    y_pred = 1*(y_prob[:, 1] > umbral)

    precision = round(precision_score(y, y_pred), 2)
    recall = round(recall_score(y, y_pred), 2)
    

    fig, ax = plt.subplots()
    sns.heatmap(confusion_matrix(y, y_pred), annot=True, cmap = 'Blues', fmt='d')
    ax.set_title("Matriz de confusión")
    
    
    return precision, recall, fig