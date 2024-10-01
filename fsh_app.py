import streamlit as st
from groq import Groq

# Initialize Groq client with the provided API key
api_key = "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"
client = Groq(api_key=api_key)

# Function to call the Groq API for fashion suggestions and general queries
def chat_with_stylist(messages):
    chat_completion = client.chat.completions.create(
        messages=messages,
        model="llama3-8b-8192",
        temperature=0.5,
        max_tokens=1024,
        top_p=1,
        stop=None,
        stream=False
    )
    return chat_completion.choices[0].message.content

# Streamlit app layout
st.title("AI Fashion Stylist Chatbot")
st.write("Chat with our AI-powered fashion stylist for avant-garde style suggestions or general fashion advice.")

# Initialize session state for chat history and messages
if "messages" not in st.session_state:
    st.session_state["messages"] = [
        {
            "role": "system",
            "content": (
                "You are an AI fashion stylist. Your task is to provide avant-garde fashion suggestions, "
                "as well as general fashion advice based on the user's input. You can also engage in casual fashion discussions. "
                "Ask about their preferences, such as age, gender, ethnicity, personal style, favorite colors, "
                "preferred materials, body type, and any specific fashion goals."
            )
        }
    ]

# Input fields for user preferences (age, ethnicity, gender)
age = st.text_input("Age", "")
ethnicity = st.text_input("Ethnicity", "")
gender = st.selectbox("Gender", ["Male", "Female", "Non-binary", "Prefer not to say", "Other"])

# General input for style preferences (no specific colors or styles)
personal_style = st.text_input("Personal style", "")
preferred_materials = st.text_input("Preferred materials", "")
body_type = st.text_input("Body type", "")
fashion_goals = st.text_input("Fashion goals", "")

# Chat box for ongoing conversation
user_input = st.text_input("Ask anything related to fashion or continue the conversation:", "")

# Button to submit user input
if st.button("Send"):
    # Append user message to chat history
    st.session_state["messages"].append({"role": "user", "content": user_input})

    # Call Groq API with chat history
    response = chat_with_stylist(st.session_state["messages"])

    # Append assistant response to chat history
    st.session_state["messages"].append({"role": "assistant", "content": response})

    # Display the conversation so far
    st.subheader("Chat History")
    for message in st.session_state["messages"]:
        st.write(f"{message['role'].capitalize()}: {message['content']}")

# Button to generate fashion suggestions based on input fields
if st.button("Generate Fashion Suggestions"):
    # Prepare user preferences for generating fashion suggestions
    fashion_preferences = f"Age: {age}, Ethnicity: {ethnicity}, Gender: {gender}, Personal style: {personal_style}, Preferred materials: {preferred_materials}, Body type: {body_type}, Fashion goals: {fashion_goals}"

    # Append user message to chat history with preferences
    st.session_state["messages"].append({"role": "user", "content": fashion_preferences})

    # Call Groq API with updated chat history
    fashion_response = chat_with_stylist(st.session_state["messages"])

    # Append assistant response to chat history
    st.session_state["messages"].append({"role": "assistant", "content": fashion_response})

    # Display the fashion suggestions and conversation so far
    st.subheader("Fashion Suggestions and Chat History")
    for message in st.session_state["messages"]:
        st.write(f"{message['role'].capitalize()}: {message['content']}")

# Button to reset chat (start a new chat)
if st.button("Start New Chat"):
    st.session_state["messages"] = [
        {
            "role": "system",
            "content": (
                "You are an AI fashion stylist. Your task is to provide avant-garde fashion suggestions, "
                "as well as general fashion advice based on the user's input. You can also engage in casual fashion discussions. "
                "Ask about their preferences, such as age, gender, ethnicity, personal style, favorite colors, "
                "preferred materials, body type, and any specific fashion goals."
            )
        }
    ]
    st.write("Chat has been reset. You can start a new conversation.")
