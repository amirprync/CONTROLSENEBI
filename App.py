import streamlit as st
import pandas as pd

def load_data(file):
    return pd.read_excel(file)

def compare_dataframes(df1, df2):
    # Verificar que las columnas necesarias existan en los DataFrames
    required_columns_1 = ['Comitente - Número', 'SENEBI - Precio de Referencia', 'Instrumento - Símbolo', 'Comitente - Cantidad']
    required_columns_2 = ['P.Número', 'Precio Productor/Comercial', 'Especie', 'Cantidad']
    for col in required_columns_1:
        if col not in df1:
            raise ValueError(f"El primer archivo no tiene la columna esperada: {col}")
    for col in required_columns_2:
        if col not in df2:
            raise ValueError(f"El segundo archivo no tiene la columna esperada: {col}")

    # Renombrar las columnas para uniformidad
    df1.rename(columns={
        'Comitente - Número': 'Numero', 
        'SENEBI - Precio de Referencia': 'Precio',
        'Instrumento - Símbolo': 'Simbolo',
        'Comitente - Cantidad': 'Cantidad'
    }, inplace=True)
    
    df2.rename(columns={
        'P.Número': 'Numero', 
        'Precio Productor/Comercial': 'Precio',
        'Especie': 'Simbolo',
        'Cantidad': 'Cantidad'
    }, inplace=True)
    
    # Unir los dataframes para comparar
    merged_df = pd.merge(df1, df2, on=['Numero', 'Simbolo', 'Cantidad'], how='outer', suffixes=('_1', '_2'))
    
    # Detectar discrepancias en precio y asignar color rojo
    merged_df['check_prices'] = merged_df.apply(
        lambda row: f"<span style='color:red;'>{row['Precio_1']}</span>" if row['Precio_1'] != row['Precio_2'] else row['Precio_1'],
        axis=1
    )

    # Filtrar las filas con discrepancias
    discrepancies = merged_df[merged_df['Precio_1'] != merged_df['Precio_2']]

    return discrepancies[['Numero', 'Precio_1', 'Precio_2', 'check_prices', 'Simbolo', 'Cantidad']]

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
            # Usar Markdown y HTML para mostrar los resultados con color
            st.markdown(result.to_html(escape=False, index=False), unsafe_allow_html=True)
    except Exception as e:
        st.error(f"Error al comparar archivos: {e}")
