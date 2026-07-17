from __future__ import annotations

import os
from pathlib import Path

import streamlit as st
from dotenv import load_dotenv

from components.theme import apply_theme
from components.sidebar import render_sidebar
from components.cards import render_feature_card
from services.workflow_service import WorkflowService
from utils.logging_config import get_logger

load_dotenv(dotenv_path=Path(__file__).resolve().parent / ".env")

logger = get_logger("app")
apply_theme()
render_sidebar()

st.title("AI Multi-Agent Studio")
st.subheader("Production-ready Multi-Agent Platform powered by CrewAI")

st.markdown("""
This studio brings together social content generation, book writing, and research workflows in a unified, professional web application.
""")

service = WorkflowService()

col1, col2, col3 = st.columns(3)
with col1:
    render_feature_card(
        "Social Content Planner",
        "Generate Twitter or LinkedIn content from a blog article using CrewAI flows and Firecrawl.",
        "📣",
        "pages/social_content.py",
    )
with col2:
    render_feature_card(
        "AI Book Writer",
        "Create a complete book outline and chapters with asynchronous multi-agent generation.",
        "📚",
        "pages/book_writer.py",
    )
with col3:
    render_feature_card(
        "Research & Fact Checker",
        "Run research, summarization, and fact verification workflows on a question or text.",
        "🔎",
        "pages/fact_checker.py",
    )

st.divider()

st.subheader("Platform Metrics")
metrics_col1, metrics_col2, metrics_col3, metrics_col4 = st.columns(4)
metrics_col1.metric("Workflows", 3)
metrics_col2.metric("Agents", 9)
metrics_col3.metric("Crews", 5)
metrics_col4.metric("Technologies", "CrewAI, Streamlit, Ollama")

st.divider()

st.subheader("About")
about_cols = st.columns(6)
for idx, tool in enumerate(["CrewAI", "Firecrawl", "Ollama", "SerperDev", "Streamlit", "Asyncio"]):
    with about_cols[idx]:
        st.markdown(f"- **{tool}**")

if __name__ == "__main__":
    logger.info("AI Multi-Agent Studio started")
