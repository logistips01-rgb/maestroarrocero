import pandas as pd
from st_aggrid import AgGrid, GridOptionsBuilder, JsCode

PROV_RENDERER = JsCode("""
class ProvRenderer {
  init(p) {
    const v = p.value || {};
    const name = v.name || p.value || '';
    const id = v.id || '';
    const city = v.city || '';
    const color = v.color || '#C8102E';
    const initials = name.split(' ').slice(0,2).map(w=>w[0]||'').join('').toUpperCase();
    this.eGui = document.createElement('div');
    this.eGui.innerHTML = `
      <div class="al-prov" style="display:flex;align-items:center;gap:10px;padding:4px 0;">
        <div class="al-prov-avatar" style="width:26px;height:26px;border-radius:6px;
             display:grid;place-items:center;font-family:'Oswald',sans-serif;
             font-weight:600;font-size:11px;color:#fff;flex:0 0 26px;
             background:${color}">${initials}</div>
        <div style="display:flex;flex-direction:column;min-width:0;">
          <b style="font-size:13px;color:#2B2B2B;font-weight:600;line-height:1.2;">${name}</b>
          <span style="font-size:11px;color:#6B6B6B;">${id}${city ? ' · ' + city : ''}</span>
        </div>
      </div>`;
  }
  getGui(){ return this.eGui; }
}
""")

BADGE_RENDERER = JsCode("""
class BadgeRenderer {
  init(p) {
    const MAP = {
      pendiente:      ['hot',  'Pendiente'],
      en_preparacion: ['wait', 'En preparación'],
      en_transito:    ['info', 'En tránsito'],
      recibido:       ['ok',   'Recibido'],
      incidencia:     ['hot',  'Incidencia'],
    };
    const [cls, lbl] = MAP[p.value] || ['info', p.value || ''];
    const COLORS = {
      ok:   {bg:'#E9F3E4',fg:'#2F6B26',dot:'#4A8B3B'},
      wait: {bg:'#FBEFD3',fg:'#8A5A0A',dot:'#E08A1A'},
      hot:  {bg:'#FDECEE',fg:'#8E0A1F',dot:'#C8102E'},
      info: {bg:'#E2ECF8',fg:'#214E84',dot:'#2F6FB5'},
    };
    const c = COLORS[cls] || COLORS.info;
    this.eGui = document.createElement('span');
    this.eGui.style.cssText = `display:inline-flex;align-items:center;gap:6px;
      font-family:'Oswald',sans-serif;font-size:10.5px;font-weight:600;
      letter-spacing:.08em;text-transform:uppercase;padding:3px 9px 3px 7px;
      border-radius:999px;background:${c.bg};color:${c.fg};white-space:nowrap;`;
    this.eGui.innerHTML = `<span style="width:6px;height:6px;border-radius:50%;
      background:${c.dot};display:inline-block;flex-shrink:0;"></span>${lbl}`;
  }
  getGui(){ return this.eGui; }
}
""")

PROGRESS_RENDERER = JsCode("""
class ProgressRenderer {
  init(p) {
    const v = p.value || {};
    const pct = v.value ?? p.value ?? 0;
    const status = v.status || '';
    const barColor = status === 'incidencia' ? '#C8102E'
                   : (status === 'pendiente' || status === 'en_preparacion') ? '#E08A1A'
                   : '#4A8B3B';
    this.eGui = document.createElement('div');
    this.eGui.style.cssText = 'display:flex;align-items:center;gap:8px;min-width:110px;';
    this.eGui.innerHTML = `
      <div style="flex:1;height:5px;background:#ECE6D6;border-radius:999px;overflow:hidden;">
        <div style="width:${pct}%;height:100%;background:${barColor};border-radius:inherit;"></div>
      </div>
      <span style="font-family:'Oswald',sans-serif;font-weight:500;font-size:11px;
                   color:#6B6B6B;min-width:32px;text-align:right;">${pct}%</span>`;
  }
  getGui(){ return this.eGui; }
}
""")

