# tools/herramientas_ecomarket.py
import uuid
from typing import Dict, Any

def verificar_elegibilidad_devolucion(payload: Dict[str, Any]) -> Dict[str, Any]:
    """
    Verifica si un producto es elegible para devolución (simulación).
    payload expected keys: id_pedido, sku_producto, motivo, fecha_compra (opcional), condicion (opcional)
    Returns: dict with keys: success(bool), elegible(bool), razon(str), id_devolucion(str|None)
    """
    if not payload or not payload.get("id_pedido") or not payload.get("sku_producto"):
        return {"success": False, "elegible": False, "razon": "Faltan id_pedido o sku_producto", "id_devolucion": None}

    motivo = (payload.get("motivo") or "").lower()
    # Reglas ficticias:
    if "dañado" in motivo or "defecto" in motivo or "incorrecto" in motivo:
        id_devolucion = str(uuid.uuid4())
        return {"success": True, "elegible": True, "razon": "Producto aceptado para devolución", "id_devolucion": id_devolucion}
    if "fuera de plazo" in motivo or "expiro" in motivo:
        return {"success": True, "elegible": False, "razon": "Plazo de devolución expirado", "id_devolucion": None}

    # Caso por defecto: requiere revisión manual
    return {"success": True, "elegible": False, "razon": "Requiere revisión manual", "id_devolucion": None}


def generar_etiqueta_devolucion(payload: Dict[str, Any]) -> Dict[str, Any]:
    """
    Genera una etiqueta de devolución (simulación).
    payload expected keys: id_devolucion, direccion_origen (dict con direccion), peso_estimado_kg (float)
    Returns: dict with success(bool), url_etiqueta(str|None), tracking_id(str|None), mensaje(str)
    """
    id_dev = payload.get("id_devolucion")
    direccion = payload.get("direccion_origen")
    peso = payload.get("peso_estimado_kg", 1.0)

    if not id_dev:
        return {"success": False, "url_etiqueta": None, "tracking_id": None, "mensaje": "Falta id_devolucion"}

    if not direccion:
        return {"success": False, "url_etiqueta": None, "tracking_id": None, "mensaje": "Falta direccion_origen"}

    # Simulación de creación de etiqueta
    tracking = f"TRK-{id_dev[:8]}"
    url = f"https://example.com/etiquetas/{id_dev}.pdf"

    return {"success": True, "url_etiqueta": url, "tracking_id": tracking, "mensaje": "Etiqueta generada correctamente"}
