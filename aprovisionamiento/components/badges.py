from typing import Literal

STATUS = Literal["pendiente", "en_preparacion", "en_transito", "recibido", "incidencia"]

_MAP = {
    "pendiente":      ("hot",  "Pendiente"),
    "en_preparacion": ("wait", "En preparación"),
    "en_transito":    ("info", "En tránsito"),
    "recibido":       ("ok",   "Recibido"),
    "incidencia":     ("hot",  "Incidencia"),
}


def badge(status: str) -> str:
    cls, label = _MAP.get(status, ("info", status))
    return f'<span class="al-badge {cls}"><span class="dot"></span>{label}</span>'
