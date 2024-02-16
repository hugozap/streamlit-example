import altair as alt
import numpy as np
import pandas as pd
import streamlit as st


uploaded_files = st.file_uploader("Upload an Excel File", type="xlsx")


# Assuming 'excel_data' is loaded from the Excel file
if uploaded_files is not None:
    excel_data = pd.read_excel(uploaded_files)
    excel_data['tipo'] = excel_data['tipo'].astype(str)
    excel_data['item'] = excel_data['item'].astype(str)
    excel_data['llave'] = excel_data['item'].str[:3]

    # Identify all returns
    returns_df = excel_data[excel_data['tipo'] == '302']

    # Initialize an empty list for errors
    errors_list = []

    # Find indexes to remove (both returns and one corresponding transaction per return)
    indexes_to_remove = set(returns_df.index)
    for index, return_row in returns_df.iterrows():
        # Attempt to find a corresponding transaction
        transaction_idx = excel_data[(excel_data['item'] == return_row['item']) & (excel_data['tipo'] != '302')].index
        if transaction_idx.empty:
            errors_list.append({'item': return_row['item'], 'error_message': 'No corresponding transaction found for return'})
        else:
            # Add the first transaction index found to the list of indexes to remove
            indexes_to_remove.add(transaction_idx[0])

    # Convert the errors list to a DataFrame
    errors_df = pd.DataFrame(errors_list)

    # Drop the rows from the main DataFrame
    excel_data.drop(index=list(indexes_to_remove), inplace=True)

else:
    excel_data = pd.DataFrame()
    errors_df = pd.DataFrame()
    returns_df = pd.DataFrame()

# Display logic for Streamlit (assuming this is being used within a Streamlit app)
if len(excel_data) > 0:
    st.title('Updated Excel Data')
    st.write(excel_data)
else:
    st.warning("No Excel file uploaded or no valid data to display after processing.")

if not errors_df.empty:
    st.error("Errors Detected:")
    st.write(errors_df)

if len(returns_df) > 0:
    st.title("Returns Table")
    st.write(returns_df)
else:
    st.info("No returns found.")