import os
import google.generativeai as genai
import streamlit as st

# Set up predefined username and password
USERNAME = "zeinhasan531"
PASSWORD = "HasanZein531*"

# Function to verify login credentials
def login(username, password):
    return username == USERNAME and password == PASSWORD

# Function to get the selected model name
def get_model_name(model_choice):
    if model_choice == "Gemini 1.5 Flash":
        return "gemini-1.5-flash-latest"
    elif model_choice == "Gemini 1.5 Pro":
        return "gemini-1.5-pro-latest"
    else:
        return "gemini-1.0-pro"

# Initialize session state for dark mode
if 'dark_mode' not in st.session_state:
    st.session_state['dark_mode'] = False

# Login page logic
if 'logged_in' not in st.session_state:
    st.session_state['logged_in'] = False

if not st.session_state['logged_in']:
    st.title("Login")

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    
    if st.button("Login"):
        if login(username, password):
            st.session_state['logged_in'] = True
            st.success("Logged in successfully!")
        else:
            st.error("Invalid username or password")
else:
    # Sidebar settings
    st.sidebar.title("Settings")

    # Dark mode toggle
    st.session_state['dark_mode'] = st.sidebar.checkbox("Dark Mode", value=st.session_state['dark_mode'])

    # Model choice dropdown
    model_choice = st.sidebar.selectbox(
        "Choose Model:",
        ["Gemini 1.5 Flash", "Gemini 1.5 Pro", "Gemini 1.0 Pro"]
    )

    # Additional model parameters
    temperature = st.sidebar.slider("Temperature", 0.0, 1.0, 1.0)
    top_p = st.sidebar.slider("Top P", 0.0, 1.0, 0.95)
    top_k = st.sidebar.slider("Top K", 0, 100, 64)
    max_output_tokens = st.sidebar.slider("Max Output Tokens", 1, 8192, 8192)

    # Configure the selected model
    genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

    model_name = get_model_name(model_choice)

    generation_config = {
        "temperature": temperature,
        "top_p": top_p,
        "top_k": top_k,
        "max_output_tokens": max_output_tokens,
        "response_mime_type": "text/plain",
    }

    # Create the model instance
    model = genai.GenerativeModel(
        model_name=model_name,
        generation_config=generation_config
    )

    # System instruction
    system_instruction = (
        "Kamu adalah AI yang dibangun dan dilatih oleh Ahmad Habib Hasan Zein seorang Data Scientist dari PT Sreeya Sewu Tbk tanggal 8 September 2024, "
        "Kamu tidak boleh memberikan informasi yang berbau SARA (Suku Agama dan Ras), dan Hoax."
    )

    # Streamlit interface after login
    st.title("Generative AI Chat")

    # Display label for user input
    st.write("Your Input:")

    # Text input for user with custom label and key
    user_input = st.text_input("You: ", key="user_input")

    if user_input:
        # Create a chat session with the model and include system instruction in history
        chat_session = model.start_chat(
            history=[
                {"role": "system", "content": {"parts": [system_instruction]}}
            ]
        )

        # Send the message and get the response
        response = chat_session.send_message(user_input)

        # Display the response
        st.text_area("Response:", response.text, height=200)
