
import streamlit as st
import tempfile
import os

from dotenv import load_dotenv

from utils.audio_processor import process_input
from core.transcriber import transcribe_all
from core.summarize import summarize, generate_title
from core.extractor import (
    extract_action_items,
    extract_decisions_items,
    extract_questions
)
from core.rag_engine import build_rag_chain, ask_question

# ---------------- CONFIGURATION ----------------

load_dotenv()

st.set_page_config(
    page_title="AL Video Assistant",
    page_icon="🎧",
    layout="wide"
)

# ---------------- CUSTOM CSS ----------------

st.markdown("""
<style>
.stApp {
    background: #0E1117;
    color: white;
}

.block-container {
    padding-top: 2rem;
    max-width: 1200px;
}

[data-testid="stSidebar"] {
    background: #161B26;
}

.main-title {
    font-size: 38px;
    font-weight: 800;
    color: #FFFFFF;
}

.subtitle {
    color: #A0AEC0;
    font-size: 16px;
}

div[data-testid="stMetric"] {
    background: #1A2232;
    padding: 18px;
    border-radius: 12px;
    border: 1px solid #293548;
}

.stButton button {
    border-radius: 9px;
    font-weight: 600;
}

</style>
""", unsafe_allow_html=True)


# ---------------- SESSION STATE ----------------

if "result" not in st.session_state:
    st.session_state.result = None

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []


# ---------------- MAIN PROCESSING FUNCTION ----------------

def run_pipeline(source, language="english"):

    chunks = process_input(source)

    transcript = transcribe_all(chunks, language)

    title = generate_title(transcript)

    summary = summarize(transcript)

    action_items = extract_action_items(transcript)

    decisions = extract_decisions_items(transcript)

    questions = extract_questions(transcript)

    rag_chain = build_rag_chain(transcript)

    return {
        "title": title,
        "transcript": transcript,
        "summary": summary,
        "action_items": action_items,
        "key_decisions": decisions,
        "open_questions": questions,
        "rag_chain": rag_chain
    }


# ---------------- SIDEBAR ----------------

with st.sidebar:

    st.markdown("## 🎧 AL Video Assistant")

    st.caption("AI-powered video intelligence")

    st.divider()

    page = st.radio(
        "Navigation",
        [
            "Dashboard",
            "Summary",
            "Action Items",
            "Key Decisions",
            "Open Questions",
            "Transcript",
            "Chat with Video"
        ]
    )

    st.divider()

    st.markdown("### Features")

    st.markdown("""
    🎙️ Audio Transcription

    📝 Smart Summarization

    ✅ Action Extraction

    💡 Decision Detection

    ❓ Question Extraction

    💬 RAG-based Chat
    """)

    if st.session_state.result:

        if st.button("🗑️ Clear Session", use_container_width=True):
            st.session_state.result = None
            st.session_state.chat_history = []
            st.rerun()


# ---------------- HEADER ----------------

st.markdown(
    '<div class="main-title">Turn Videos Into Insights.</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">Upload your video or paste a YouTube URL. '
    'Let AI understand your content.</div>',
    unsafe_allow_html=True
)

st.write("")


# ---------------- DASHBOARD INPUT ----------------

if page == "Dashboard":

    st.markdown("## 📤 Upload Your Content")

    input_type = st.radio(
        "Select input type",
        ["YouTube URL", "Upload File"],
        horizontal=True
    )

    source = None
    uploaded_file = None

    if input_type == "YouTube URL":

        youtube_url = st.text_input(
            "YouTube Video URL",
            placeholder="https://www.youtube.com/watch?v=..."
        )

        source = youtube_url.strip()

    else:

        uploaded_file = st.file_uploader(
            "Upload Audio or Video",
            type=["mp3", "wav", "m4a", "mp4", "webm", "mpeg"]
        )

    language = st.selectbox(
        "Transcription Language",
        ["english", "hinglish"]
    )

    st.write("")

    if st.button(
        "🚀 Generate Insights",
        type="primary",
        use_container_width=True
    ):

        if input_type == "YouTube URL" and not source:
            st.warning("Please enter a YouTube URL.")

        elif input_type == "Upload File" and not uploaded_file:
            st.warning("Please upload a file.")

        else:

            temp_path = None

            try:

                if uploaded_file:

                    suffix = os.path.splitext(
                        uploaded_file.name
                    )[1]

                    with tempfile.NamedTemporaryFile(
                        delete=False,
                        suffix=suffix
                    ) as temp:

                        temp.write(uploaded_file.getbuffer())
                        temp_path = temp.name

                    source = temp_path

                with st.spinner(
                    "Processing your video... Please wait."
                ):

                    result = run_pipeline(source, language)

                    st.session_state.result = result
                    st.session_state.chat_history = []

                st.success("Video analyzed successfully!")

                st.rerun()

            except Exception as e:

                st.error(f"Something went wrong: {str(e)}")

            finally:

                if temp_path and os.path.exists(temp_path):
                    os.remove(temp_path)


