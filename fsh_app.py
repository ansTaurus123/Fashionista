import streamlit as st
import cohere

# Set the Cohere API key
COHERE_API_KEY = "SB1mJfw1oJpKhiCRAXWh7Ll4jHR2P0hF3dAMznrO"
co = cohere.Client(COHERE_API_KEY)

# Define fashion-related questions
fashion_questions = [
    "Preferred clothing style? (casual, formal, sporty, etc.)",
    "What colors do you usually wear?",
    "Do you prefer any specific brands?",
    "What type of footwear do you like?",
    "Do you follow fashion trends?",
    "Is comfort or style more important?",
    "Do you like accessories?",
    "Favorite season for fashion?",
    "Any fabric preferences?"
]

# Function to ask questions in sequence and record answers
def ask_next_question(state):
    if state["question_index"] < len(fashion_questions):
        question = fashion_questions[state["question_index"]]
        state["question_index"] += 1
        return question
    else:
        return "You've completed the questionnaire! Let me provide some recommendations."

# Function to provide recommendations
def provide_recommendations(answers, country=None):
    recommendations = f"Based on your preferences:\n"
    recommendations += f"1. Style: {answers.get('style', 'Not specified')}\n"
    recommendations += f"2. Colors: {answers.get('colors', 'Not specified')}\n"
    recommendations += f"3. Footwear: {answers.get('footwear', 'Not specified')}\n"

    if country:
        recommendations += f"\nSome popular fashion brands from {country}:\n"
        if country.lower() == "pakistan":
            recommendations += "- Khaadi\n- Gul Ahmed\n- Sapphire\n"
        elif country.lower() == "usa":
            recommendations += "- Nike\n- Levi's\n- Tommy Hilfiger\n"
        # Add more countries as needed

    return recommendations

# Streamlit UI
st.title("Fashion Recommender Chatbot")

# System message input
system_message = st.text_input("System message", value="You are a fashion expert.")

# Cohere settings sliders
max_tokens = st.slider("Max tokens", 1, 2048, 512)
temperature = st.slider("Temperature", 0.1, 4.0, 0.7)
top_p = st.slider("Top-p (nucleus sampling)", 0.1, 1.0, 0.95)

# Initialize conversation state
if "history" not in st.session_state:
    st.session_state.history = []
    st.session_state.question_index = 0

# Initialize the `answers` dictionary in session state if it's not there
if "answers" not in st.session_state:
    st.session_state.answers = {}

# Ask next question
question = ask_next_question(st.session_state)
st.write(f"**Assistant**: {question}")

# User input box for answers
user_response = st.text_input("Your answer", key="user_response")

# When user submits a response
if st.button("Next"):
    if user_response:
        # Record answer to the current question
        current_question = fashion_questions[st.session_state.question_index - 1]
        # Store the user's response in the `answers` dictionary
        st.session_state.answers[current_question] = user_response
        
        # Check if all questions are answered
        if st.session_state.question_index < len(fashion_questions):
            st.write(f"**Next Question**: {ask_next_question(st.session_state)}")
        else:
            # Provide recommendations
            country = st.text_input("Enter country for brand recommendations (e.g., Pakistan)", value="")
            recommendations = provide_recommendations(st.session_state.answers, country)
            st.write(f"**Recommendations**: {recommendations}")

# Reset the conversation
if st.button("Reset Chat"):
    st.session_state.history = []
    st.session_state.question_index = 0
    st.session_state.answers = {}
