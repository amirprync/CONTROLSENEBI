import streamlit as st
import pandas as pd

def load_data(file):
    return pd.read_excel(file)

def compare_dataframes(df1, df2):
    # Verificar que las columnas necesarias existan en los DataFrames
    if 'Comitente - Número' not in df1 or 'SENEBI - Precio de Referencia' not in df1:
        raise ValueError("El primer archivo no tiene las columnas esperadas.")
    if 'P.Número' not in df2 or 'Precio Productor/Comercial' not in df2:
        raise ValueError("El segundo archivo no tiene las columnas esperadas.")

    # Renombrar las columnas para uniformidad
    df1.rename(columns={'Comitente - Número': 'Numero', 'SENEBI - Precio de Referencia': 'Precio_1'}, inplace=True)
    df2.rename(columns={'P.Número': 'Numero', 'Precio Productor/Comercial': 'Precio_2'}, inplace=True)
    
    # Unir los dataframes para comparar
    merged_df = pd.merge(df1, df2, on='Numero', how='outer')
    
    # Rellenar valores faltantes para asegurar la alineación
    merged_df['Precio_1'].fillna(value=pd.NA, inplace=True)
    merged_df['Precio_2'].fillna(value=pd.NA, inplace=True)

    # Filtrar las filas donde los precios no coinciden
    discrepancies = merged_df[merged_df['Precio_1'] != merged_df['Precio_2']]
    return discrepancies

st.title('Comparador de Excel')

# Carga de archivos
file1 = st.file_uploader("Subir archivo Excel 1", type=['xlsx'])
file2 = st.file_uploader("Subir archivo Excel 2", type=['xlsx'])

if file1 and file2:
    df1 = load_data(file1)
    df2 = load_data(file2)

    try:
        # Comparar los dataframes
        result = compare_dataframes(df1, df2)

        if result.empty:
            st.write("Todos los datos coinciden.")
        else:
            st.write("Discrepancias encontradas:")
            st.write(result)
    except Exception as e:
        st.error(f"Error al comparar archivos: {e}")
