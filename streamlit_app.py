import altair as alt
import numpy as np
import pandas as pd
import streamlit as st


uploaded_files = st.file_uploader("Upload an Excel File", type="xlsx")


# Assuming 'excel_data' is your DataFrame loaded from the Excel file
if uploaded_files is not None:
    excel_data = pd.read_excel(uploaded_files)
    excel_data['llave'] = excel_data['item'].astype(str).str[:3]

    # Initialize an empty DataFrame for errors
    errors = pd.DataFrame(columns=['item', 'error_message'])

    # Separate DataFrame for returns
    returns_df = excel_data[excel_data['tipo'] == '302'].copy()

    # Track rows to be removed from the main DataFrame
    rows_to_drop = set()

    for _, return_row in returns_df.iterrows():
        # Attempt to find a corresponding transaction
        transactions = excel_data[(excel_data['item'] == return_row['item']) & (excel_data['tipo'] != '302')]
        
        if transactions.empty:
            # If no transaction is found, log an error
            errors = errors.append({'item': return_row['item'], 'error_message': 'No corresponding transaction found for return'}, ignore_index=True)
        else:
            # If a transaction is found, mark the first one for removal
            transaction_index = transactions.index[0]
            rows_to_drop.add(transaction_index)

        # Mark the return row for removal from the main DataFrame
        rows_to_drop.add(return_row.name)

    # Remove the marked returns and transactions from the main DataFrame
    excel_data.drop(index=list(rows_to_drop), inplace=True)

else:
    excel_data = pd.DataFrame()
    errors = pd.DataFrame()
    returns_df = pd.DataFrame()  # Ensure returns_df is defined even if no file is uploaded

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
