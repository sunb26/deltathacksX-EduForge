
import streamlit as st

st.title("Flashcards")
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
        
        # Create a placeholder for the answer
        answer_placeholder = st.empty()
        
        # Use a button to toggle the answer
        if st.button("Click to reveal the answer", key="question_button"):
            st.session_state.show_answer = not st.session_state.show_answer
        
        # If the answer is to be shown, display it in the placeholder above the button
        if st.session_state.show_answer:
            answer_placeholder.markdown(f"**Answer:** {card['answer']}")

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

# Navigation buttons
col1, col2, col3 = st.columns([8, 10, 8])
with col1:
    st.button("Previous", on_click=prev_card)
with col3:
    st.button("Next", on_click=next_card)
