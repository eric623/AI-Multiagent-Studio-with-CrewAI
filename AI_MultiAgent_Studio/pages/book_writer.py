from __future__ import annotations

import asyncio
import json
from pathlib import Path

import streamlit as st
from dotenv import load_dotenv

from components.theme import apply_theme
from components.sidebar import render_sidebar
from services.workflow_service import WorkflowService
from utils.logging_config import get_logger
from workflows.book_writer.real_adapter import BookWriterRealAdapter

load_dotenv(dotenv_path=Path(__file__).resolve().parents[1] / ".env")
logger = get_logger("book_writer")

apply_theme()
render_sidebar()

st.title("📚 AI Book Writer")
st.write("Generate an outline and chapters for a book using the existing CrewAI book-writing flow.")

with st.form("book_writer_form"):
    topic = st.text_input("Book topic", value="Artificial Intelligence in 2026")
    chapter_count = st.number_input("Number of chapters (optional)", min_value=1, max_value=20, value=5)
    llm_model = st.selectbox("LLM model", ["ollama/llama3.2:3b", "ollama/llama3.2:1b", "gpt-4o-mini"])
    submitted = st.form_submit_button("Run workflow")

if submitted:
    service = WorkflowService()
    try:
        st.info("Starting the book-writing workflow with Ollama")
        adapter = BookWriterRealAdapter()
        result = adapter.run(topic, int(chapter_count), llm_model)
        payload = result
        path = service.save_json(payload, "book_writer_payload.json")
        st.success(f"Book workflow completed and saved to {path.name}")
        st.subheader("Book outline")
        st.markdown(payload.get("generated_outline", "No outline generated."))

        with st.expander("Technical details"):
            st.caption(f"Topic: {payload.get('topic', 'unknown')}")
            st.caption(f"Chapters: {payload.get('total_chapters', 0)}")
            st.caption(f"Model: {payload.get('llm', {}).get('model', 'unknown')}")
            st.caption(f"Agents config: {payload.get('source_config', {}).get('agents_path', 'unknown')}")
            st.caption(f"Tasks config: {payload.get('source_config', {}).get('tasks_path', 'unknown')}")

        st.download_button(
            "Download payload",
            data=json.dumps(payload, indent=2),
            file_name="book_writer_payload.json",
            mime="application/json",
        )
    except Exception as exc:  # pragma: no cover - UI error path
        logger.exception("Book writer workflow failed")
        st.error(f"Unexpected error: {exc}")
