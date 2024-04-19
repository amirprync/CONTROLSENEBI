import streamlit as st
import pandas as pd

def load_data(file):
    return pd.read_excel(file)

def compare_dataframes(df1, df2):
    # Verificar que las columnas necesarias existan en los DataFrames
    required_columns_1 = ['Comitente - Número', 'SENEBI - Precio de Referencia', 'Instrumento - Símbolo', 'Comitente - Cantidad']
    required_columns_2 = ['P.Número', 'Precio Productor/Comercial', 'Especie', 'Cantidad']

    # Verificación de las columnas y renombrarlas para coincidencia
    df1 = df1.rename(columns={
        'Comitente - Número': 'Numero', 
        'SENEBI - Precio de Referencia': 'Precio_1',
        'Instrumento - Símbolo': 'Simbolo',
        'Comitente - Cantidad': 'Cantidad'
    })

    df2 = df2.rename(columns={
        'P.Número': 'Numero', 
        'Precio Productor/Comercial': 'Precio_2',
        'Especie': 'Simbolo',
        'Cantidad': 'Cantidad'
    })
    
    # Unir los dataframes para comparar en base a las tres columnas clave
    merged_df = pd.merge(df1, df2, on=['Numero', 'Simbolo', 'Cantidad'], how='outer', indicator=True)
    
    # Aplicar formato HTML para resaltar las discrepancias de precio
    merged_df['check_prices'] = merged_df.apply(
        lambda row: f"<span style='color:red;'>{row['Precio_1']}</span>" if row['_merge'] == 'both' and pd.notna(row['Precio_1']) and pd.notna(row['Precio_2']) and row['Precio_1'] != row['Precio_2'] else f"{row['Precio_1']}",
        axis=1
    )

    # Filtrar las filas con discrepancias
    discrepancies = merged_df[(merged_df['_merge'] != 'both') | ((merged_df['Precio_1'] != merged_df['Precio_2']) & pd.notna(merged_df['Precio_1']) & pd.notna(merged_df['Precio_2']))]
    discrepancies = discrepancies.drop(columns=['_merge'])

    return discrepancies[['Numero', 'Simbolo', 'Cantidad', 'Precio_1', 'Precio_2', 'check_prices']]

st.title('Control SENEBI')

# Carga de archivos
file1 = st.file_uploader("Subir archivo Excel DE OPERACIONES DE BO", type=['xlsx'])
file2 = st.file_uploader("Subir archivo Excel DE MINUTAS SENEBI", type=['xlsx'])

if file1 and file2:
    df1 = load_data(file1)
    df2 = load_data(file2)

    try:
        # Comparar los dataframes
        result = compare_dataframes(df1, df2)

        if result.empty:
            st.success("Todos los datos coinciden.")
        else:
            st.write("Discrepancias encontradas:")
            # Usar Markdown y HTML para mostrar los resultados con color
            st.markdown(result.to_html(escape=False, index=False), unsafe_allow_html=True)
    except Exception as e:
        st.error(f"Error al comparar archivos: {e}")
