import streamlit as st
from groq import Groq

# Initialize Groq client with the provided API key
api_key = "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"
client = Groq(api_key=api_key)

# Function to call the Groq API for fashion suggestions
def generate_fashion_suggestions(personal_style, favorite_colors, preferred_materials, body_type, fashion_goals):
    user_message = {
        "role": "user",
        "content": (
            f"Personal style: {personal_style} \n"
            f"Favorite colors: {favorite_colors} \n"
            f"Preferred materials: {preferred_materials} \n"
            f"Body type: {body_type} \n"
            f"Fashion goals: {fashion_goals}"
        )
    }
    
    chat_completion = client.chat.completions.create(
        messages=[
            {
                "role": "system",
                "content": (
                    "Your task is to suggest avant-garde fashion trends and styles tailored to the user's preferences. "
                    "If the user doesn't provide this information, ask the user about their personal style, favorite colors, "
                    "preferred materials, body type, and any specific fashion goals or occasions they have in mind. "
                    "Generate creative, bold, and unconventional fashion suggestions that push the boundaries of traditional style "
                    "while considering the user's individual taste. Provide detailed descriptions, key pieces, and styling tips."
                )
            },
            user_message
        ],
        model="llama3-8b-8192",
        temperature=0.5,
        max_tokens=1024,
        top_p=1,
        stop=None,
        stream=False
    )
    
    return chat_completion.choices[0].message.content

# Streamlit app layout
st.title("AI Fashion Stylist")
st.write("Get avant-garde fashion trends and style suggestions tailored to your preferences.")

# Initialize session state for chat history
if "messages" not in st.session_state:
    st.session_state["messages"] = []

# Input fields for user preferences
personal_style = st.text_input("Personal style", "Edgy, minimal, with a touch of androgyny")
favorite_colors = st.text_input("Favorite colors", "Black, white, and deep red")
preferred_materials = st.text_input("Preferred materials", "Leather, denim, and high-quality cotton")
body_type = st.text_input("Body type", "Tall and lean")
fashion_goals = st.text_input("Fashion goals", "To create a striking, fearless look for an art gallery opening")

# Button to generate new suggestions
if st.button("Generate Fashion Suggestions"):
    suggestion = generate_fashion_suggestions(personal_style, favorite_colors, preferred_materials, body_type, fashion_goals)
    st.session_state["messages"].append(suggestion)

# Display suggestions
st.subheader("Fashion Suggestions")
for message in st.session_state["messages"]:
    st.write(message)

# Button to reset chat
if st.button("Reset Chat"):
    st.session_state["messages"] = []
    st.write("Chat reset. Please enter your preferences again.")
