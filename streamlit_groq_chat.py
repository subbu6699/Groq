import os
import streamlit as st
from groq import Groq

# Streamlit Page Configuration
st.set_page_config(page_title="Groq Model Chat", layout='wide')

# Sidebar Inputs
st.sidebar.header("Groq API Configuration")
api_key = st.sidebar.text_input("API Key", value=os.getenv("GROQ_API_KEY", ""), type="password")
base_url = st.sidebar.text_input("Base URL", "https://api.groq.com/openai/v1")

# Initialize Groq Client
def initialize_groq_client(api_key, base_url):
    return Groq(api_key=api_key, base_url=base_url)

# Fetch models with caching
@st.cache_data(show_spinner=False)
def get_models(api_key, base_url):
    client = initialize_groq_client(api_key, base_url)
    try:
        models = client.models.list()
        return {model["name"]: model["id"] for model in models}
    except Exception as e:
        st.sidebar.error(f"Error fetching models: {str(e)}")
        return {}

# Initialize Groq Client and Fetch Models
if api_key:
    models = get_models(api_key, base_url)

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
                client = initialize_groq_client(api_key, base_url)  # Initialize client here for sending messages
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
