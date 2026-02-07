from __future__ import annotations

import re
from copy import deepcopy
from dataclasses import dataclass, field
from typing import Any

from src.order_validator import load_menu, next_question_hint, validate_order


def _default_order() -> dict[str, Any]:
    return {
        "customer_name": None,
        "items": [],
        "delivery": {"type": None, "address": None, "reference": None},
        "payment": {"method": None, "cash_with": None},
        "awaiting_confirmation": False,
        "status": "new",
    }


PRODUCT_ALIASES = {
    "lomo": "lomo",
    "choripan": "choripan",
    "chori": "choripan",
    "hamburguesa": "hamburguesa",
    "molleja": "molleja",
    "carlitos": "carlitos",
    "tostado": "tostado",
    "miga": "sanguches_de_miga",
    "primavera": "primavera",
    "caño": "cano",
    "cano": "cano",
    "frankfurt": "frankfurt",
}

CONDIMENTS = ["mayonesa", "ketchup", "mostaza", "salsa golf", "picante", "tomate", "lechuga", "cebolla"]


@dataclass
class ChatSession:
    conversation_id: str
    order: dict[str, Any] = field(default_factory=_default_order)
    history: list[dict[str, str]] = field(default_factory=list)


class ChatEngine:
    def __init__(self, menu_path: str = "data/menu.json") -> None:
        self.menu = load_menu(menu_path)
        self.sessions: dict[str, ChatSession] = {}

    def get_session(self, conversation_id: str) -> ChatSession:
        if conversation_id not in self.sessions:
            self.sessions[conversation_id] = ChatSession(conversation_id=conversation_id)
        return self.sessions[conversation_id]

    def handle_message(self, conversation_id: str, message: str) -> dict[str, Any]:
        session = self.get_session(conversation_id)
        text = message.strip().lower()
        session.history.append({"role": "user", "text": message})

        if session.order.get("awaiting_confirmation") and text in {"si", "sí", "dale", "ok", "confirmo"}:
            session.order["status"] = "confirmed"
            session.order["awaiting_confirmation"] = False
            reply = "¡Listo, pedido confirmado! 🙌 Enseguida lo pasamos a cocina."
            session.history.append({"role": "assistant", "text": reply})
            return self._response(session, reply)

        self._extract_data(session.order, text)

        validation = validate_order(session.order, self.menu)
        if validation.can_confirm:
            session.order["awaiting_confirmation"] = True
            session.order["status"] = "awaiting_confirmation"
            reply = self._build_summary(session.order)
        else:
            session.order["status"] = "collecting_data"
            missing = next_question_hint(validation)
            reply = self._question_for_missing(missing)

        session.history.append({"role": "assistant", "text": reply})
        return self._response(session, reply)

    def _extract_data(self, order: dict[str, Any], text: str) -> None:
        # Name
        name_match = re.search(r"(?:soy|nombre|me llamo)\s+([a-záéíóúñ]+)", text)
        if name_match:
            order["customer_name"] = name_match.group(1).capitalize()

        # Delivery (accept common variants: retiro/retirar, envio/enviar)
        if re.search(r"\bretir(?:o|ar)?\b", text):
            order["delivery"]["type"] = "retiro"
        if re.search(r"\benvi(?:o|ar|á)\b", text):
            order["delivery"]["type"] = "envio"
        addr_match = re.search(r"(?:direccion|dirección)\s*[:\-]?\s*(.+)$", text)
        if addr_match:
            order["delivery"]["address"] = addr_match.group(1).strip()

        # Payment
        if "efectivo" in text:
            order["payment"]["method"] = "efectivo"
        if "transferencia" in text:
            order["payment"]["method"] = "transferencia"
        money_match = re.search(r"\$\s?(\d{3,})", text)
        if money_match and order["payment"].get("method") == "efectivo":
            order["payment"]["cash_with"] = int(money_match.group(1))

        # Item parsing (simple)
        product = None
        for alias, canonical in PRODUCT_ALIASES.items():
            if alias in text:
                product = canonical
                break

        if product:
            qty = 1
            qty_match = re.search(r"(\d+)\s*(x|de)?\s*" + re.escape(product), text)
            if qty_match:
                qty = int(qty_match.group(1))
            variant = "special" if "special" in text else None

            condiments = [c for c in CONDIMENTS if c in text]
            without = re.findall(r"sin\s+([a-záéíóúñ]+)", text)

            existing = None
            for item in order["items"]:
                if item.get("product") == product and item.get("variant") == variant:
                    existing = item
                    break

            if existing:
                existing["quantity"] += qty
                for c in condiments:
                    if c not in existing["condiments"]:
                        existing["condiments"].append(c)
                for w in without:
                    if w not in existing["without"]:
                        existing["without"].append(w)
            else:
                order["items"].append(
                    {
                        "product": product,
                        "variant": variant,
                        "quantity": qty,
                        "condiments": condiments,
                        "extras": [],
                        "without": without,
                        "stock_confirmed": False if product == "molleja" else True,
                    }
                )

    def _question_for_missing(self, missing: str | None) -> str:
        questions = {
            "items": "¿Qué te preparo? Pasame producto y cantidad 🙌",
            "items[0].product": "¿Qué producto querés pedir?",
            "items[0].quantity": "¿Cuántos querés?",
            "items[0].condiments": "¿Con qué condimentos te lo preparo?",
            "items[0].stock_confirmed": "¿Me esperás un minuto que confirmo stock de molleja?",
            "delivery.type": "¿Es para retirar o envío?",
            "delivery.address": "¿Me pasás la dirección para el envío?",
            "payment.method": "¿Abonás en efectivo o transferencia?",
            "payment.cash_with": "Si pagás en efectivo, ¿con cuánto abonás para preparar el cambio?",
            "customer_name": "¿A nombre de quién va el pedido?",
        }
        if missing in questions:
            return questions[missing]

        if missing and missing.startswith("items"):
            return "¿Me confirmás los detalles del producto (cantidad/condimentos)?"
        return "¿Me pasás un dato más para cerrar el pedido?"

    def _build_summary(self, order: dict[str, Any]) -> str:
        lines = ["**Resumen de tu pedido**"]
        for item in order["items"]:
            product = self.menu["products"][item["product"]]["display_name"]
            variant = " Special" if item.get("variant") == "special" else ""
            lines.append(f"- {item['quantity']}x {product}{variant}")
            if item.get("condiments"):
                lines.append(f"  - Condimentos: {', '.join(item['condiments'])}")
            if item.get("without"):
                lines.append(f"  - Sin: {', '.join(item['without'])}")

        lines.append(f"- Entrega: {order['delivery']['type']}")
        if order["delivery"].get("address"):
            lines.append(f"- Dirección: {order['delivery']['address']}")
        lines.append(f"- Pago: {order['payment']['method']}")
        if order["payment"].get("cash_with"):
            lines.append(f"- Efectivo con: ${order['payment']['cash_with']}")
        lines.append(f"- Nombre: {order['customer_name']}")
        lines.append("\n¿Está correcto así y lo confirmamos?")
        return "\n".join(lines)

    def _response(self, session: ChatSession, reply: str) -> dict[str, Any]:
        return {
            "reply": reply,
            "order": deepcopy(session.order),
            "history": deepcopy(session.history),
        }
