"""Order validator for WhatsApp sandwich shop MVP."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import json
from typing import Any


@dataclass
class ValidationResult:
    missing_fields: list[str]
    errors: list[str]
    can_confirm: bool


def load_menu(menu_path: str | Path = "data/menu.json") -> dict[str, Any]:
    with open(menu_path, "r", encoding="utf-8") as f:
        return json.load(f)


def validate_order(order: dict[str, Any], menu: dict[str, Any]) -> ValidationResult:
    missing_fields: list[str] = []
    errors: list[str] = []

    items = order.get("items") or []
    if not items:
        missing_fields.append("items")

    products = menu.get("products", {})

    for i, item in enumerate(items):
        prefix = f"items[{i}]"
        product = item.get("product")
        quantity = item.get("quantity")

        if not product:
            missing_fields.append(f"{prefix}.product")
            continue

        if product not in products:
            errors.append(f"{prefix}.product_invalid:{product}")
            continue

        if not isinstance(quantity, int) or quantity <= 0:
            missing_fields.append(f"{prefix}.quantity")

        variant = item.get("variant")
        if variant and variant.lower() == "special":
            if not products[product].get("supports_special", False):
                errors.append(f"{prefix}.special_not_supported:{product}")
            # force explicit condiments for special too
            condiments = item.get("condiments") or []
            if len(condiments) == 0:
                missing_fields.append(f"{prefix}.condiments")

        if products[product].get("requires_stock_check"):
            if item.get("stock_confirmed") is not True:
                missing_fields.append(f"{prefix}.stock_confirmed")

    delivery = order.get("delivery") or {}
    delivery_type = delivery.get("type")
    if delivery_type not in menu.get("delivery_types", []):
        missing_fields.append("delivery.type")
    elif delivery_type == "envio":
        if not delivery.get("address"):
            missing_fields.append("delivery.address")

    payment = order.get("payment") or {}
    method = payment.get("method")
    if method not in menu.get("payment_methods", []):
        missing_fields.append("payment.method")
    elif method == "efectivo" and not payment.get("cash_with"):
        missing_fields.append("payment.cash_with")

    if not order.get("customer_name"):
        missing_fields.append("customer_name")

    can_confirm = len(missing_fields) == 0 and len(errors) == 0
    return ValidationResult(
        missing_fields=sorted(set(missing_fields)),
        errors=sorted(set(errors)),
        can_confirm=can_confirm,
    )


def next_question_hint(validation: ValidationResult) -> str | None:
    """Return next follow-up question target using priority: prep -> delivery -> payment -> identity."""
    if validation.can_confirm:
        return None

    priorities = [
        "items",
        "delivery",
        "payment",
        "customer_name",
    ]

    for p in priorities:
        for field in validation.missing_fields:
            if field.startswith(p):
                return field
    return validation.missing_fields[0] if validation.missing_fields else None
