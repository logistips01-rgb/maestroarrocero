import streamlit as st
from components.layout import page_header, panel, section_rule
from components.badges import badge
from components.tracker import tracker
from data.mock import get_detalle, get_pedidos
from lucide_svgs import ICONS


_ESTADO_STEPS = ["pendiente", "en_preparacion", "en_transito", "recibido"]


def render():
    page_header(
        title="Detalle de pedido",
        subtitle="Información completa del pedido seleccionado.",
    )

    df = get_pedidos()
    codes = df["code"].tolist()

    col_sel, col_btn = st.columns([3, 1])
    with col_sel:
        default = st.session_state.get("detalle_code", codes[0] if codes else "")
        default_idx = codes.index(default) if default in codes else 0
        code = st.selectbox(
            "Pedido",
            options=codes,
            index=default_idx,
            label_visibility="collapsed",
            key="detalle_sel",
        )
    with col_btn:
        if st.button("← Volver a Pedidos", use_container_width=True):
            st.session_state["nav_section"] = "📋 Pedidos"
            st.rerun()

    row = get_detalle(code)
    if row is None:
        st.error("Pedido no encontrado.")
        return

    section_rule()

    prov      = row["prov"]
    status    = row["status"]
    progress  = row.get("progress", {})
    pct       = progress.get("value", 0) if isinstance(progress, dict) else 0
    initials  = "".join(w[0] for w in prov["name"].split()[:2]).upper()

    col_main, col_side = st.columns([2, 1], gap="large")

    with col_main:
        with panel("Resumen del pedido"):
            st.html(f"""
            <div style="display:flex;align-items:flex-start;gap:18px;padding:8px 0 14px;">
              <div style="width:48px;height:48px;border-radius:10px;background:{prov['color']};
                   display:grid;place-items:center;font-family:'Oswald',sans-serif;
                   font-weight:700;font-size:16px;color:#fff;flex:0 0 48px;">{initials}</div>
              <div style="flex:1;min-width:0;">
                <div style="font-family:'Oswald',sans-serif;font-size:18px;font-weight:700;
                            color:#2B2B2B;letter-spacing:.02em;">{code}</div>
                <div style="font-size:13px;color:#6B6B6B;margin-top:2px;">
                  {prov['name']} · {prov.get('city', '')}
                </div>
              </div>
              <div style="flex:0 0 auto;">{badge(status)}</div>
            </div>
            <hr style="border:none;border-top:1px solid #ECE6D6;margin:0 0 14px;">
            <div style="display:grid;grid-template-columns:repeat(3,1fr);gap:16px;">
              <div>
                <div style="font-size:11px;text-transform:uppercase;letter-spacing:.1em;
                            color:#9A9A9A;font-family:'Oswald',sans-serif;">Artículo</div>
                <div style="font-size:13px;color:#2B2B2B;font-weight:500;margin-top:3px;">
                  {row['item']}</div>
                <div style="font-size:11px;color:#6B6B6B;">{row.get('cat','')}</div>
              </div>
              <div>
                <div style="font-size:11px;text-transform:uppercase;letter-spacing:.1em;
                            color:#9A9A9A;font-family:'Oswald',sans-serif;">Cantidad</div>
                <div style="font-size:13px;color:#2B2B2B;font-weight:500;margin-top:3px;">
                  {row['qty']}</div>
              </div>
              <div>
                <div style="font-size:11px;text-transform:uppercase;letter-spacing:.1em;
                            color:#9A9A9A;font-family:'Oswald',sans-serif;">Importe</div>
                <div style="font-family:'Oswald',sans-serif;font-size:16px;font-weight:700;
                            color:#2B2B2B;margin-top:3px;">
                  {row['amount']:,} €</div>
              </div>
            </div>
            """)

        with panel("Progreso de entrega"):
            steps = [
                ("pendiente",       "Pedido emitido",        row.get("emit", "—")),
                ("en_preparacion",  "En preparación",        "—"),
                ("en_transito",     "En tránsito",           "—"),
                ("recibido",        "Entregado / Recibido",  row.get("eta", "—")),
            ]
            current_idx = _ESTADO_STEPS.index(status) if status in _ESTADO_STEPS else -1

            steps_html = ""
            for i, (key, label, date_str) in enumerate(steps):
                if i < current_idx:
                    dot_color, dot_inner, label_color = "#4A8B3B", "✓", "#4A8B3B"
                elif i == current_idx:
                    dot_color, dot_inner, label_color = "#C8102E", "●", "#C8102E"
                else:
                    dot_color, dot_inner, label_color = "#ECE6D6", "", "#9A9A9A"

                connector = ""
                if i < len(steps) - 1:
                    conn_color = "#4A8B3B" if i < current_idx else "#ECE6D6"
                    connector = (
                        f'<div style="flex:1;height:2px;background:{conn_color};'
                        f'margin:0 4px;align-self:center;margin-top:-18px;"></div>'
                    )

                steps_html += f"""
                <div style="display:flex;flex-direction:column;align-items:center;flex:1;min-width:0;">
                  <div style="width:28px;height:28px;border-radius:50%;
                       background:{dot_color};display:grid;place-items:center;
                       font-size:12px;color:#fff;font-weight:700;">{dot_inner}</div>
                  <div style="font-size:11px;font-weight:600;color:{label_color};
                       font-family:'Oswald',sans-serif;text-align:center;margin-top:5px;
                       letter-spacing:.04em;">{label}</div>
                  <div style="font-size:10px;color:#9A9A9A;margin-top:2px;">{date_str}</div>
                </div>
                """
                if i < len(steps) - 1:
                    conn_color = "#4A8B3B" if i < current_idx else "#ECE6D6"
                    steps_html += (
                        f'<div style="flex:0 0 40px;height:2px;background:{conn_color};'
                        f'align-self:flex-start;margin-top:14px;"></div>'
                    )

            bar_pct = pct
            bar_color = ("#C8102E" if status == "incidencia"
                         else "#E08A1A" if status in ("pendiente", "en_preparacion")
                         else "#4A8B3B")

            st.html(f"""
            <div style="padding:8px 0;">
              <div style="display:flex;align-items:flex-start;gap:0;">{steps_html}</div>
              <div style="margin-top:20px;">
                <div style="display:flex;justify-content:space-between;margin-bottom:5px;">
                  <span style="font-size:11px;color:#6B6B6B;font-family:'Oswald',sans-serif;
                               font-weight:600;text-transform:uppercase;letter-spacing:.08em;">
                    Progreso</span>
                  <span style="font-family:'Oswald',sans-serif;font-weight:600;
                               font-size:13px;color:{bar_color};">{bar_pct}%</span>
                </div>
                <div style="height:6px;background:#ECE6D6;border-radius:999px;overflow:hidden;">
                  <div style="width:{bar_pct}%;height:100%;background:{bar_color};
                       border-radius:inherit;"></div>
                </div>
              </div>
            </div>
            """)

    with col_side:
        with panel("Fechas clave"):
            st.html(f"""
            <div style="display:flex;flex-direction:column;gap:14px;padding:4px 0;">
              <div>
                <div style="font-size:10.5px;text-transform:uppercase;letter-spacing:.1em;
                            color:#9A9A9A;font-family:'Oswald',sans-serif;">Emisión</div>
                <div style="font-size:16px;font-family:'Oswald',sans-serif;font-weight:700;
                            color:#2B2B2B;margin-top:2px;">{row.get('emit','—')}</div>
              </div>
              <div style="border-top:1px solid #ECE6D6;padding-top:14px;">
                <div style="font-size:10.5px;text-transform:uppercase;letter-spacing:.1em;
                            color:#9A9A9A;font-family:'Oswald',sans-serif;">ETA prevista</div>
                <div style="font-size:16px;font-family:'Oswald',sans-serif;font-weight:700;
                            color:#C8102E;margin-top:2px;">{row.get('eta','—')}</div>
              </div>
            </div>
            """)

        with panel("Proveedor"):
            st.html(f"""
            <div style="padding:4px 0;">
              <div style="display:flex;align-items:center;gap:12px;margin-bottom:14px;">
                <div style="width:36px;height:36px;border-radius:8px;
                     background:{prov['color']};display:grid;place-items:center;
                     font-family:'Oswald',sans-serif;font-weight:700;font-size:13px;
                     color:#fff;flex:0 0 36px;">{initials}</div>
                <div>
                  <div style="font-size:13px;font-weight:600;color:#2B2B2B;line-height:1.2;">
                    {prov['name']}</div>
                  <div style="font-size:11px;color:#6B6B6B;">{prov.get('id','')}</div>
                </div>
              </div>
              <div style="font-size:12px;color:#6B6B6B;display:flex;align-items:center;gap:6px;">
                <span>📍</span> {prov.get('city','')}
              </div>
            </div>
            """)

        with panel("Acciones"):
            if st.button("📋 Copiar código", use_container_width=True):
                st.toast(f"Código {code} copiado.")
            if st.button("📥 Exportar PDF", use_container_width=True):
                st.toast("Generando PDF…")
            if st.button("🔔 Crear alerta", use_container_width=True):
                st.toast("Alerta creada para este pedido.")
