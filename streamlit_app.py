import altair as alt
import numpy as np
import pandas as pd
import streamlit as st


uploaded_files = st.file_uploader("Upload an Excel File", type="xlsx")


if uploaded_files is not None:
    excel_data = pd.read_excel(uploaded_files)
    excel_data['llave'] = excel_data['item'].astype(str).str[:3]

    # Initialize an empty DataFrame for errors
    errors = pd.DataFrame(columns=['item', 'error_message'])

    # Identifying rows to drop (returns with corresponding transactions)
    rows_to_drop = []

    for index, row in excel_data.iterrows():
        if row['tipo'] == '302':
            # Find a matching transaction for this return
            matching_transactions = excel_data[(excel_data['item'] == row['item']) & (excel_data['tipo'] != '302')]
            
            if matching_transactions.empty:
                # No corresponding transaction found; log an error
                errors = errors.append({'item': row['item'], 'error_message': 'No corresponding transaction for return'}, ignore_index=True)
            else:
                # Assuming we remove the first matching transaction found
                transaction_to_remove = matching_transactions.index[0]
                rows_to_drop.append(transaction_to_remove)  # Add transaction row to the list of rows to drop
            
            # Add return row index to the list of rows to drop
            rows_to_drop.append(index)

    # Remove identified rows from the main DataFrame
    excel_data = excel_data.drop(rows_to_drop)

else:
    excel_data = pd.DataFrame()
    errors = pd.DataFrame()  # Ensure errors DataFrame is defined even if no file is uploaded

# Process and display the updated data and errors in Streamlit
if len(excel_data) > 0:
    st.title('Excel Data Processing App')
    st.write(excel_data)  # Adjust the number in head() if you want to display more rows
else:
    st.warning("No Excel file uploaded. Please upload a valid XLSX file to continue.")

if not errors.empty:
    st.error("Errors Detected:")
    st.write(errors)
else:
    st.success("No errors detected.")