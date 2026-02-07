# Cómo correr en local (VS Code)

## 1) Requisitos
- Python 3.10+

## 2) Abrir proyecto en VS Code
```bash
cd el_special
code .
```

## 3) (Opcional) entorno virtual
```bash
python -m venv .venv
source .venv/bin/activate
```

## 4) Levantar servidor local
```bash
python -m src.local_server --host 0.0.0.0 --port 8000
```

## 5) Probar en navegador
- Chat UI local: `http://localhost:8000`
- Healthcheck: `http://localhost:8000/health`

## 6) Probar API con curl
```bash
curl -X POST http://localhost:8000/api/chat \
  -H 'Content-Type: application/json' \
  -d '{"conversation_id":"demo","message":"quiero 1 lomo special"}'
```

## Puertos
- `8000`: servidor local (UI + API)

## Debug
- En la pantalla web se ve el chat y abajo el estado del pedido en JSON.
- El estado vive en memoria por `conversation_id`.
- Si reiniciás el server, se reinician las conversaciones.
