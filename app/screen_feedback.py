import streamlit as st

def render_feedback_ui(question: str = "", student_answer: str = "") -> None:
    """
    Renders the exam question, student answer input, and feedback display.
    """

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
                    feedback_text = f"""
**Strengths** ✅
- Clearly addressed the main topic.
- Good structure and logical flow.

**Weaknesses** ⚠️
- Missing examples for some points.
- Minor grammatical errors.

**Suggestions** 💡
- Include references or citations if applicable.
- Expand on key concepts for clarity.

**Score:** 7/10
"""
                # ---------- FEEDBACK DISPLAY ----------
                st.markdown("### 📋 Feedback")
                st.markdown(feedback_text, unsafe_allow_html=True)

                # Optional: Add colored alert boxes for categories
                st.success("Strengths highlighted above")
                st.warning("Weaknesses highlighted above")
                st.info("Suggestions highlighted above")
