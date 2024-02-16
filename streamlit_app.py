import altair as alt
import numpy as np
import pandas as pd
import streamlit as st


uploaded_files = st.file_uploader("Upload an Excel File", type="xlsx")


if uploaded_files is not None:
    excel_data = pd.read_excel(uploaded_files)
    # Ensure 'tipo' and 'item' are treated as strings for consistent comparison
    excel_data['tipo'] = excel_data['tipo'].astype(str)
    excel_data['item'] = excel_data['item'].astype(str)
    excel_data['llave'] = excel_data['item'].str[:3]

    # Separate DataFrame for returns and errors
    returns_df = excel_data[excel_data['tipo'] == '302'].copy()
    errors = pd.DataFrame(columns=['item', 'error_message'])

    # Identifying transactions to remove
    transactions_to_remove = pd.DataFrame()
    for _, return_row in returns_df.iterrows():
        transactions = excel_data[(excel_data['item'] == return_row['item']) & (excel_data['tipo'] != '302')]
        if transactions.empty:
            error_entry = {'item': return_row['item'], 'error_message': 'No corresponding transaction found for return'}
            errors = errors.append(error_entry, ignore_index=True)
        else:
            # Assuming we remove the first matching transaction found
            transaction_to_remove = transactions.iloc[0]
            transactions_to_remove = transactions_to_remove.append(transaction_to_remove)

    # Remove transactions and returns from the main DataFrame
    excel_data = excel_data.drop(returns_df.index)
    excel_data = excel_data.drop(transactions_to_remove.index).reset_index(drop=True)

else:
    excel_data = pd.DataFrame()
    errors = pd.DataFrame()
    returns_df = pd.DataFrame()

# Display the updated data, errors, and the separate returns table
if len(excel_data) > 0:
    st.title('Updated Excel Data')
    st.write(excel_data)
else:
    st.warning("No Excel file uploaded or no valid data to display after processing.")

if not errors.empty:
    st.error("Errors Detected:")
    st.write(errors)

if len(returns_df) > 0:
    st.title("Returns Table")
    st.write(returns_df)
else:
    st.info("No returns found.")
