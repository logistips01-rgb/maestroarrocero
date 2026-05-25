import streamlit as st
from pathlib import Path

_THEME_CSS = Path(__file__).parent.parent / "theme.css"

def inject_theme() -> None:
    st.markdown(f"<style>{_THEME_CSS.read_text(encoding='utf-8')}</style>",
                unsafe_allow_html=True)
