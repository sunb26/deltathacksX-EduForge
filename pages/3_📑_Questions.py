import json 
import requests 
import streamlit as st 

import base64

from src.functionalities.createPDF import pdfCreate
from src.crud.read import read_qa

st.title("Questions")

def display_pdf(file):
    # Opening file from file path
    with open(file, "rb") as f:
        base64_pdf = base64.b64encode(f.read()).decode('utf-8')

    # Embedding PDF in HTML
    pdf_display = F'<iframe src="data:application/pdf;base64,{base64_pdf}" width="900" height="700" type="application/pdf"></iframe>'

    # Displaying File
    st.markdown(pdf_display, unsafe_allow_html=True)


if 'options' not in st.session_state:
    st.session_state.options = ['Anatomy', 'History', 'Geography']

# Display the select box
selected_option = st.sidebar.selectbox(
    'Select a topic',
    st.session_state.options
)

st.sidebar.write('You selected:', selected_option)

if selected_option:
    res = read_qa("joe", selected_option)

    content_string = ""
    for pair in res:
        content_string += f"Q: {pair[0]}\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\nA: {pair[1]}\n\n"

    pdfCreate(content_string, selected_option.lower())

    display_pdf(f"pdfs/{selected_option}.pdf")