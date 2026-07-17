from __future__ import annotations

import json
from pathlib import Path

import streamlit as st
from dotenv import load_dotenv

from components.theme import apply_theme
from components.sidebar import render_sidebar
from services.workflow_service import WorkflowService
from utils.logging_config import get_logger
from workflows.fact_checker.real_adapter import FactCheckerRealAdapter

load_dotenv(dotenv_path=Path(__file__).resolve().parents[1] / ".env")
logger = get_logger("fact_checker")

apply_theme()
render_sidebar()

st.title("🔎 Research & Fact Checker")
st.write("Run research, summarization, and fact-checking workflows on a question, topic, or pasted text.")

with st.form("fact_checker_form"):
    question = st.text_input("Question", value="What are the latest AI agents trends?")
    topic = st.text_input("Topic", value="AI agents")
    text_input = st.text_area("Text to analyze", height=200, value="Paste any article or report here for research and verification.")
    submitted = st.form_submit_button("Run workflow")

if submitted:
    service = WorkflowService()
    try:
        adapter = FactCheckerRealAdapter()
        result = adapter.run(question, topic, text_input)
        payload = result
        path = service.save_json(payload, "fact_checker_payload.json")
        st.success(f"Research report generated and saved to {path.name}")
        st.subheader("Research report")
        st.markdown(payload.get("report", "No report generated."))

        with st.expander("Technical details"):
            st.caption(f"Topic: {payload.get('topic', 'unknown')}")
            st.caption(f"Question: {payload.get('question', 'unknown')}")
            st.caption(f"Model: {payload.get('llm', {}).get('model', 'unknown')}")
            st.caption(f"Agents config: {payload.get('source_config', {}).get('agents_path', 'unknown')}")
            st.caption(f"Tasks config: {payload.get('source_config', {}).get('tasks_path', 'unknown')}")

        st.download_button(
            "Download report payload",
            data=json.dumps(payload, indent=2),
            file_name="fact_checker_payload.json",
            mime="application/json",
        )
    except Exception as exc:  # pragma no cover - UI error path
        logger.exception("Fact checker workflow failed")
        st.error(f"Unexpected error: {exc}")
