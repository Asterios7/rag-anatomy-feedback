import streamlit as st
from openai import OpenAI
import os
from dotenv import load_dotenv
load_dotenv()

st.title("ChatGPT-like clone")

client = OpenAI(api_key=os.environ['OPENAI_API_KEY'])

# Default model
if "openai_model" not in st.session_state:
    st.session_state["openai_model"] = "gpt-4o-mini"  # modern replacement

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Accept user input
if prompt := st.chat_input("What is up?"):
    # Add user message to history
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Generate assistant reply **ONLY after user input**
    # with st.chat_message("assistant"):
    #     stream = client.chat.completions.create(
    #         model=st.session_state["openai_model"],
    #         messages=st.session_state.messages,
    #         stream=True,
    #     )
    #     response = st.write_stream(stream)

    with st.chat_message("assistant"):
        stream = client.responses.create(
            model=st.session_state["openai_model"],
            input=st.session_state.messages,  # Use 'input' instead of 'messages'
            stream=True,
        )
        response = st.write_stream(stream)

    # Save assistant reply to session
    st.session_state.messages.append(
        {"role": "assistant", "content": response}
    )
