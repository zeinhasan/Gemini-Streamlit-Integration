import streamlit as st
import os
from config import Config
from utils import apply_css, initialize_session, get_model_name, create_chat_session

def main():
    st.set_page_config(page_title="Chatbot with Gemini Models", layout="wide")

    initialize_session()

    # Check if user is logged in
    if 'logged_in' not in st.session_state:
        st.session_state['logged_in'] = False

    if not st.session_state['logged_in']:
        st.title("Login")

        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        
        # Retrieve credentials from environment variables
        valid_username = os.getenv("LOGIN_USERNAME")
        valid_password = os.getenv("LOGIN_PASSWORD")

        if st.button("Login"):
            if username == valid_username and password == valid_password:
                st.session_state['logged_in'] = True
                st.success("Logged in successfully!")
            else:
                st.error("Invalid username or password")
    else:
        # Sidebar settings
        st.sidebar.title("Settings")
        st.session_state['dark_mode'] = st.sidebar.checkbox("Dark Mode", value=st.session_state['dark_mode'])

        model_choice = st.sidebar.selectbox(
            "Choose Model:",
            ["Gemini 1.5 Flash", "Gemini 1.5 Pro", "Gemini 1.0 Pro"]
        )

        temperature = st.sidebar.slider("Temperature", 0.0, 1.0, 1.0)
        top_p = st.sidebar.slider("Top P", 0.0, 1.0, 0.95)
        top_k = st.sidebar.slider("Top K", 0, 100, 64)
        max_output_tokens = st.sidebar.slider("Max Output Tokens", 1, 8192, 8192)

        apply_css(st.session_state['dark_mode'])

        st.title("Chatbot with Gemini Models")

        # Retrieve API key from environment variable
        api_key = os.getenv("GEMINI_API_KEY")
        if api_key:
            model_name = get_model_name(model_choice)
            chat_session = create_chat_session(api_key, model_name, temperature, top_p, top_k, max_output_tokens)

            if 'chat_history' not in st.session_state:
                st.session_state['chat_history'] = []

            user_input = st.text_input("You: ", key="user_input")
            if user_input:
                response = chat_session.send_message(user_input)
                st.session_state.chat_history.append(("user", user_input))
                st.session_state.chat_history.append(("ai", response.text, model_name))

            chat_container = st.container()
            with chat_container:
                for entry in st.session_state.chat_history:
                    if entry[0] == "user":
                        st.markdown(f"""
                            <div class="chat-message user">
                                <div class="chat-icon user"></div>
                                <div class="chat-bubble user">{entry[1]}</div>
                            </div>
                        """, unsafe_allow_html=True)
                    else:
                        st.markdown(f"""
                            <div class="chat-message ai">
                                <div class="chat-icon ai"></div>
                                <div class="chat-bubble ai">{entry[1]} <br><small>{entry[2]}</small></div>
                            </div>
                        """, unsafe_allow_html=True)
        else:
            st.error("API key not found. Please set the 'GEMINI_API_KEY' environment variable.")

if __name__ == "__main__":
    main()
