import re
import streamlit as st
from pathlib import Path

_THEME_CSS = Path(__file__).parent.parent / "theme.css"


def _strip_css_comments(css: str) -> str:
    return re.sub(r"/\*.*?\*/", "", css, flags=re.DOTALL)


def inject_theme() -> None:
    css = _strip_css_comments(_THEME_CSS.read_text(encoding="utf-8"))
    st.markdown(f"<style>{css}</style>", unsafe_allow_html=True)
