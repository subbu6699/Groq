# streamlit_groq_chat.py
import streamlit as st
from groq_api import GroqAPI

# Streamlit Page Configuration
st.set_page_config(page_title="Groq Model Chat", layout='wide')

# Sidebar Inputs for API Key and Base URL
st.sidebar.header("Groq API Configuration")
api_key = st.sidebar.text_input("API Key (Enter here)", type="password")
base_url = st.sidebar.text_input("Base URL", "https://api.groq.com")

# Initialize GroqAPI instance only if API Key is provided
if api_key:
    groq_api = GroqAPI(api_key=api_key, base_url=base_url)

    # Fetch available models
    models = groq_api.get_available_models()
    if isinstance(models, list):  # Check if models were successfully retrieved
        model_choices = {model['name']: model['id'] for model in models}
    else:
        st.sidebar.error(f"Error fetching models: {models}")
        model_choices = {}
else:
    models = []
    model_choices = {}

# Sidebar Input for Model Selection
model_name = st.sidebar.selectbox("Select Model", options=list(model_choices.keys()))
model_id = model_choices.get(model_name)

# Main Page Title
st.title("Groq Model Chat Interface")
st.markdown("""
### Chat with a Groq Model
Enter your message, and the model will respond based on the Groq API's capabilities.
""")

# Input Text Box for User Message
input_text = st.text_input("Enter your message:")

# Send Button and Display Model Response
if st.button("Send"):
    if not api_key or not model_id:
        st.error("Please provide your API Key and select a Model.")
    else:
        response = groq_api.chat_with_model(model_id, input_text)
        st.markdown(f"**Model Response:** {response}")