# ---------------- DISPLAY RESULTS ----------------

result = st.session_state.result


if result:

    st.divider()

    st.markdown(f"## 🎬 {result['title']}")

    st.caption("Your video analysis is ready.")

    # ---------------- DASHBOARD ----------------

    if page == "Dashboard":

        c1, c2, c3, c4 = st.columns(4)

        with c1:
            st.metric("Transcript", "Ready")

        with c2:
            st.metric("Summary", "Ready")

        with c3:
            st.metric(
                "Action Items",
                len(result["action_items"])
                if isinstance(result["action_items"], (list, tuple))
                else "Ready"
            )

        with c4:
            st.metric(
                "Decisions",
                len(result["key_decisions"])
                if isinstance(result["key_decisions"], (list, tuple))
                else "Ready"
            )

        st.divider()

        st.markdown("### 📝 Executive Summary")

        st.info(result["summary"])

        c1, c2 = st.columns(2)

        with c1:

            with st.container(border=True):

                st.markdown("### ✅ Action Items")

                st.write(result["action_items"])

        with c2:

            with st.container(border=True):

                st.markdown("### 💡 Key Decisions")

                st.write(result["key_decisions"])

        st.markdown("### ❓ Open Questions")

        st.write(result["open_questions"])

    # ---------------- SUMMARY ----------------

    elif page == "Summary":

        st.markdown("## 📝 Video Summary")

        st.write(result["summary"])

        st.download_button(
            "⬇️ Download Summary",
            data=str(result["summary"]),
            file_name="video_summary.txt"
        )

    # ---------------- ACTION ITEMS ----------------

    elif page == "Action Items":

        st.markdown("## ✅ Action Items")

        st.write(result["action_items"])

    # ---------------- DECISIONS ----------------

    elif page == "Key Decisions":

        st.markdown("## 💡 Key Decisions")

        st.write(result["key_decisions"])

    # ---------------- QUESTIONS ----------------

    elif page == "Open Questions":

        st.markdown("## ❓ Open Questions")

        st.write(result["open_questions"])

    # ---------------- TRANSCRIPT ----------------

    elif page == "Transcript":

        st.markdown("## 📄 Full Transcript")

        transcript = result["transcript"]

        st.text_area(
            "Transcript",
            transcript,
            height=450
        )

        st.download_button(
            "⬇️ Download Transcript",
            data=transcript,
            file_name="transcript.txt"
        )

    # ---------------- RAG CHAT ----------------

    elif page == "Chat with Video":

        st.markdown("## 💬 Chat With Your Video")

        st.caption(
            "Ask questions and get answers based on your video."
        )

        # Display previous messages

        for message in st.session_state.chat_history:

            with st.chat_message(message["role"]):
                st.markdown(message["content"])

        question = st.chat_input(
            "Ask anything about your video..."
        )

        if question:

            st.session_state.chat_history.append({
                "role": "user",
                "content": question
            })

            with st.chat_message("user"):
                st.markdown(question)

            with st.chat_message("assistant"):

                with st.spinner("Thinking..."):

                    try:

                        answer = ask_question(
                            result["rag_chain"],
                            question
                        )

                        st.markdown(answer)

                        st.session_state.chat_history.append({
                            "role": "assistant",
                            "content": str(answer)
                        })

                    except Exception as e:

                        st.error(f"Chat error: {str(e)}")

else:

    if page != "Dashboard":

        st.info(
            "Please upload and analyze a video from Dashboard first."
        )

    st.divider()

    st.markdown("## ✨ What can this assistant do?")

    c1, c2, c3 = st.columns(3)

    with c1:
        st.markdown("### 🎙️ Transcription")
        st.caption("Convert audio and video into text.")

    with c2:
        st.markdown("### 🧠 AI Insights")
        st.caption("Generate summaries and extract decisions.")

    with c3:
        st.markdown("### 💬 Video Chat")
        st.caption("Ask questions using Retrieval Augmented Generation.")
