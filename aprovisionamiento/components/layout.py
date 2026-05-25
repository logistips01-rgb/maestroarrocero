import streamlit as st
from contextlib import contextmanager
from typing import Optional


def page_header(title: str, eyebrow: Optional[str] = None,
                subtitle: Optional[str] = None) -> None:
    eyebrow_html = (
        f'<div class="al-eyebrow"><span class="dot"></span>{eyebrow}</div>'
        if eyebrow else ""
    )
    sub_html = f'<p class="al-sub">{subtitle}</p>' if subtitle else ""
    st.html(f"""
        <div style="margin-bottom:22px;">
          {eyebrow_html}
          <h1 class="al-title">{title}</h1>
          {sub_html}
        </div>
    """)


def section_rule(label: str = "") -> None:
    label_html = (
        f'<span style="font-family:var(--font-display);font-size:10.5px;font-weight:600;'
        f'letter-spacing:.14em;text-transform:uppercase;color:var(--fg-2);'
        f'background:var(--canvas);padding:0 10px;position:relative;top:-1px;">{label}</span>'
        if label else ""
    )
    st.html(f'<div style="border-top:1px solid var(--rule-1);margin:20px 0 16px;'
            f'text-align:center;">{label_html}</div>')


@contextmanager
def panel(title: str, subtitle: Optional[str] = None):
    sub_html = f'<div class="al-panel-sub">{subtitle}</div>' if subtitle else ""
    st.html(f"""
        <div class="al-panel-head" style="border:1px solid var(--rule-1);
             border-bottom:0;border-radius:var(--radius-lg) var(--radius-lg) 0 0;
             background:var(--surface);">
          <div>
            <div class="al-panel-title">{title}</div>
            {sub_html}
          </div>
        </div>
    """)
    with st.container(border=True):
        yield
