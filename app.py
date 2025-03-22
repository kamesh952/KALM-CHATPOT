import streamlit as st
import google.generativeai as genai
from datetime import datetime

# Set up Gemini API Key
genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])

# Check available models
available_models = [model.name for model in genai.list_models()]
def get_best_model():
    preferred_models = [
        "models/gemini-1.5-pro-latest", 
        "models/gemini-1.5-flash-latest"
    ]
    for model in preferred_models:
        if model in available_models:
            return model
    return available_models[0] if available_models else ""

# Initialize Gemini Model
model_name = get_best_model()
if not model_name:
    
    st.error("No available Gemini models found. Please check your API access.")
    st.stop()
model = genai.GenerativeModel(model_name)

# Streamlit UI
st.set_page_config(page_title="AI Chatbot", page_icon="🤖", layout="wide")
st.title("🤖 KALM AI Chatbot")
st.write("Chat with your AI assistant!")

# Sign-in button on top right
st.sidebar.title("User Settings")
if st.sidebar.button("Sign In"):
    st.sidebar.success("Sign-in feature coming soon!")

# Sidebar for chat history
st.sidebar.title("Chat History")
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# Clear chat history button
if st.sidebar.button("Clear Chat History"):
    st.session_state.chat_history = []
    st.rerun()

# Layout with two columns: Sidebar for history, main for chat
col1, col2 = st.columns([1, 3])

with col1:
    st.sidebar.write("**Previous Messages:**")
    for message in st.session_state.chat_history:
        if message["role"] == "user":
            st.sidebar.write(f"🧑 {message['timestamp']} - {message['content']}")
        else:
            st.sidebar.write(f"🤖 {message['timestamp']} - {message['content']}")

with col2:
    chat_container = st.container()
    with chat_container:
        for message in st.session_state.chat_history:
            with st.chat_message(message["role"]):
                st.markdown(f"**{message['timestamp']}**  ")
                st.write(message["content"])

# User input
user_input = st.chat_input("Type your message...")
if user_input:
    user_message = {
        "role": "user",
        "content": user_input,
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    }
    st.session_state.chat_history.append(user_message)
    
    with st.chat_message("user"):
        st.markdown(f"**{user_message['timestamp']}**  ")
        st.write(user_message["content"])

    # Generate response from Gemini
    try:
        with st.spinner("Thinking..."):
            response = model.generate_content(user_input)
            assistant_response = response.text if hasattr(response, 'text') else "I'm sorry, I couldn't generate a response."
    except Exception as e:
        assistant_response = f"Error: {str(e)}"
    
    assistant_message = {
        "role": "assistant",
        "content": assistant_response,
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    }
    st.session_state.chat_history.append(assistant_message)
    
    with st.chat_message("assistant"):
        st.markdown(f"**{assistant_message['timestamp']}**  ")
        st.write(assistant_message["content"])
