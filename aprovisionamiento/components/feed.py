from typing import Literal

KIND = Literal["recibido", "en_transito", "incidencia", "pendiente", "en_preparacion"]

_ICON = {
    "recibido":       ('<svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><polyline points="20 6 9 17 4 12"/></svg>', "ok"),
    "en_transito":    ('<svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M5 17H3a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h11a2 2 0 0 1 2 2v3"/><rect x="9" y="11" width="14" height="10" rx="2"/></svg>', "info"),
    "incidencia":     ('<svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><path d="m21.73 18-8-14a2 2 0 0 0-3.48 0l-8 14A2 2 0 0 0 4 21h16a2 2 0 0 0 1.73-3Z"/><line x1="12" y1="9" x2="12" y2="13"/><line x1="12" y1="17" x2="12.01" y2="17"/></svg>', "hot"),
    "pendiente":      ('<svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="10"/><polyline points="12 6 12 12 16 14"/></svg>', "wait"),
    "en_preparacion": ('<svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M21 8a2 2 0 0 0-1-1.73l-7-4a2 2 0 0 0-2 0l-7 4A2 2 0 0 0 3 8v8a2 2 0 0 0 1 1.73l7 4a2 2 0 0 0 2 0l7-4A2 2 0 0 0 21 16Z"/></svg>', "wait"),
}


def feed_item(code: str, text: str, time: str, kind: KIND = "en_transito") -> str:
    icon_svg, tone = _ICON.get(kind, (_ICON["en_transito"]))
    return f"""
    <div style="display:flex;align-items:flex-start;gap:10px;padding:10px 0;
                border-bottom:1px solid var(--rule-1);">
      <div class="al-kpi-icon {tone}" style="flex:0 0 26px;width:26px;height:26px;border-radius:6px;margin-top:1px;">
        {icon_svg}
      </div>
      <div style="flex:1;min-width:0;">
        <div style="font-family:var(--font-display);font-size:11.5px;font-weight:600;
                    letter-spacing:.04em;color:var(--ink);">{code}</div>
        <div style="font-size:12.5px;color:var(--fg-2);margin-top:2px;">{text}</div>
      </div>
      <div style="font-size:11px;color:var(--fg-3);white-space:nowrap;padding-top:2px;">{time}</div>
    </div>
    """


def delivery_item(code: str, supplier: str, item: str, eta: str,
                  qty: str, status: str) -> str:
    from components.badges import badge
    return f"""
    <div style="display:flex;align-items:center;gap:14px;padding:11px 0;
                border-bottom:1px solid var(--rule-1);">
      <div style="flex:0 0 80px;font-family:var(--font-display);font-weight:600;
                  font-size:12px;letter-spacing:.06em;color:var(--ink);">{code}</div>
      <div style="flex:1;min-width:0;">
        <div style="font-size:13px;font-weight:600;color:var(--ink);
                    white-space:nowrap;overflow:hidden;text-overflow:ellipsis;">{item}</div>
        <div style="font-size:11.5px;color:var(--fg-2);">{supplier}</div>
      </div>
      <div style="font-family:var(--font-display);font-size:12px;
                  font-weight:500;color:var(--fg-1);text-align:right;">{qty}</div>
      <div style="font-family:var(--font-display);font-size:12px;
                  font-weight:600;color:var(--ink);text-align:right;min-width:70px;">{eta}</div>
      <div>{badge(status)}</div>
    </div>
    """
