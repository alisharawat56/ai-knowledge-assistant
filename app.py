
import streamlit as st

from src.qa import answer_question


# -------------------------------------------------
# Page configuration
# -------------------------------------------------

st.set_page_config(
    page_title="AI Knowledge Assistant",
    page_icon="📚",
    layout="wide"
)


# -------------------------------------------------
# Application header
# -------------------------------------------------

st.title("📚 AI Knowledge Assistant")

st.write(
    "Ask questions about Python programming. "
    "Answers are generated using your local knowledge base."
)

st.caption("Powered by RAG, Ollama, and SQLite")


# -------------------------------------------------
# Question input
# -------------------------------------------------

with st.form("question_form"):
    question = st.text_area(
        "Enter your question",
        placeholder="Example: What is a Python module?",
        height=100
    )

    ask_button = st.form_submit_button(
        "Ask",
        type="primary",
        use_container_width=True
    )


# -------------------------------------------------
# Process question
# -------------------------------------------------

if ask_button:

    if not question.strip():
        st.warning("Please enter a question.")

    else:
        with st.spinner(
            "Searching your knowledge base and generating an answer..."
        ):
            result = answer_question(question.strip())

        st.session_state["qa_result"] = result
        st.session_state["last_question"] = question.strip()


# -------------------------------------------------
# Display answer and sources
# -------------------------------------------------

if "qa_result" in st.session_state:
    result = st.session_state["qa_result"]

    st.divider()

    st.subheader("Your Question")
    st.write(st.session_state["last_question"])

    st.subheader("Answer")

    if result.get("error"):
        st.error(result.get("answer", "Something went wrong."))

    elif result.get("insufficient_evidence", False):
        st.warning(result.get("answer", "Not enough evidence to answer."))

    else:
        st.success("Response validated.")
        st.write(result["answer"])

    limitations = result.get("limitations", [])

    if limitations:
        with st.expander("Response limitations"):
            for limitation in limitations:
                st.write(f"- {limitation}")

    sources = result.get("sources", [])

    if sources:
        st.divider()
        st.subheader("Verified Retrieved Sources")

        for source in sources:
            label = source["source_label"]
            document = source["document_name"]
            title = source["title"]

            with st.expander(f"{label} — {title} ({document})"):
                st.markdown(f"**Document:** {document}")
                st.markdown(f"**Title:** {title}")
                st.markdown("**Retrieved passage:**")
                st.write(source["text"])

                st.caption(f"Chunk ID: {source['chunk_id']}")

                if source.get("source_url"):
                    st.markdown(
                        f"[Open original document]({source['source_url']})"
                    )
