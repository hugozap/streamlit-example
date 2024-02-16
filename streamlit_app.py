import altair as alt
import numpy as np
import pandas as pd
import streamlit as st


uploaded_files = st.file_uploader("Upload an Excel File", type="xlsx")

import pandas as pd

# Assuming 'excel_data' is your DataFrame loaded from the Excel file
if uploaded_files is not None:
    excel_data = pd.read_excel(uploaded_files)
    excel_data['llave'] = excel_data['item'].astype(str).str[:3]

    # Initialize an empty DataFrame for errors
    errors = pd.DataFrame(columns=['item', 'error_message'])

    # Find all "302" returns
    returns = excel_data[excel_data['tipo'] == '302']

    # Track rows to be removed (both returns and their corresponding transactions, if found)
    rows_to_drop = set()

    for _, return_row in returns.iterrows():
        # Check for a corresponding transaction
        transactions = excel_data[(excel_data['item'] == return_row['item']) & (excel_data['tipo'] != '302')]
        
        if transactions.empty:
            # Log error if no corresponding transaction is found
            errors = errors.append({'item': return_row['item'], 'error_message': 'No corresponding transaction found for return'}, ignore_index=True)
        else:
            # Get the index of the first matching transaction
            transaction_index = transactions.index[0]
            rows_to_drop.add(transaction_index)

        # Always add the return row to the rows to be dropped
        rows_to_drop.add(return_row.name)

    # Drop both returns and transactions
    excel_data.drop(index=list(rows_to_drop), inplace=True)

else:
    excel_data = pd.DataFrame()
    errors = pd.DataFrame()

# Display updated data and any errors
if len(excel_data) > 0:
    st.title('Updated Excel Data')
    st.write(excel_data)
else:
    st.warning("No Excel file uploaded or no valid data to display after processing.")

if not errors.empty:
    st.error("Errors Detected:")
    st.write(errors)
else:
    st.success("No errors detected in returns processing.")
