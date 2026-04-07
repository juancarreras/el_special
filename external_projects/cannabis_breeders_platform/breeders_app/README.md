# Breeders Genetics Platform MVP (funcional)

Este módulo implementa una app web funcional con:
- explorador de genéticas
- perfil/listado de genéticas
- árbol genealógico interactivo
- creación de cruzas
- batches y selección de fenotipos
- observaciones básicas vía API

## 1) Instalación desde VS Code (paso a paso)

1. Abrí la carpeta del repo en VS Code (`/workspace/el_special/external_projects/cannabis_breeders_platform`).
2. Abrí una terminal integrada (`Terminal -> New Terminal`).
3. Creá y activá entorno virtual:
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   ```
4. Instalá dependencias:
   ```bash
   pip install -r external_projects/cannabis_breeders_platform/breeders_app/requirements.txt
   ```

## 2) Levantar backend + frontend

Desde la raíz del repo (`/workspace/el_special/external_projects/cannabis_breeders_platform`):
```bash
uvicorn external_projects.cannabis_breeders_platform.breeders_app.backend.main:app --reload --port 8000
```

Abrí en navegador:
- App: http://localhost:8000/
- Healthcheck API: http://localhost:8000/api/health
- Swagger API: http://localhost:8000/docs

## 3) Flujo de uso sugerido (demo rápida)

1. Crear breeder.
2. Crear varias genéticas.
3. Crear relaciones (mother_of / father_of / backcross_of / self_of).
4. Buscar genética en el explorador y abrir árbol.
5. Crear proyecto.
6. Crear cruza (madre/padre).
7. Crear batch de fenotipos.
8. Cargar fenotipos y marcar `keeper` / `discard`.

## 4) Persistencia

- La base se guarda en SQLite local: `breeders.db` en la raíz del repo.
- Para reiniciar datos, borrar ese archivo y volver a levantar el server.

## 5) Alcance

Es un MVP funcional para validar el producto. Próximos pasos recomendados:
- auth + permisos granulares
- carga de imágenes
- roles por equipo breeder
- filtros avanzados y paginación
- layout de árbol multicapa y lazy loading
