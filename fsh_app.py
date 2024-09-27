import streamlit as st
from crewai import Agent, Task, Crew
import os
from langchain_community.chat_models import ChatCohere
import cohere

# Initialize language models
os.environ["COHERE_API_KEY"] = "SB1mJfw1oJpKhiCRAXWh7Ll4jHR2P0hF3dAMznrO"
llm = ChatCohere()
co = cohere.Client(os.getenv("COHERE_API_KEY"))

# Define the agents
# Agent 1: Fashion Analyzer (Asks questions and collects user responses)
fashion_analyzer = Agent(
    role="Fashion Analyzer",
    goal="Ask relevant fashion-related questions to understand the user's style.",
    backstory=(
        "You're a fashion consultant who asks personalized questions to understand user preferences such as style, color, "
        "comfort, brand preferences, and other important factors for recommending outfits."
    ),
    llm=llm,
    allow_delegation=False,
    verbose=True
)

# Agent 2: Fashion Stylist (Provides recommendations based on responses)
fashion_stylist = Agent(
    role="Fashion Stylist",
    goal="Provide tailored fashion recommendations based on the user's preferences.",
    backstory="You are a fashion expert who recommends styles based on the user's answers provided by the Fashion Analyzer.",
    llm=llm,
    allow_delegation=False,
    verbose=True
)

# Agent 3: Brand Researcher (Researches brands relevant to user preferences)
brand_researcher = Agent(
    role="Brand Researcher",
    goal="Suggest relevant fashion brands based on user preferences and location.",
    backstory="You specialize in researching and suggesting popular brands based on the user's preferences and country.",
    llm=llm,
    allow_delegation=False,
    verbose=True
)

# Define tasks
# Task 1: Collect user preferences (Handled by Fashion Analyzer)
collect_preferences_task = Task(
    description=(
        "Ask the user a series of questions about their fashion preferences, including style, color, fabric, and footwear choices. "
        "Store these preferences for generating recommendations."
    ),
    agent=fashion_analyzer
)

# Task 2: Generate fashion recommendations (Handled by Fashion Stylist)
recommendation_task = Task(
    description=(
        "Based on the user's fashion preferences, provide curated outfit recommendations that match their style and comfort."
    ),
    agent=fashion_stylist
)

# Task 3: Brand research (Handled by Brand Researcher)
brand_research_task = Task(
    description=(
        "Based on the user's preferences and country, research and suggest relevant fashion brands that align with their style."
    ),
    agent=brand_researcher
)

# Setup Crew for agent task orchestration
crew = Crew(
    agents=[fashion_analyzer, fashion_stylist, brand_researcher],
    tasks=[collect_preferences_task, recommendation_task, brand_research_task],
    verbose=2
)

# Streamlit interface
st.title("AI Fashion Stylist")

# Initialize session state
if "user_responses" not in st.session_state:
    st.session_state.user_responses = {}
if "task_completed" not in st.session_state:
    st.session_state.task_completed = False

# Step 1: Ask fashion questions and collect user preferences
if not st.session_state.task_completed:
    st.write("Let's learn more about your fashion preferences!")
    if "Preferred clothing style" not in st.session_state.user_responses:
        style = st.selectbox("What's your preferred clothing style?", ["Casual", "Formal", "Sporty", "Ethnic", "Others"])
        st.session_state.user_responses["Preferred clothing style"] = style
    if "Preferred colors" not in st.session_state.user_responses:
        colors = st.text_input("What colors do you usually wear?")
        st.session_state.user_responses["Preferred colors"] = colors
    if "Preferred brands" not in st.session_state.user_responses:
        brands = st.text_input("Any specific brands you prefer?")
        st.session_state.user_responses["Preferred brands"] = brands
    if "Preferred footwear" not in st.session_state.user_responses:
        footwear = st.selectbox("What type of footwear do you like?", ["Sneakers", "Formal shoes", "Heels", "Sandals", "Boots"])
        st.session_state.user_responses["Preferred footwear"] = footwear
    if "Country" not in st.session_state.user_responses:
        country = st.text_input("Which country are you from?")
        st.session_state.user_responses["Country"] = country

    # Proceed to recommendations
    if st.button("Submit Preferences"):
        st.session_state.task_completed = True

# Step 2: Generate recommendations and research brands
if st.session_state.task_completed:
    st.write("Generating your personalized fashion recommendations...")
    # Trigger the agent to start processing the tasks
    user_preferences = st.session_state.user_responses
    result = crew.kickoff(inputs={"user_preferences": user_preferences})

    # Display the results
    st.markdown("### Fashion Recommendations")
    st.markdown(result["recommendation_task"])  # Output from Fashion Stylist

    st.markdown("### Suggested Brands")
    st.markdown(result["brand_research_task"])  # Output from Brand Researcher

# Reset the session
if st.button("Start Over"):
    st.session_state.user_responses = {}
    st.session_state.task_completed = False
