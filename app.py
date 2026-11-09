
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

        st.error(
            result.get(
                "answer",
                "Something went wrong while processing your question."
            )
        )

    elif not result.get("sources"):

        st.info(
            "I don't have enough evidence in the available documents "
            "to answer this question. Try asking something related "
            "to Python documentation."
        )

        st.write(result.get("answer", ""))

    else:

        st.success("Answer generated using retrieved documentation.")

        st.write(result.get("answer", ""))

    # ---------------------------------------------
    # Expandable source passages
    # ---------------------------------------------

    sources = result.get("sources", [])

    if sources:

        st.divider()
        st.subheader("Retrieved Sources")

        for source in sources:

            label = source.get("source_label", "Source")
            document = source.get("document_name", "Unknown document")
            title = source.get("title", "Untitled")

            with st.expander(
                f"{label} — {title} ({document})"
            ):

                st.markdown("**Document:** " + document)

                st.markdown("**Title:** " + title)

                st.markdown("**Passage:**")

                st.write(source.get("text", "No passage available."))

                st.caption(
                    "Chunk ID: " + str(source.get("chunk_id", "Unknown"))
                )

                source_url = source.get("source_url")

                if source_url:
                    st.markdown(f"[Open original document]({source_url})")
