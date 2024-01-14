import json 
import requests 
import streamlit as st 
from streamlit_lottie import st_lottie 
from src.convert import pdf_to_html
from src.chunk import chunk_html
import io
from src.crud.read import read_topic
from src.crud.write import new_qa, new_flashcard, new_topic
from src.generate import generate

url = requests.get( 
# Fetch Lottie animation JSON
    "https://lottie.host/4fc7f4b7-8f35-4180-b4a2-582640972370/yucw3rNo6u.json"
) 

url_json = dict() 

if url.status_code == 200: 
    url_json = url.json() 
else: 
    print("Error in the URL") 

# Set width and height parameters as per your requirement
width = 725  # Adjust the width accordingly
height = 200  # Adjust the height accordingly

# Use columns to create a layout with two columns
col1, col2 = st.columns([1, 3])

# Custom CSS to reduce the padding between columns
col2_css = f"<style>div.st-cg {{ padding-right: 0; }}</style>"
st.markdown(col2_css, unsafe_allow_html=True)

# In the first column (col1), add the title, subtitle, and Lottie animation
with col1:
    st.title("EduForge")    
    st.subheader("One Stop Study Shop")

with col2:
    st_lottie(url_json, width=width, height=height)

# Initial selections for the select box
if 'options' not in st.session_state:
    st.session_state.options = read_topic("joe")

# Display the select box
selected_option = st.sidebar.selectbox(
    'Choose a topic',
    st.session_state.options
)

st.sidebar.write('You selected:', selected_option)

# Use a form to get user input for a new selection
with st.sidebar.form("add_selection_form"):
    newTopic = st.text_input("Enter new selection:")
    submit_button = st.form_submit_button("Add Selection")


# If the form is submitted, add the new selection to the options
if submit_button and newTopic:
    if newTopic not in st.session_state.options:  # Check to avoid duplicates
        st.session_state.options.append(newTopic)
        # Update the select box with the new list of options
        selected_option = newTopic
        st.sidebar.write("New topic:", newTopic)
        st.sidebar.write("Topic list:", st.session_state.options)
        new_topic("joe", newTopic)
        st.rerun()


st.markdown(
    """
    ## About Us
    EduForge is a pioneering educational software service designed to revolutionize the way students learn. Born from a blend of expert educational insights and cutting-edge technology, our platform specializes in creating adaptive practice problems and flashcards. Tailored to each student's unique learning style and pace, EduForge ensures a personalized educational experience, making learning more effective and engaging. Whether tackling complex equations or exploring new subjects, EduForge adapts to individual needs, turning every study session into a step towards academic excellence.
    
    Our commitment extends beyond students to educators, offering a suite of tools for creating custom content, tracking progress, and enhancing teaching methods. EduForge stands at the intersection of traditional education and digital innovation, providing a dynamic, interactive learning environment for all. 
    
    #### Join us in shaping the future of education, where every challenge is an opportunity to learn and grow."""
    )
uploaded = st.sidebar.file_uploader("Choose a file", type="pdf", accept_multiple_files=False)

if uploaded:
    # Convert the uploaded file to a BytesIO object
    pdf_stream = io.BytesIO(uploaded.read())

    # Call your conversion function with the BytesIO object
    html_content = pdf_to_html(pdf_stream)

    chunks = chunk_html(selected_option, html_content)

    res = generate("flashcard", "joe", selected_option)
    
    print("logging new flashcards")
    new_flashcard("joe", selected_option, res)

    st.write(res)

    res = generate("qa", "joe", selected_option)

    print("logging new qas")
    new_qa("joe", selected_option, res)
    

    st.write(res)
    