ITEM_RENDERER = JsCode("""
function(p) {
  const item = p.data.item || '';
  const cat  = p.data.cat  || '';
  return `<div style="display:flex;flex-direction:column;padding:3px 0;">
    <span style="color:#2B2B2B;font-weight:500;font-size:13px;">${item}</span>
    <span style="font-size:11.5px;color:#6B6B6B;">${cat}</span>
  </div>`;
}
""")

AMOUNT_FMT = JsCode("""
function(p){
  if (p.value == null) return '';
  return p.value.toLocaleString('es-ES') + ' €';
}
""")


def build_pedidos_grid(df: pd.DataFrame):
    gb = GridOptionsBuilder.from_dataframe(df)
    gb.configure_default_column(
        resizable=True, sortable=True, filter=True,
        cellStyle={"display": "flex", "alignItems": "center"},
    )
    gb.configure_selection("multiple", use_checkbox=True, header_checkbox=True)

    gb.configure_column("code", header_name="Pedido",
                        cellStyle={"fontFamily": "Oswald", "fontWeight": "600",
                                   "color": "#2B2B2B", "letterSpacing": ".04em"},
                        width=120)
    gb.configure_column("prov", header_name="Proveedor",
                        cellRenderer=PROV_RENDERER, autoHeight=True, width=230)
    gb.configure_column("item", header_name="Materia prima",
                        cellRenderer=ITEM_RENDERER, autoHeight=True, flex=1)
    gb.configure_column("cat", hide=True)
    gb.configure_column("qty", header_name="Cantidad", type=["rightAligned"], width=100)
    gb.configure_column("status", header_name="Estado",
                        cellRenderer=BADGE_RENDERER, width=155)
    gb.configure_column("progress", header_name="Progreso",
                        cellRenderer=PROGRESS_RENDERER, width=165, autoHeight=True)
    gb.configure_column("emit", header_name="Emisión", width=95,
                        cellStyle={"color": "#6B6B6B"})
    gb.configure_column("eta", header_name="ETA", width=95,
                        cellStyle={"color": "#2B2B2B", "fontWeight": "500"})
    gb.configure_column("amount", header_name="Importe", type=["rightAligned"],
                        valueFormatter=AMOUNT_FMT, width=110,
                        cellStyle={"fontFamily": "Oswald", "fontWeight": "500",
                                   "color": "#2B2B2B"})

    gb.configure_grid_options(
        domLayout="normal", rowHeight=48, headerHeight=40,
        suppressRowClickSelection=False,
    )

    return AgGrid(
        df,
        gridOptions=gb.build(),
        theme="material",
        allow_unsafe_jscode=True,
        height=500,
        fit_columns_on_grid_load=False,
        update_mode="MODEL_CHANGED",
    )


def build_recepciones_grid(df: pd.DataFrame):
    gb = GridOptionsBuilder.from_dataframe(df)
    gb.configure_default_column(
        resizable=True, sortable=True, filter=True,
        cellStyle={"display": "flex", "alignItems": "center"},
    )
    gb.configure_column("code", header_name="Pedido",
                        cellStyle={"fontFamily": "Oswald", "fontWeight": "600",
                                   "color": "#2B2B2B"}, width=120)
    gb.configure_column("prov", header_name="Proveedor",
                        cellRenderer=PROV_RENDERER, autoHeight=True, width=220)
    gb.configure_column("item", header_name="Artículo", flex=1)
    gb.configure_column("qty_pedido", header_name="Pedido", type=["rightAligned"], width=95)
    gb.configure_column("qty_recibido", header_name="Recibido", type=["rightAligned"], width=95)
    gb.configure_column("status", header_name="Estado",
                        cellRenderer=BADGE_RENDERER, width=155)
    gb.configure_column("fecha", header_name="Fecha recep.", width=120,
                        cellStyle={"color": "#2B2B2B", "fontWeight": "500"})
    gb.configure_column("albarán", header_name="Albarán", width=110,
                        cellStyle={"color": "#6B6B6B"})

    gb.configure_grid_options(domLayout="normal", rowHeight=44, headerHeight=40)

    return AgGrid(
        df,
        gridOptions=gb.build(),
        theme="material",
        allow_unsafe_jscode=True,
        height=460,
        fit_columns_on_grid_load=False,
        update_mode="MODEL_CHANGED",
    )
