import streamlit as st
from typing import Optional, Literal, List

TONE = Literal["red", "sand", "green", "blue"]
TREND = Literal["up", "down", "flat"]


def _sparkline_svg(data: List[float], color: str = "#C8102E",
                   width: int = 80, height: int = 22) -> str:
    if not data or len(data) < 2:
        return ""
    mx, mn = max(data), min(data)
    span = (mx - mn) or 1
    step = width / (len(data) - 1)
    pts = [(i * step, height - ((v - mn) / span) * (height - 4) - 2)
           for i, v in enumerate(data)]
    d = "M" + " L".join(f"{x:.1f} {y:.1f}" for x, y in pts)
    d_area = f"{d} L{pts[-1][0]:.1f} {height} L0 {height} Z"
    return f"""
      <svg class="al-kpi-spark" viewBox="0 0 {width} {height}" preserveAspectRatio="none">
        <path d="{d_area}" fill="{color}" opacity=".12"/>
        <path d="{d}" fill="none" stroke="{color}" stroke-width="1.6"
              stroke-linecap="round" stroke-linejoin="round"/>
      </svg>
    """


def kpi(label: str, value: str, unit: Optional[str] = None,
        icon_svg: str = "", tone: TONE = "red",
        trend: Optional[str] = None, trend_dir: TREND = "up",
        spark: Optional[List[float]] = None,
        spark_color: str = "#C8102E") -> str:
    unit_html = f'<span class="unit">{unit}</span>' if unit else ""
    trend_arrow = {"up": "↗", "down": "↘", "flat": "—"}[trend_dir]
    trend_html = (
        f'<span class="al-kpi-trend {trend_dir}">{trend_arrow} {trend}</span>'
        if trend else "<span></span>"
    )
    spark_html = _sparkline_svg(spark, spark_color) if spark else ""
    return f"""
    <div class="al-kpi">
      <div class="al-kpi-head">
        <div class="al-kpi-label">{label}</div>
        <div class="al-kpi-icon {tone}">{icon_svg}</div>
      </div>
      <div class="al-kpi-value">{value}{unit_html}</div>
      <div class="al-kpi-foot">{trend_html}{spark_html}</div>
    </div>
    """


def kpi_grid(items: List[dict]) -> None:
    cols = st.columns(len(items), gap="small")
    for col, it in zip(cols, items):
        with col:
            st.html(kpi(**it))
