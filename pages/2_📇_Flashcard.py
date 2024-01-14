import streamlit as st
from src.crud.read import read_topic, read_flashcard

st.title("Flashcards")

st.session_state.dropdown_options = read_topic("joe")  

current_selection = st.selectbox("Choose an option:", st.session_state.dropdown_options, key='current_selection')

if 'selected_option' not in st.session_state or st.session_state.selected_option != current_selection:
    st.session_state.selected_option = current_selection

    
if 'st.session_state.flashcards' not in st.session_state:
    st.session_state.flashcards = read_flashcard("joe", current_selection)

if 'current_card' not in st.session_state:
    st.session_state.current_card = 0
if 'show_answer' not in st.session_state:
    st.session_state.show_answer = False

# Function to show the current flashcard
def show_flashcard():
    card = st.session_state.flashcards[st.session_state.current_card]
    
    with st.container():
        st.markdown(
            f'''
            <div style="border: 2px solid #f0f2f6; border-radius: 10px; padding: 150px; text-align: center; background-color: white;">
                <h2>{card['question']}</h2>
            </div>
            ''',
            unsafe_allow_html=True
        )
        
        
        answer_placeholder = st.empty()

        
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
    st.session_state.current_card = (st.session_state.current_card - 1) % len(st.session_state.flashcards)
    st.session_state.show_answer = False

# Function to navigate to the next flashcard
def next_card():
    st.session_state.current_card = (st.session_state.current_card + 1) % len(st.session_state.flashcards)
    st.session_state.show_answer = False


# Display the flashcard
show_flashcard()

# Navigation buttons, adjust columns to align 'Next' with the right edge of the flashcard box
button_cols = st.columns([1, 5, 1])
with button_cols[0]:
    st.button("Previous", on_click=prev_card)
with button_cols[2]:
    st.button("Next", on_click=next_card)
