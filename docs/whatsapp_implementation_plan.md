# Cómo hacerlo funcionar en WhatsApp (plan de implementación)

## 1) Arquitectura mínima (MVP)
1. **WhatsApp API** (Meta Cloud API o BSP) recibe mensajes.
2. **Webhook backend** (tu servidor) procesa cada mensaje entrante.
3. **Orquestador de conversación** llama al modelo con:
   - `system instruction` (este repo)
   - historial de conversación
   - estado del pedido actual
4. **Validador de pedido** revisa faltantes (condimentos, entrega, pago, etc.).
5. **Respuesta al cliente por WhatsApp**.
6. **Persistencia** en DB (pedido + estado + mensajes).

---

## 2) Estados sugeridos del pedido
Usar un estado por conversación para que sea robusto:
- `new`
- `collecting_items`
- `collecting_customizations`
- `collecting_delivery`
- `collecting_payment`
- `awaiting_confirmation`
- `confirmed`
- `cancelled`

---

## 3) Estructura de datos recomendada
```json
{
  "conversation_id": "wa:+549...",
  "customer_name": null,
  "items": [
    {
      "product": "Lomo",
      "variant": "Special",
      "quantity": 1,
      "condiments": [],
      "extras": [],
      "without": []
    }
  ],
  "delivery": {
    "type": null,
    "address": null,
    "reference": null
  },
  "payment": {
    "method": null,
    "cash_with": null
  },
  "missing_fields": [],
  "status": "collecting_customizations"
}
```

---

## 4) Reglas de validación clave
- Si item contiene `Special`, confirmar condimentos faltantes.
- Si `delivery.type = envío`, dirección es obligatoria.
- Si `payment.method = efectivo`, pedir `cash_with`.
- Si hay `Molleja`, bloquear confirmación hasta `stock_confirmed = true`.
- No pasar a `confirmed` sin confirmación explícita del cliente.

---

## 5) Flujo de mensajes (resumido)
1. Llega mensaje del cliente.
2. Parseás intención + actualizás estado estructurado.
3. Corrés validaciones.
4. Si faltan campos, respondés con la próxima repregunta priorizada.
5. Si está completo, mandás resumen final.
6. Si el cliente confirma, guardás `confirmed` y notificás cocina/caja.

---

## 6) Qué construir ahora (siguiente sprint)
1. Definir un **menú JSON** con catálogo y variantes válidas.
2. Implementar webhook `/whatsapp/inbound`.
3. Implementar módulo `order_validator`.
4. Implementar plantilla de resumen final.
5. Guardar pedidos en una DB simple (SQLite/Postgres).

Con esto ya podés operar pedidos reales por WhatsApp y luego escalar a tablet/pantalla de cocina.
