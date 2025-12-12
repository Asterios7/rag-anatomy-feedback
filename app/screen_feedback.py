import streamlit as st
import pandas as pd
from llm import async_embed_text, async_response_openai, GenText
from ranker import retrieve_top_k
from prompts import Prompts
import asyncio

RETRIEVAL_TOP_K = 1
OPENAI_MODEL = 'gpt-4o-mini'
df_rag = pd.read_parquet('./db/book_partition_full.parquet')

async def generate_feedback(question, student_answer):
    # Async calls
    question_text_embedding = await async_embed_text(text=question)
    df_rag_ranked = retrieve_top_k(
        df_rag=df_rag,
        query_embedding=question_text_embedding,
        top_k=RETRIEVAL_TOP_K
    )

    retrieved_text = " \n".join(df_rag_ranked['subchapter_text'].values)
    system_prompt, user_prompt = await Prompts.feedback(
        question=question,
        student_answer=student_answer,
        retrieved_text=retrieved_text
    )
    response = await async_response_openai(
        system_prompt=system_prompt,
        user_prompt=user_prompt,
        model=OPENAI_MODEL,
        response_model=GenText,
        temperature=0.0001
    )

    citations = []
    for i, row in df_rag_ranked.iterrows():
        citations.append(
            f"**{i+1}. Chapter {row.chapter_number}: {row.chapter_title}**  "
            f"• Subchapter {row.subchapter_number}: {row.subchapter_title}  "
            f"• Page: {row.subchapter_page}"
        )

    citations_text = "\n\n 📚 Citations\n\n" + "\n\n".join(citations)

    return response.text + citations_text


def render_feedback_ui(question: str = "", student_answer: str = "") -> None:
    """
    Renders the exam question, student answer input, and feedback display.
    """
    # ---------- HEADER ----------
    st.markdown("<h1 style='text-align: center; color: #4B8BBE;'>Exam Feedback AI</h1>", unsafe_allow_html=True)
    st.markdown("<h4 style='text-align: center; color: #555;'>Get instant feedback on student answers</h4>", unsafe_allow_html=True)
    st.write("---")

    # ---------- INPUT SECTION ----------
    with st.container():
        col1, col2 = st.columns(2)

        with col1:
            st.markdown("### 📝 Exam Question")
            question = st.text_area(
                "Enter the exam question here:",
                value=question,
                placeholder="Type or paste the exam question...",
                height=200
            )

        with col2:
            st.markdown("### ✍️ Student Answer")
            student_answer = st.text_area(
                "Enter the student answer here:",
                value=student_answer,
                placeholder="Type or paste the student's answer...",
                height=200
            )

    # ---------- SUBMIT BUTTON ----------
    with st.container():
        if st.button("Generate Feedback"):
            if not question.strip() or not student_answer.strip():
                st.warning("Please enter both a question and a student answer.")
            else:
                with st.spinner("Generating feedback..."):
                    # ---- MOCK FEEDBACK ----
                    # Replace this with your AI / model integration
                    feedback_text = asyncio.run(generate_feedback(question, student_answer))
                # ---------- FEEDBACK DISPLAY ----------
                st.markdown("### 📋 Feedback")
                st.markdown(feedback_text, unsafe_allow_html=True)

                # Optional: Add colored alert boxes for categories
                # st.success("Strengths highlighted above")
                # st.warning("Weaknesses highlighted above")
                # st.info("Suggestions highlighted above")
