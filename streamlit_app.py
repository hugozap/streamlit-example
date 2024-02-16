import altair as alt
import numpy as np
import pandas as pd
import streamlit as st


if uploaded_files is not None:
    excel_data = pd.read_excel(uploaded_files)
    # Add 'llave' column by slicing the first 3 characters of the 'item' column
    excel_data['llave'] = excel_data['item'].astype(str).str[:3]
else:
    excel_data = pd.DataFrame()

# Process and display the data in Streamlit
if len(excel_data) > 0:
    st.title('Excel Data Processing App')
    st.write(excel_data.head())  # Adjust the number in head() if you want to display more rows
else:
    st.warning("No Excel file uploaded. Please upload a valid XLSX file to continue.")
