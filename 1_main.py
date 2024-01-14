import streamlit as st

st.set_page_config(
    page_title="Streamlit Homepage", 
    page_icon=":smiley:"
)

st.title("Streamlit Homepage")
st.sidebar.title("Streamlit Homepage")

if "my_input" not in st.session_state:
    st.session_state["my_input"] = ""

my_input = st.text_input("Input", st.session_state["my_input"])
submit = st.button("Submit")
if submit:
    st.session_state["my_input"] = my_input
    st.write(f"Input: {my_input}")