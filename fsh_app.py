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

# Function to ask questions in sequence
def ask_next_question(state):
    if state["question_index"] < len(fashion_questions):
        question = fashion_questions[state["question_index"]]
        state["question_index"] += 1
        return question
    else:
        return "Thank you for answering all the questions. How can I assist you further?"

# Function to handle the conversation with Cohere API
def get_response(message, system_message, max_tokens, temperature, top_p, history):
    # Add system message and history to the conversation prompt
    prompt = system_message + "\n" + "\n".join([f"User: {h['user']}\nAssistant: {h['assistant']}" for h in history])

    # Append the current message
    prompt += f"\nUser: {message}\nAssistant:"

    # Call Cohere API
    response = co.generate(
        prompt=prompt[:1000],  # Limit prompt length to avoid issues
        max_tokens=max_tokens,
        temperature=temperature,
        p=top_p
    )

    # Extract assistant's reply
    return response.generations[0].text.strip()[:500]  # Limit reply length

# Streamlit UI
st.title("Fashion Recommender Chatbot")

# System message input
system_message = st.text_input("System message", value="You are a fashion expert.")

# User details input
gender = st.radio("Gender", ["Male", "Female", "Other"])
age = st.number_input("Age", min_value=1, max_value=120, value=25)
ethnicity = st.text_input("Ethnicity")

# Cohere settings sliders
max_tokens = st.slider("Max tokens", 1, 2048, 512)
temperature = st.slider("Temperature", 0.1, 4.0, 0.7)
top_p = st.slider("Top-p (nucleus sampling)", 0.1, 1.0, 0.95)

# Initialize conversation state
if "history" not in st.session_state:
    st.session_state.history = []
    st.session_state.question_index = 0

# Display conversation history
for chat in st.session_state.history:
    st.write(f"**User**: {chat['user']}")
    st.write(f"**Assistant**: {chat['assistant']}")

# User input box
user_message = st.text_input("Your message", key="user_input")

# When user submits a message
if st.button("Send"):
    if user_message:
        # Ask next fashion question if available
        question = ask_next_question(st.session_state)

        # Generate assistant response using Cohere API
        assistant_response = get_response(
            user_message, system_message, max_tokens, temperature, top_p, st.session_state.history
        )

        # Update conversation history
        st.session_state.history.append({"user": user_message, "assistant": assistant_response})

        # Display next question if available
        if question:
            st.write(f"**Assistant**: {question}")

# Reset the conversation
if st.button("Reset Chat"):
    st.session_state.history = []
    st.session_state.question_index = 0
