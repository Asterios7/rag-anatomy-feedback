import streamlit as st
from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()
client = OpenAI(api_key=os.environ['OPENAI_API_KEY'])

def render_chat_ui():
    st.markdown(
        "<h1 style='text-align: center; color: #4B8BBE;'>Chat with McKinley Human Anatomy</h1>", 
        unsafe_allow_html=True
        )
    st.write("---")

    if "openai_model" not in st.session_state:
        st.session_state["openai_model"] = "gpt-4o-mini"

    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Display chat history (oldest first)
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # --- Chat input box always at the bottom ---
    prompt = st.chat_input("Type your message...")
    if prompt:
        # Append user message
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        # Generate assistant reply
        with st.chat_message("assistant"):
            stream = client.chat.completions.create(
                model=st.session_state["openai_model"],
                messages=st.session_state.messages,
                stream=True,
            )
            response = st.write_stream(stream)

        # Save assistant reply
        st.session_state.messages.append({"role": "assistant", "content": response})
