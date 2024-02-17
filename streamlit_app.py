import altair as alt
import numpy as np
import pandas as pd
import streamlit as st

# Initialize empty DataFrames
proveedores_df = pd.DataFrame()
excel_data = pd.DataFrame()
errors_df = pd.DataFrame()
returns_df = pd.DataFrame()
ventas_con_descuento = pd.DataFrame()

uploaded_files = st.file_uploader("Cargar archivo base", type="xlsx")
proveedores_files = st.file_uploader("Cargar archivo de proveedores", type="xlsx")

if uploaded_files is not None and proveedores_files is not None:
    excel_data = pd.read_excel(uploaded_files)
    proveedores_df = pd.read_excel(proveedores_files)

    # dejar llave como string
    proveedores_df['llave'] = proveedores_df.iloc[:,0].astype(str)

    excel_data['tipo'] = excel_data['tipo'].astype(str)
    excel_data['item'] = excel_data['item'].astype(str)
    excel_data['llave'] = excel_data['item'].str[:3]

    # Identify all returns after loading and preprocessing the data
    returns_df = excel_data[excel_data['tipo'] == '302']

    # The rest of your logic follows...
    errors_list = []

    # Logic to find indexes to remove and handle errors
    # Logic to find indexes to remove and handle errors
    indexes_to_remove = set()
    for index, return_row in returns_df.iterrows():
        indexes_to_remove.add(index);
        # Find all transactions that correspond to the return item and are not returns themselves
        transactions_idx = excel_data[(excel_data['item'] == return_row['item']) & (excel_data['tipo'] != '302')].index
        
        if transactions_idx.empty:
            errors_list.append({'item': return_row['item'], 'error_message': 'No se encontró venta correspondiente a la devolución'})
        elif len(transactions_idx) < return_row['cantidad']:
            # Not enough transactions to remove as indicated by the 'cantidad'
            errors_list.append({'item': return_row['item'], 'error_message': f"Hay más ventas que devoluciones: {return_row['cantidad']}, Found: {len(transactions_idx)}"})
        else:
            indexes_to_remove.add(index)  # Add the return index itself to be removed
            # Add the specified number of transaction indexes starting from the earliest found
            for i in range(return_row['cantidad']):
                indexes_to_remove.add(transactions_idx[i])

    # Convert the errors list to a DataFrame for display
    errors_df = pd.DataFrame(errors_list)

    # Drop the rows from the main DataFrame based on the indexes to remove
    excel_data.drop(index=list(indexes_to_remove), inplace=True)

    

# Ajustar el índice y los nombres de las columnas según sea necesario
resultado.reset_index(inplace=True)


# Display logic for Streamlit
if not excel_data.empty:
    st.title('Excel cargado')
    st.write(excel_data)
else:
    st.warning("Excel no válido.")

if not errors_df.empty:
    st.error("Errores:")
    st.write(errors_df)

if not returns_df.empty:
    st.title("Devoluciones")
    st.write(returns_df)
else:
    st.info("No se encontraron devoluciones")



# Check if the DataFrame is not empty and 'cod_cco' column exists
if not excel_data.empty and 'cod_cco' in excel_data.columns:
    # Get unique values of 'cod_cco'
    unique_cod_cco = excel_data['cod_cco'].unique()

    for cod_cco in unique_cod_cco:
        # Filter DataFrame for the current 'cod_cco'
        filtered_df = excel_data[excel_data['cod_cco'] == cod_cco]

        # Display the filtered DataFrame
        st.subheader(f"Centro de costo: {cod_cco}")
        st.dataframe(filtered_df)

        # Unir `excel_data` con `proveedores_df` para tener la información de descuento disponible en las ventas
        ventas_con_descuento = pd.merge(excel_data, proveedores_df, left_on='llave', right_on='llave')

        # Calcular el total de ventas, total descuento y el valor después del descuento por proveedor
        grupo_proveedores = ventas_con_descuento.groupby('llave').apply(lambda x: pd.Series({
            'Total Ventas': x['pre_tot'].sum(),  # Asume que hay una columna 'monto' en `excel_data` para el monto de la venta
            'Total Descuento': (x['pre_tot'] * (x['DESCUENTO']/100.0)).sum(),
            'Total a pagar proveedor': x['pre_tot'].sum() - (x['pre_tot'] * (x['DESCUENTO']/100.0)).sum()
        }))

        st.subheader("Consolidado Proveedores")
        st.dataframe(grupo_proveedores);


else:
    st.warning("No hay datos disponibles.")


if not proveedores_df.empty:
    st.title("Proveedores")
    st.write(proveedores_df)

if not ventas_con_descuento.empty:
    st.title("Ventas con descuento")
    st.write(ventas_con_descuento)

