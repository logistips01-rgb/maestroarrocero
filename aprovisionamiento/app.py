import streamlit as st
from components.theme import inject_theme

st.set_page_config(
    page_title="Aprovisionamiento · Aldelis",
    page_icon="🍗",
    layout="wide",
    initial_sidebar_state="expanded",
)
inject_theme()

with st.sidebar:
    st.html("""
      <div style="display:flex;align-items:center;gap:12px;padding:4px 4px 14px;">
        <span style="font-family:'Pacifico',cursive;color:#C8102E;font-size:34px;line-height:1;">
          Aldelis
        </span>
        <div>
          <div style="font-family:'Oswald',sans-serif;font-size:11px;font-weight:600;
                      text-transform:uppercase;letter-spacing:.14em;color:#fff;">
            Aprovisionamiento
          </div>
          <div style="font-size:10px;color:rgba(255,255,255,.45);">Grupo Padesa</div>
        </div>
      </div>
    """)

    st.text_input(" ", placeholder="Buscar pedido o proveedor…",
                  label_visibility="collapsed", key="global_search")

    st.markdown("###### Principal")
    section = st.radio(
        "Sección",
        ["📊 Panel", "📋 Pedidos", "📦 Recepciones", "🔍 Detalle"],
        label_visibility="collapsed",
        key="nav_section",
    )

    st.markdown("###### Periodo")
    periodo = st.selectbox(
        "Periodo",
        ["Esta semana", "Últimos 7 días", "Este mes", "Últimos 30 días"],
        label_visibility="collapsed",
        key="periodo_sel",
    )

    st.markdown("###### Acciones")
    if st.button("➕ Nuevo pedido", use_container_width=True, type="primary"):
        st.session_state["nav_section"] = "📋 Pedidos"
        st.rerun()
    if st.button("⬇ Exportar", use_container_width=True):
        st.toast("Exportando…")

# ── Routing ───────────────────────────────────────────────────────
page = st.session_state.get("nav_section", "📊 Panel")

if page == "📊 Panel":
    from pages import panel as pg; pg.render()
elif page == "📋 Pedidos":
    from pages import pedidos as pg; pg.render()
elif page == "📦 Recepciones":
    from pages import recepciones as pg; pg.render()
elif page == "🔍 Detalle":
    from pages import detalle as pg; pg.render()
