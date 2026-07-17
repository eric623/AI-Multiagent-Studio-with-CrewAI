from __future__ import annotations

import json
from pathlib import Path

import streamlit as st
from dotenv import load_dotenv

from components.theme import apply_theme
from components.sidebar import render_sidebar
from services.workflow_service import WorkflowService
from utils.logging_config import get_logger
from workflows.social_content.real_adapter import SocialContentRealAdapter

load_dotenv(dotenv_path=Path(__file__).resolve().parents[1] / ".env")
logger = get_logger("social_content")

apply_theme()
render_sidebar()

st.title("📣 Social Content Planner")
st.write("Generate Twitter/X or LinkedIn content from a blog article using CrewAI flows and Firecrawl.")

with st.form("social_content_form"):
    blog_url = st.text_input("Blog URL", value="https://example.com/blog")
    post_type = st.selectbox("Target platform", ["twitter", "linkedin"])
    draft_path = st.text_input("Draft output path", value="assets/social_draft.md")
    example_threads = st.text_input("Example threads path", value="assets/example_threads.txt")
    example_linkedin = st.text_input("Example LinkedIn path", value="assets/example_linkedin.txt")
    submitted = st.form_submit_button("Run workflow")

if submitted:
    service = WorkflowService()
    try:
        st.info("Workflow execution uses Ollama locally via the configured model.")
        adapter = SocialContentRealAdapter()
        result = adapter.run(blog_url, post_type, draft_path, example_threads, example_linkedin)
        payload = result
        path = service.save_json(payload, "social_content_payload.json")
        st.success(f"Content generated and saved to {path.name}")
        st.subheader("Generated content")
        st.markdown(payload.get("generated_content", "No content generated."))

        with st.expander("Technical details"):
            st.caption(f"Source: {payload.get('source', 'unknown')}")
            st.caption(f"Model: {payload.get('llm', {}).get('model', 'unknown')}")
            st.caption(f"Fallback used: {payload.get('fallback_used', False)}")
            st.caption(f"Agents config: {payload.get('source_config', {}).get('agents_path', 'unknown')}")
            st.caption(f"Tasks config: {payload.get('source_config', {}).get('tasks_path', 'unknown')}")

        st.download_button(
            "Download JSON",
            data=json.dumps(payload, indent=2),
            file_name="social_content_payload.json",
            mime="application/json",
        )
    except Exception as exc:  # pragma: no cover - UI error path
        logger.exception("Social content workflow failed")
        st.error(f"Unexpected error: {exc}")
