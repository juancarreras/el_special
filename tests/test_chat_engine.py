import unittest

from src.chat_engine import ChatEngine


class TestChatEngine(unittest.TestCase):
    def setUp(self):
        self.engine = ChatEngine(menu_path="data/menu.json")

    def test_first_prompt_when_no_items(self):
        out = self.engine.handle_message("c1", "hola")
        self.assertIn("qué te preparo", out["reply"].lower())

    def test_special_needs_condiments(self):
        out = self.engine.handle_message("c2", "quiero 1 lomo special")
        self.assertIn("condimentos", out["reply"].lower())

    def test_delivery_detects_retirar_variant(self):
        cid = "c4"
        self.engine.handle_message(cid, "haceme un lomo")
        out = self.engine.handle_message(cid, "para retirar")
        self.assertEqual("retiro", out["order"]["delivery"]["type"])
        self.assertIn("abonás", out["reply"].lower())

    def test_valid_flow_reaches_confirmation(self):
        cid = "c3"
        self.engine.handle_message(cid, "quiero 1 lomo special con mayonesa")
        self.engine.handle_message(cid, "retiro")
        self.engine.handle_message(cid, "transferencia")
        out = self.engine.handle_message(cid, "soy juan")
        self.assertIn("resumen de tu pedido", out["reply"].lower())


if __name__ == "__main__":
    unittest.main()
