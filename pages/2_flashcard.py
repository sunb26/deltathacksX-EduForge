import streamlit as st
from src.crud.read import read_topic

st.title("Flashcards")

# Dropdown menu options

if 'dropdown_options' not in st.session_state:
    st.session_state.dropdown_options = read_topic("joe")  # Replace these with your actual options

# Add a dropdown menu under the title
current_selection = st.selectbox("Choose an option:", st.session_state.dropdown_options, key='current_selection')

# Check if the selection has changed and update the session state variable
if 'selected_option' not in st.session_state or st.session_state.selected_option != current_selection:
    st.session_state.selected_option = current_selection

    
# Simulating a database of flashcards
flashcards = [
    {"question": "Who is credited with inventing Champagne?", "answer": "Dom Perignon"},
    {"question": "Who is credited with inventing Champagne 2?", "answer": "Dom Perignon 2"},
    # ... (more flashcards can be added here)
]

# Initialize session state variables if they don't exist
if 'current_card' not in st.session_state:
    st.session_state.current_card = 0
if 'show_answer' not in st.session_state:
    st.session_state.show_answer = False

# Function to show the current flashcard
def show_flashcard():
    card = flashcards[st.session_state.current_card]
    
    # Container for the flashcard
    with st.container():
        # Custom CSS to create the flashcard effect
        st.markdown(
            f'''
            <div style="border: 2px solid #f0f2f6; border-radius: 10px; padding: 150px; text-align: center; background-color: white;">
                <h2>{card['question']}</h2>
            </div>
            ''',
            unsafe_allow_html=True
        )
        
        # Create a placeholder for the answer above the button
        answer_placeholder = st.empty()

        # Use a button to toggle the answer, changing the text based on whether the answer is shown
        button_label = "Click to reveal the answer" if not st.session_state.show_answer else "Click to hide answer"
        if st.button(button_label, key="question_button"):
            # Toggle the show_answer state
            st.session_state.show_answer = not st.session_state.show_answer
            # Rerun the script to update the button label immediately
            st.rerun()

        # If the answer is to be shown, display it in the placeholder
        if st.session_state.show_answer:
            answer_placeholder.markdown(f"**Answer:** {card['answer']}")
        else:
            answer_placeholder.empty()

# Function to navigate to the previous flashcard
def prev_card():
    st.session_state.current_card = (st.session_state.current_card - 1) % len(flashcards)
    st.session_state.show_answer = False

# Function to navigate to the next flashcard
def next_card():
    st.session_state.current_card = (st.session_state.current_card + 1) % len(flashcards)
    st.session_state.show_answer = False


# Display the flashcard
show_flashcard()

# Navigation buttons, adjust columns to align 'Next' with the right edge of the flashcard box
button_cols = st.columns([1, 5, 1])
with button_cols[0]:
    st.button("Previous", on_click=prev_card)
with button_cols[2]:
    st.button("Next", on_click=next_card)
