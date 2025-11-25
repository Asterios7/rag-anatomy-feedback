import streamlit as st
import pandas as pd
from typing import Tuple
from dotenv import load_dotenv
from openai import OpenAI
import os
import asyncio
from prompts import Prompts
from ranker import retrieve_top_k
from llm import async_embed_text


load_dotenv()
client = OpenAI(api_key=os.environ['OPENAI_API_KEY'])

RETRIEVAL_TOP_K = 4
OPENAI_MODEL = 'gpt-5.1'
df_rag = pd.read_parquet('./book/book_partition_full.parquet')


async def augment_prompt(prompt: str) -> Tuple[str, str]:
    # Async calls
    text_embedding = await async_embed_text(text=prompt)
    df_rag_ranked = retrieve_top_k(
        df_rag=df_rag,
        query_embedding=text_embedding,
        top_k=RETRIEVAL_TOP_K
    )

    retrieved_text = " \n".join(df_rag_ranked['subchapter_text'].values)

    citations = []
    for i, row in df_rag_ranked.iterrows():
        citations.append(
            f"**{i+1}. Chapter {row.chapter_number}: {row.chapter_title}**  "
            f"• Subchapter {row.subchapter_number}: {row.subchapter_title}  "
            f"• Page: {row.subchapter_page}"
        )

    system_prompt, user_prompt = await Prompts.converse_with_book(
        prompt=prompt,
        retrieved_text=retrieved_text,
        citations=citations
    )

    return system_prompt, user_prompt


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

    if "augmented_messages" not in st.session_state:
        st.session_state.augmented_messages = []

    # Display chat history (oldest first)
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # --- Chat input box always at the bottom ---
    prompt = st.chat_input("Type your message...")
    if prompt:
        with st.chat_message("user"):
            st.markdown(prompt)

        system_prompt_augm, user_prompt_augm = asyncio.run(augment_prompt(prompt))
        # Append user message
        st.session_state.messages.append({"role": "user", "content": prompt})
        st.session_state.augmented_messages.append(
            {"role": "system", "content": system_prompt_augm}
            )
        st.session_state.augmented_messages.append(
            {"role": "system", "content": user_prompt_augm}
            )
        


        # Generate assistant reply
        with st.chat_message("assistant"):
            print(st.session_state.augmented_messages)
            stream = client.chat.completions.create(
                model=st.session_state["openai_model"],
                messages=st.session_state.augmented_messages,
                stream=True,
            )
            response = st.write_stream(stream)

        # Save assistant reply
        st.session_state.messages.append({"role": "assistant", "content": response})
