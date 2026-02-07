# Próximo paso técnico inmediato

Con lo agregado en este commit ya tenés una base para empezar la integración:

1. `data/menu.json`: fuente de verdad de catálogo y reglas de negocio.
2. `src/order_validator.py`: validación de faltantes/errores para decidir si se puede confirmar.
3. `tests/test_order_validator.py`: pruebas de las reglas críticas del negocio.

## Cómo usarlo en el webhook
- Al llegar un mensaje de WhatsApp, actualizá un objeto `order` por conversación.
- Ejecutá `validate_order(order, menu)`.
- Si `can_confirm = false`, preguntá el primer faltante usando `next_question_hint(...)`.
- Si `can_confirm = true`, mandá resumen final y pedí confirmación explícita.

Este módulo todavía no parsea lenguaje natural; ese parser/orquestador se conecta en la capa del webhook.
