import os
import streamlit as st
from dotenv import load_dotenv

from api_client import ask_question, check_health, API_BASE_URL

load_dotenv()

st.set_page_config(page_title="RAG Document Assistant - Data Structures & Algorithms", page_icon="📚", layout="wide")

# Sidebar Status & Information
with st.sidebar:
    st.title("⚙️ System Status")
    st.markdown(f"**Backend URL:** `{API_BASE_URL}`")
    
    is_online = check_health()
    if is_online:
        st.success("🟢 Backend Connected (/health OK)")
    else:
        st.error("🔴 Backend Unreachable")
        
    st.divider()
    st.markdown("### 📚 Document Domain")
    st.markdown("**Data Structures & Algorithms**")
    st.markdown("- Unit I: Stacks, Queues, Expressions")
    st.markdown("- Unit III: Trees, BSTs, Huffman Coding")
    st.markdown("- Unit IV: Sorting Algorithms")

st.title("📚 RAG-Powered Document Assistant")
st.caption("Ask questions about Data Structures & Algorithms and receive grounded, cited answers.")

if "messages" not in st.session_state:
    st.session_state.messages = []

if not is_online:
    st.warning("⚠️ Backend server is currently offline. Please start FastAPI on port 8000 (`uvicorn app.main:app --reload`).")

# Render message history
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# User Input
question = st.chat_input("Ask a question about Stacks, Queues, Trees, Huffman Coding, or Sorting...")

if question:
    st.session_state.messages.append({"role": "user", "content": question})
    with st.chat_message("user"):
        st.markdown(question)

    with st.chat_message("assistant"):
        with st.spinner("Searching vector store and generating grounded answer..."):
            try:
                result = ask_question(question)
                answer = result["answer"]
                sources = result.get("sources", [])

                st.markdown(answer)
                if sources:
                    st.caption("📑 **Cited Sources:** " + ", ".join(sources))

                content = answer + (
                    f"\n\n*Cited Sources: {', '.join(sources)}*" if sources else ""
                )
                st.session_state.messages.append({"role": "assistant", "content": content})

            except Exception as e:
                error_msg = f"❌ Error contacting backend API: {e}"
                st.error(error_msg)
                st.session_state.messages.append({"role": "assistant", "content": error_msg})
