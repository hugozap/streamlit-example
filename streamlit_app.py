import altair as alt
import numpy as np
import pandas as pd
import streamlit as st


uploaded_files = st.file_uploader("Upload an Excel File", type="xlsx")
if uploaded_files is not None:
    excel_data = pd.read_excel(uploaded_files)
else:
    excel_data = pd.DataFrame()

# Process and display the data in Streamlit
if len(excel_data) > 0:
    st.title('Excel Data Processing App')
    st.write(excel_data)
else:
    st.warning("No Excel file uploaded. Please upload a valid XLSX file to continue.")

