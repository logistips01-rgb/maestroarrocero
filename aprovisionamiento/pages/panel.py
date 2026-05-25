import streamlit as st
from datetime import date
from components.layout import page_header, panel, section_rule
from components.kpi import kpi_grid
from components.feed import feed_item, delivery_item
from components.plotly_theme import volumen_chart, estado_bar_chart
from data.mock import get_pedidos, get_recepciones, get_kpi_sparks, get_volumen_semana
from lucide_svgs import ICONS


def render():
    today = date.today()
    week  = today.isocalendar()[1]
    day_es = ["Lunes","Martes","Miércoles","Jueves","Viernes","Sábado","Domingo"][today.weekday()]
    month_es = ["enero","febrero","marzo","abril","mayo","junio",
                "julio","agosto","septiembre","octubre","noviembre","diciembre"][today.month-1]

    page_header(
        title="Panel general",
        eyebrow=f"{day_es} · {today.day} de {month_es} de {today.year} · Semana {week}",
        subtitle="Visión global del aprovisionamiento de hoy y la próxima semana.",
    )

    df_ped = get_pedidos()
    df_rec = get_recepciones()
    sparks  = get_kpi_sparks()

    n_activos   = len(df_ped)
    n_pendiente = (df_ped["status"] == "pendiente").sum()
    n_rec_hoy   = (df_rec["status"] == "recibido").sum()
    val_transito = df_ped[df_ped["status"] == "en_transito"]["amount"].sum()

    kpi_grid([
        dict(label="Pedidos activos",      value=str(n_activos),
             icon_svg=ICONS["package"], tone="red",
             trend="+12% vs semana ant.", trend_dir="up",
             spark=sparks["pedidos"]),
        dict(label="Pendientes recepción", value=str(n_pendiente),
             icon_svg=ICONS["hourglass"], tone="sand",
             trend="−3 vs ayer", trend_dir="down",
             spark=sparks["pendientes"], spark_color="#C8B888"),
        dict(label="Recepciones hoy",      value=str(n_rec_hoy),
             unit=f"/ {len(df_rec)}",
             icon_svg=ICONS["truck"], tone="blue",
             trend=f"{int(n_rec_hoy/len(df_rec)*100)}% del día", trend_dir="flat",
             spark=sparks["recepciones"], spark_color="#214E84"),
        dict(label="Valor en tránsito",    value=f"{val_transito//1000}",
             unit="K €",
             icon_svg=ICONS["euro"], tone="green",
             trend="+8,4% vs mes ant.", trend_dir="up",
             spark=sparks["valor"], spark_color="#2F6B26"),
    ])

    section_rule()

    col_chart, col_feed = st.columns([3, 2], gap="large")

    with col_chart:
        with panel("Volumen semanal", "Unidades recibidas vs previsión"):
            days, recibido, prevision = get_volumen_semana()
            st.plotly_chart(volumen_chart(days, recibido, prevision),
                            use_container_width=True, config={"displayModeBar": False})

        with panel("Distribución por estado"):
            counts = df_ped["status"].value_counts()
            labels_map = {"pendiente": "Pendiente", "en_preparacion": "En prep.",
                          "en_transito": "En tránsito", "recibido": "Recibido",
                          "incidencia": "Incidencia"}
            labels = [labels_map.get(k, k) for k in counts.index]
            colors = ["#C8102E","#E08A1A","#2F6FB5","#4A8B3B","#C8B888"]
            st.plotly_chart(estado_bar_chart(labels, counts.values, colors),
                            use_container_width=True, config={"displayModeBar": False})

    with col_feed:
        with panel("Próximas recepciones", "Pedidos con ETA ≤ 3 días"):
            proximos = df_ped[df_ped["status"].isin(["en_transito","en_preparacion"])].head(6)
            if proximos.empty:
                st.info("Sin recepciones próximas.")
            else:
                items_html = ""
                for _, r in proximos.iterrows():
                    items_html += delivery_item(
                        code=r["code"],
                        supplier=r["prov"]["name"],
                        item=r["item"],
                        eta=r["eta"],
                        qty=r["qty"],
                        status=r["status"],
                    )
                st.html(f'<div style="padding:0 2px;">{items_html}</div>')

        with panel("Actividad reciente"):
            eventos = [
                ("PC26-01012", "Recibido · 24 000 ud bandejas", "hace 12 min", "recibido"),
                ("PC26-01007", "Incidencia en recepción — faltan 1 200 ud", "hace 35 min", "incidencia"),
                ("PC26-01019", "En tránsito desde Zaragoza", "hace 1 h", "en_transito"),
                ("PC26-01003", "Preparación completada por proveedor", "hace 2 h", "en_preparacion"),
                ("PC26-00998", "Recibido · 18 500 ud film", "ayer 16:42", "recibido"),
            ]
            ev_html = "".join(feed_item(code, text, t, kind)
                              for code, text, t, kind in eventos)
            st.html(f'<div style="padding:0 2px;">{ev_html}</div>')
