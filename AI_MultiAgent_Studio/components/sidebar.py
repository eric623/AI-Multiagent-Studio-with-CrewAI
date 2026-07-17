import streamlit as st


def render_sidebar() -> None:
    with st.sidebar:
        st.title("🤖 AI Multi-Agent Studio")
        st.caption("Production-ready multi-agent platform")

        st.page_link("app.py", label="🏠 Home")
        st.page_link("pages/social_content.py", label="📣 Social Content Planner")
        st.page_link("pages/book_writer.py", label="📚 AI Book Writer")
        st.page_link("pages/fact_checker.py", label="🔎 Research & Fact Checker")

        st.divider()
        st.subheader("Environment")
        st.text_input("OpenAI API", value="Configured if available", label_visibility="collapsed")
        st.text_input("Firecrawl", value="Configured if available", label_visibility="collapsed")
