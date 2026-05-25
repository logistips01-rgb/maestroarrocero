import plotly.graph_objects as go

BRAND = {
    "red":    "#C8102E",
    "sand":   "#C8B888",
    "ink":    "#2B2B2B",
    "fg2":    "#6B6B6B",
    "rule":   "#ECE6D6",
    "surface":"#FFFFFF",
    "green":  "#2F6B26",
    "blue":   "#214E84",
}


def aldelis_layout(**overrides) -> dict:
    base = dict(
        font=dict(family="Open Sans, sans-serif", size=12, color=BRAND["ink"]),
        paper_bgcolor=BRAND["surface"],
        plot_bgcolor=BRAND["surface"],
        margin=dict(l=40, r=20, t=20, b=40),
        xaxis=dict(
            showgrid=False,
            linecolor=BRAND["rule"],
            tickfont=dict(family="Oswald", size=10.5, color=BRAND["fg2"]),
        ),
        yaxis=dict(
            gridcolor=BRAND["rule"],
            griddash="dot",
            linecolor=BRAND["rule"],
            tickfont=dict(family="Oswald", size=10, color="#9A9A9A"),
        ),
        legend=dict(
            orientation="h", yanchor="bottom", y=1.02, x=0,
            font=dict(size=11, color=BRAND["fg2"]),
        ),
        hoverlabel=dict(
            bgcolor=BRAND["ink"],
            font=dict(color="#fff", family="Open Sans"),
        ),
    )
    base.update(overrides)
    return base


def volumen_chart(days, recibido, prevision):
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=days, y=recibido, name="Recibido",
        mode="lines+markers",
        line=dict(color=BRAND["red"], width=2),
        marker=dict(size=6, color=BRAND["surface"],
                    line=dict(color=BRAND["red"], width=1.6)),
        fill="tozeroy", fillcolor="rgba(200,16,46,.08)",
    ))
    fig.add_trace(go.Scatter(
        x=days, y=prevision, name="Previsión",
        mode="lines",
        line=dict(color=BRAND["sand"], width=2, dash="dash"),
    ))
    fig.update_layout(**aldelis_layout(height=240, showlegend=True))
    return fig


def estado_bar_chart(labels, values, colors=None):
    if colors is None:
        colors = [BRAND["red"], BRAND["sand"], BRAND["green"], BRAND["blue"]]
    fig = go.Figure(go.Bar(
        x=labels, y=values,
        marker_color=colors[:len(labels)],
        marker_line_width=0,
    ))
    fig.update_layout(**aldelis_layout(height=220, showlegend=False))
    fig.update_traces(width=0.5)
    return fig


def categorias_donut(labels, values):
    fig = go.Figure(go.Pie(
        labels=labels, values=values,
        hole=0.6,
        marker=dict(colors=[BRAND["red"], BRAND["sand"], BRAND["green"],
                             BRAND["blue"], "#9A9A9A"]),
        textinfo="label+percent",
        textfont=dict(family="Oswald", size=11),
    ))
    fig.update_layout(
        **aldelis_layout(height=240, showlegend=False,
                         margin=dict(l=10, r=10, t=10, b=10))
    )
    return fig
