# streamlit_groq_chat.py
import os
import streamlit as st
from groq import Groq
from dotenv import load_dotenv

# Load environment variables from .env file (if available)
load_dotenv()

# Streamlit Page Configuration
st.set_page_config(page_title="Groq Model Chat", layout='wide')

# Sidebar Inputs
st.sidebar.header("Groq API Configuration")
api_key = st.sidebar.text_input("API Key", value=os.getenv("GROQ_API_KEY", ""), type="password")
base_url = st.sidebar.text_input("Base URL", "https://api.groq.com")

# Function to Initialize Groq Client
@st.cache_data(show_spinner=False)
def initialize_groq_client(api_key):
    return Groq(api_key=api_key)

# Initialize Groq Client if API Key is provided
if api_key:
    client = initialize_groq_client(api_key)

    # Fetch the list of available models
    def get_models(client):
        try:
            models = client.models.list()
            return {model["name"]: model["id"] for model in models}
        except Exception as e:
            st.sidebar.error(f"Error fetching models: {str(e)}")
            return {}

    # Retrieve models from Groq API
    models = get_models(client)

    # Sidebar Inputs for Model Selection
    model_name = st.sidebar.selectbox("Select Model", options=list(models.keys()))
    model_id = models.get(model_name, "")

    # Main Page Title
    st.title("Groq Model Chat Interface")
    st.markdown("""
    ### Chat with a Groq Model
    Enter your message, and the model will respond based on Groq API capabilities.
    """)

    # Input Text Box for User Message
    input_text = st.text_input("Enter your message:")

    # Send Button and Display Model Response
    if st.button("Send"):
        if not model_id:
            st.error("Please select a Model.")
        else:
            try:
                chat_completion = client.chat.completions.create(
                    messages=[{"role": "user", "content": input_text}],
                    model=model_id
                )
                response_text = chat_completion.choices[0].message.content
                st.markdown(f"**Model Response:** {response_text}")
            except Exception as e:
                st.error(f"Error: {str(e)}")
else:
    st.sidebar.error("Please provide a valid API Key.")
