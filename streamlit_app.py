import altair as alt
import numpy as np
import pandas as pd
import streamlit as st

# Initialize empty DataFrames
excel_data = pd.DataFrame()
errors_df = pd.DataFrame()
returns_df = pd.DataFrame()

uploaded_files = st.file_uploader("Upload an Excel File", type="xlsx")

if uploaded_files is not None:
    excel_data = pd.read_excel(uploaded_files)
    excel_data['tipo'] = excel_data['tipo'].astype(str)
    excel_data['item'] = excel_data['item'].astype(str)
    excel_data['llave'] = excel_data['item'].str[:3]

    # Identify all returns after loading and preprocessing the data
    returns_df = excel_data[excel_data['tipo'] == '302']

    # The rest of your logic follows...
    errors_list = []

    # Logic to find indexes to remove and handle errors
    indexes_to_remove = set()
    for index, return_row in returns_df.iterrows():
        transaction_idx = excel_data[(excel_data['item'] == return_row['item']) & (excel_data['tipo'] != '302')].index
        if transaction_idx.empty:
            errors_list.append({'item': return_row['item'], 'error_message': 'No corresponding transaction found for return'})
        else:
            indexes_to_remove.add(index)  # Add the return index
            indexes_to_remove.add(transaction_idx[0])  # Add the first transaction index found

    # Convert the errors list to a DataFrame
    errors_df = pd.DataFrame(errors_list)

    # Drop the rows from the main DataFrame
    excel_data.drop(index=list(indexes_to_remove), inplace=True)

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
        st.subheader(f"Table for cod_cco: {cod_cco}")
        st.dataframe(filtered_df)
else:
    st.warning("No hay datos disponibles.")