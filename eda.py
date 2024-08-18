import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from styles import style
intro = """
# Analisis Exploratorio de Datos Automatico
### Daniel Vielma Data Scientist\n

Hacer un analisis exploratorio de datos resulta beneficioso. Esto permite observar las características fundamentales de los mismos, comprender la estructura del conjunto de datos, identificar la variable objetivo y explorar posibles técnicas de modelado.\n

![](https://raw.githubusercontent.com/Lilsup99/autoeda/main/datascience-hero.jpg)

Cargue su archivo `.csv` o `.xlsx` y obtenga su reporte inicial de un analisis exploratorio de datos.

"""
st.write(intro)
st.markdown(style,unsafe_allow_html=True)
##### Funciones de validacion
def hola():
    pass

def grafica_columna(serie:pd.Series):
    if serie.dtype == 'object':
        if len(serie.drop_duplicates())<=15:
            fig = px.bar(serie.value_counts(),x=serie.value_counts().index, y='count')
            return fig
        else:
            fig = go.Figure(go.Indicator(
                            mode = "number",
                            value = len(serie.drop_duplicates()),
                            title = {'text': "Valores unicos", 'font': {'size': 24}},
                            number={'font': {'size': 70}}
                            ))
            fig.update_layout(paper_bgcolor = "rgba(20, 94, 137, 0.2)",font = {'color': "white", 'family': "Arial"})
            return fig
    elif (serie.dtype == 'float64') or (serie.dtype == 'int64'):
        fig = px.histogram(serie)
        return fig
#########################

archivo = st.file_uploader('Ingrese archivo(csv o xlsx)')

### Control de tipo de archivo que se sube
data = pd.DataFrame(dtype="category")
if archivo is not None:
    if '.csv' in archivo.name:
        data = pd.read_csv(archivo)
    elif '.xlsx' in archivo.name:
        data = pd.read_excel(archivo, header=0)

    else: st.write('Subir un archivo de datos en formato tabular')


if not data.empty:
    st.markdown('# Resultados')

with st.expander('datos'):
    if not data.empty:
        st.dataframe(data)

with st.expander('Informacion detallada'):
    if not data.empty:
        for i in data.columns:
            st.divider()
            st.markdown("# {}".format(i))
            col1, col2 = st.columns([0.6,0.4])
            with col1:
                st.write(grafica_columna(data[i]))
            with col2:
                if data[i].dtype == 'object':
                    text = "* Valores Nulos: {} \n * Valor mas repetido: {} "\
                            .format(data[i].isna().sum(),
                                    data[i].mode(dropna=True)[0])
                elif (data[i].dtype == 'float64') or (data[i].dtype == 'int64'):
                    text = "* Valores Nulos: {} \n * Valor minimo: {} \n * Valor maximo: {} \n * Valor promedio: {} \n * Desviacion estandar: {}".\
                            format(data[i].isna().sum(),
                                   data[i].min(),
                                   data[i].max(),
                                   data[i].mean(),
                                   data[i].std())
                st.write('Tipo de Dato:')
                st.write(data[i].dtype)
                st.divider()
                st.markdown(text)

