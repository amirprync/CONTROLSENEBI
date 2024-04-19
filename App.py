import streamlit as st
import pandas as pd

def load_data(file):
    return pd.read_excel(file)

def compare_dataframes(df1, df2):
    # Renombrar las columnas para uniformidad
    df1.rename(columns={'Comitente - Número': 'Numero', 'SENEBI - Precio de Referencia': 'Precio'}, inplace=True)
    df2.rename(columns={'P.Número': 'Numero', 'Precio Productor/Comercial': 'Precio'}, inplace=True)
    
    # Unir los dataframes para comparar
    merged_df = pd.merge(df1, df2, on='Numero', suffixes=('_1', '_2'))
    # Filtrar las filas donde los precios no coinciden
    discrepancies = merged_df[merged_df['Precio_1'] != merged_df['Precio_2']]
    return discrepancies

st.title('Comparador de Excel')

# Carga de archivos
file1 = st.file_uploader("Subir archivo Excel 1", type=['xlsx'])
file2 = st.file_uploader("Subir archivo Excel 2", type=['xlsx'])

if file1 and file2:
    # Cargar los datos
    df1 = load_data(file1)
    df2 = load_data(file2)

    # Comparar los dataframes
    result = compare_dataframes(df1, df2)

    if result.empty:
        st.write("Todos los datos coinciden.")
    else:
        st.write("Discrepancias encontradas:")
        st.write(result)
