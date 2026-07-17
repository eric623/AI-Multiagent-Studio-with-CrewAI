import streamlit as st


def render_feature_card(title: str, description: str, icon: str, page_path: str) -> None:
    with st.container():
        st.markdown(f"### {icon} {title}")
        st.write(description)
        if st.button(f"Open {title}", key=f"btn_{title.lower().replace(' ', '_')}"):
            st.switch_page(page_path)
