import streamlit as st
from components.layout import page_header, panel, section_rule
from components.tables import build_pedidos_grid
from data.mock import get_pedidos
from lucide_svgs import ICONS


def render():
    page_header(
        title="Pedidos",
        subtitle="Listado completo de pedidos activos y su estado de avance.",
    )

    df = get_pedidos()

    col_stat, col_search, col_filt = st.columns([2, 3, 2])
    with col_stat:
        estado_opts = ["Todos los estados", "pendiente", "en_preparacion",
                       "en_transito", "recibido", "incidencia"]
        estado_labels = {
            "Todos los estados": "Todos los estados",
            "pendiente": "Pendiente",
            "en_preparacion": "En preparación",
            "en_transito": "En tránsito",
            "recibido": "Recibido",
            "incidencia": "Incidencia",
        }
        estado_sel = st.selectbox(
            "Estado",
            options=estado_opts,
            format_func=lambda x: estado_labels.get(x, x),
            label_visibility="collapsed",
            key="pedidos_estado",
        )
    with col_search:
        buscar = st.text_input(
            "Buscar",
            placeholder="Buscar por código, proveedor o artículo…",
            label_visibility="collapsed",
            key="pedidos_search",
        )
    with col_filt:
        prov_names = ["Todos los proveedores"] + sorted(
            {r["prov"]["name"] for _, r in df.iterrows()}
        )
        prov_sel = st.selectbox(
            "Proveedor",
            options=prov_names,
            label_visibility="collapsed",
            key="pedidos_prov",
        )

    vista = df.copy()
    if estado_sel != "Todos los estados":
        vista = vista[vista["status"] == estado_sel]
    if prov_sel != "Todos los proveedores":
        vista = vista[vista["prov"].apply(lambda p: p["name"] == prov_sel)]
    if buscar:
        q = buscar.lower()
        mask = (
            vista["code"].str.lower().str.contains(q, na=False)
            | vista["item"].str.lower().str.contains(q, na=False)
            | vista["prov"].apply(lambda p: q in p.get("name", "").lower())
        )
        vista = vista[mask]

    section_rule()

    col_a, col_b, col_c, col_d = st.columns(4)
    col_a.metric("Total pedidos", len(df))
    col_b.metric("Mostrados", len(vista))
    col_c.metric("En tránsito", int((df["status"] == "en_transito").sum()))
    col_d.metric("Incidencias", int((df["status"] == "incidencia").sum()))

    section_rule()

    with panel("Pedidos", f"{len(vista)} registros"):
        if vista.empty:
            st.info("No hay pedidos que coincidan con los filtros.")
        else:
            result = build_pedidos_grid(vista.reset_index(drop=True))
            selected = result.selected_rows
            if selected is not None and len(selected) > 0:
                n = len(selected)
                st.caption(f"{n} pedido{'s' if n > 1 else ''} seleccionado{'s' if n > 1 else ''}.")
                if st.button("🔍 Ver detalle del primero", key="btn_detalle_from_ped"):
                    code = selected[0]["code"] if isinstance(selected[0], dict) else selected[0]
                    st.session_state["detalle_code"] = code
                    st.session_state["nav_section"] = "🔍 Detalle"
                    st.rerun()
