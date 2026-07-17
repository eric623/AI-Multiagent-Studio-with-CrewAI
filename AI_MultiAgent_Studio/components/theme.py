import streamlit as st


def apply_theme() -> None:
    st.set_page_config(
        page_title="AI Multi-Agent Studio",
        page_icon="🤖",
        layout="wide",
        initial_sidebar_state="expanded",
    )
    st.markdown(
        """
        <style>
        .stApp { background: linear-gradient(135deg, #0f172a 0%, #111827 100%); color: white; }
        .block-container { padding-top: 2rem; }
        div[data-testid="stSidebar"] { background: #020617; }
        </style>
        """,
        unsafe_allow_html=True,
    )
