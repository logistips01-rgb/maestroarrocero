"""Mock data — replace with real DB/API queries."""
import pandas as pd
from datetime import date, timedelta
import random

random.seed(42)

PROVEEDORES = [
    {"id": "PROV-001", "name": "Bandejas Hispania S.L.",  "city": "Zaragoza", "color": "#C8102E"},
    {"id": "PROV-002", "name": "Etiquetas Padesa",         "city": "Madrid",   "color": "#214E84"},
    {"id": "PROV-003", "name": "Film Pack Ibérica",        "city": "Barcelona","color": "#2F6B26"},
    {"id": "PROV-004", "name": "Cajas Norte S.A.",         "city": "Bilbao",   "color": "#8A5A0A"},
    {"id": "PROV-005", "name": "Plásticos del Ebro",       "city": "Zaragoza", "color": "#6B3FA0"},
]

ARTICULOS = [
    ("Bandeja IFCO 400×300 mm",       "Envases"),
    ("Etiqueta adhesiva ALDI 80×90",  "Etiquetas"),
    ("Film extensible 500m 90cm",     "Films"),
    ("Caja cartón blanca 374×260",    "Cajas"),
    ("Bandeja bipack EVOH negra",     "Envases"),
    ("Etiqueta Lidl hamburguesa",     "Etiquetas"),
    ("Film barrera 300mm",            "Films"),
    ("Palet plástico gris H1",        "Palets"),
    ("Bandeja alveolar PET 250×180",  "Envases"),
    ("Etiqueta Eroski pollo",         "Etiquetas"),
]

ESTADOS = ["pendiente","en_preparacion","en_transito","recibido","incidencia"]
PESOS   = [0.25, 0.20, 0.30, 0.18, 0.07]


def _make_pedidos(n=28):
    rows = []
    today = date.today()
    for i in range(n):
        prov   = random.choice(PROVEEDORES)
        art, cat = random.choice(ARTICULOS)
        status = random.choices(ESTADOS, weights=PESOS)[0]
        pct    = {"pendiente": 0, "en_preparacion": random.randint(10,40),
                  "en_transito": random.randint(55,80),
                  "recibido": 100, "incidencia": random.randint(30,70)}[status]
        emit_d = today - timedelta(days=random.randint(1, 14))
        eta_d  = today + timedelta(days=random.randint(0, 10))
        rows.append({
            "code":     f"PC26-{1000+i:05d}",
            "prov":     prov,
            "item":     art,
            "cat":      cat,
            "qty":      f"{random.randint(1,50)*1000:,} ud",
            "status":   status,
            "progress": {"value": pct, "status": status},
            "emit":     emit_d.strftime("%d/%m/%y"),
            "eta":      eta_d.strftime("%d/%m/%y"),
            "amount":   random.randint(800, 18000),
        })
    return pd.DataFrame(rows)


def _make_recepciones(n=18):
    rows = []
    today = date.today()
    for i in range(n):
        prov = random.choice(PROVEEDORES)
        art, _  = random.choice(ARTICULOS)
        pedido  = random.randint(5000, 50000)
        recibido = pedido if random.random() > 0.3 else random.randint(int(pedido*0.5), pedido)
        status  = "recibido" if recibido == pedido else ("incidencia" if recibido < pedido*0.9 else "en_transito")
        fecha   = today - timedelta(days=random.randint(0, 7))
        rows.append({
            "code":         f"PC26-{2000+i:05d}",
            "prov":         prov,
            "item":         art,
            "qty_pedido":   f"{pedido:,} ud",
            "qty_recibido": f"{recibido:,} ud",
            "status":       status,
            "fecha":        fecha.strftime("%d/%m/%Y"),
            "albarán":      f"ALB-{random.randint(10000,99999)}",
        })
    return pd.DataFrame(rows)


def get_pedidos() -> pd.DataFrame:
    return _make_pedidos(28)


def get_recepciones() -> pd.DataFrame:
    return _make_recepciones(18)


def get_kpi_sparks():
    return {
        "pedidos":   [14,16,15,19,18,22,20,24,26,28],
        "pendientes":[18,17,17,16,15,15,14,13,12,12],
        "recepciones":[2,2,3,3,4,5,5,6,6,7],
        "valor":     [180,170,178,182,188,196,202,210,214,218],
    }


def get_volumen_semana():
    today = date.today()
    days  = [(today - timedelta(days=6-i)).strftime("%a %d") for i in range(7)]
    recibido  = [12,18,9,22,15,21,7]
    prevision = [15,15,15,18,18,20,20]
    return days, recibido, prevision


def get_estados_counts(df: pd.DataFrame):
    return df["status"].value_counts().reset_index()


def get_detalle(code: str):
    df = get_pedidos()
    row = df[df["code"] == code]
    if row.empty:
        return None
    return row.iloc[0].to_dict()
