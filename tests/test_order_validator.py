import unittest

from src.order_validator import load_menu, validate_order, next_question_hint


class TestOrderValidator(unittest.TestCase):
    def setUp(self):
        self.menu = load_menu("data/menu.json")

    def test_requires_condiments_for_special(self):
        order = {
            "customer_name": "Juan",
            "items": [{"product": "lomo", "variant": "special", "quantity": 1, "condiments": []}],
            "delivery": {"type": "retiro"},
            "payment": {"method": "transferencia"},
        }
        result = validate_order(order, self.menu)
        self.assertIn("items[0].condiments", result.missing_fields)
        self.assertFalse(result.can_confirm)

    def test_requires_stock_check_for_molleja(self):
        order = {
            "customer_name": "Ana",
            "items": [{"product": "molleja", "variant": "special", "quantity": 1, "condiments": ["mostaza"]}],
            "delivery": {"type": "retiro"},
            "payment": {"method": "transferencia"},
        }
        result = validate_order(order, self.menu)
        self.assertIn("items[0].stock_confirmed", result.missing_fields)

    def test_requires_address_for_delivery(self):
        order = {
            "customer_name": "Luis",
            "items": [{"product": "lomo", "quantity": 1, "condiments": ["mayonesa"]}],
            "delivery": {"type": "envio"},
            "payment": {"method": "transferencia"},
        }
        result = validate_order(order, self.menu)
        self.assertIn("delivery.address", result.missing_fields)

    def test_requires_cash_with_for_cash(self):
        order = {
            "customer_name": "Mica",
            "items": [{"product": "lomo", "quantity": 1, "condiments": ["mostaza"]}],
            "delivery": {"type": "retiro"},
            "payment": {"method": "efectivo"},
        }
        result = validate_order(order, self.menu)
        self.assertIn("payment.cash_with", result.missing_fields)

    def test_valid_order_can_confirm(self):
        order = {
            "customer_name": "Mica",
            "items": [
                {
                    "product": "molleja",
                    "variant": "special",
                    "quantity": 1,
                    "condiments": ["mostaza"],
                    "stock_confirmed": True,
                }
            ],
            "delivery": {"type": "envio", "address": "San Martin 123"},
            "payment": {"method": "efectivo", "cash_with": 10000},
        }
        result = validate_order(order, self.menu)
        self.assertTrue(result.can_confirm)
        self.assertEqual([], result.missing_fields)
        self.assertEqual([], result.errors)

    def test_question_priority_points_to_prep_first(self):
        order = {
            "customer_name": "Juli",
            "items": [{"product": "lomo", "variant": "special", "quantity": 1, "condiments": []}],
            "delivery": {"type": "envio"},
            "payment": {"method": "efectivo"},
        }
        result = validate_order(order, self.menu)
        self.assertEqual("items[0].condiments", next_question_hint(result))


if __name__ == "__main__":
    unittest.main()
