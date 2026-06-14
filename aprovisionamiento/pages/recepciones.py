import streamlit as st
from components.layout import page_header, panel, section_rule
from components.tables import build_recepciones_grid
from data.mock import get_recepciones
from components.plotly_theme import categorias_donut
import plotly.graph_objects as go


def render():
    page_header(
        title="Recepciones",
        subtitle="Registro de recepciones de materiales y control de albaranes.",
    )

    df = get_recepciones()

    col_s, col_f, col_p = st.columns([2, 2, 3])
    with col_s:
        estado_opts = ["Todos los estados", "recibido", "en_transito", "incidencia"]
        estado_labels = {
            "Todos los estados": "Todos los estados",
            "recibido": "Recibido",
            "en_transito": "En tránsito",
            "incidencia": "Incidencia",
        }
        estado_sel = st.selectbox(
            "Estado",
            options=estado_opts,
            format_func=lambda x: estado_labels.get(x, x),
            label_visibility="collapsed",
            key="rec_estado",
        )
    with col_f:
        prov_names = ["Todos los proveedores"] + sorted(
            {r["prov"]["name"] for _, r in df.iterrows()}
        )
        prov_sel = st.selectbox(
            "Proveedor",
            options=prov_names,
            label_visibility="collapsed",
            key="rec_prov",
        )
    with col_p:
        buscar = st.text_input(
            "Buscar",
            placeholder="Código, artículo o albarán…",
            label_visibility="collapsed",
            key="rec_search",
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
            | vista["albarán"].str.lower().str.contains(q, na=False)
        )
        vista = vista[mask]

    section_rule()

    n_recibido  = int((df["status"] == "recibido").sum())
    n_transito  = int((df["status"] == "en_transito").sum())
    n_incidencia = int((df["status"] == "incidencia").sum())
    pct_ok = round(n_recibido / len(df) * 100) if len(df) else 0

    col_a, col_b, col_c, col_d = st.columns(4)
    col_a.metric("Total recepciones", len(df))
    col_b.metric("Recibidas", n_recibido, f"{pct_ok}%")
    col_c.metric("En tránsito", n_transito)
    col_d.metric("Incidencias", n_incidencia)

    section_rule()

    col_table, col_chart = st.columns([3, 1], gap="large")

    with col_table:
        with panel("Recepciones", f"{len(vista)} registros"):
            if vista.empty:
                st.info("No hay recepciones que coincidan con los filtros.")
            else:
                build_recepciones_grid(vista.reset_index(drop=True))

    with col_chart:
        with panel("Por estado"):
            labels = ["Recibido", "En tránsito", "Incidencia"]
            values = [n_recibido, n_transito, n_incidencia]
            st.plotly_chart(
                categorias_donut(labels, values),
                use_container_width=True,
                config={"displayModeBar": False},
            )

        with panel("Por proveedor"):
            prov_counts = df["prov"].apply(lambda p: p["name"]).value_counts().head(5)
            fig = go.Figure(go.Bar(
                x=prov_counts.values,
                y=prov_counts.index,
                orientation="h",
                marker_color="#C8102E",
                marker_line_width=0,
            ))
            fig.update_layout(
                height=200,
                margin=dict(l=10, r=10, t=10, b=10),
                paper_bgcolor="#FFFFFF",
                plot_bgcolor="#FFFFFF",
                xaxis=dict(showgrid=False, visible=False),
                yaxis=dict(
                    tickfont=dict(family="Oswald", size=10.5, color="#6B6B6B"),
                    autorange="reversed",
                ),
                showlegend=False,
            )
            st.plotly_chart(
                fig,
                use_container_width=True,
                config={"displayModeBar": False},
            )
