# 1. Product Vision
- **Qué producto es:** una plataforma web de inteligencia genética para cannabis orientada a breeders, que combina exploración pública de genéticas, visualización genealógica interactiva y un workspace privado de breeding basado en evidencia.
- **Qué problema resuelve:** hoy la información genética está fragmentada (foros, planillas, mensajes, memoria del breeder), sin trazabilidad robusta entre cruzas, fenotipos y decisiones de selección.
- **Para quién está pensado:** breeders independientes, micro-bancos/comunidades, coleccionistas avanzados y usuarios exploradores que quieren entender linajes reales.
- **Necesidad real que cubre:** registrar y comunicar el proceso de mejora genética de punta a punta: origen, cruza, batch fenotípico, observaciones comparables y selección final.
- **Por qué sería valioso:** convierte conocimiento tácito en activo estructurado, reutilizable y verificable; acelera decisiones de breeding y mejora credibilidad pública del proyecto genético.

# 2. Unique Value Proposition
- **Vs apps de cultivo:** no se centra en riego/EC/plagas/diario de cultivo; se centra en decisiones de breeding, genealogía y selección fenotípica.
- **Vs bancos de semillas:** no es solo catálogo de productos; es un sistema de trazabilidad del proceso que originó cada línea.
- **Vs strain databases tradicionales:** no solo describe “strain cards”; modela relaciones parentales dinámicas, eventos de cruza y evolución generacional.
- **Vs trackers genéricos:** incorpora semántica genética nativa (madre/padre, F1/F2/S1, BX, lote fenotípico, descarte, keeper) y visualización de grafo aplicable al trabajo real del breeder.

# 3. User Types
## 3.1 Breeder independiente
- **Objetivo:** documentar su pipeline genético y no perder contexto entre ciclos.
- **Frustraciones:** notas desordenadas, dificultad para comparar fenos, poca capacidad de mostrar proceso sin exponer todo.
- **Valor recibido:** workspace de proyecto + fenotipos + decisiones, con control fino de privacidad y salida visual para storytelling técnico.

## 3.2 Breeder/comunidad/banco pequeño
- **Objetivo:** coordinar equipo, estandarizar criterios de selección y publicar líneas con respaldo.
- **Frustraciones:** criterios inconsistentes, datos dispersos por personas, baja trazabilidad para la comunidad.
- **Valor recibido:** estructura colaborativa por proyectos, historial auditable de decisiones y perfil público confiable por genética.

## 3.3 Coleccionista o investigador de genéticas
- **Objetivo:** entender linajes, autenticidad y evolución de líneas.
- **Frustraciones:** información contradictoria, árboles incompletos, falta de contexto histórico.
- **Valor recibido:** explorador potente con grafo navegable, fuentes/notas y relaciones explícitas entre líneas.

## 3.4 Usuario explorador/general
- **Objetivo:** descubrir genéticas y aprender relaciones entre familias.
- **Frustraciones:** terminología técnica confusa y datos en exceso.
- **Valor recibido:** experiencia visual guiada, fichas claras y capas progresivas de detalle técnico.

# 4. MVP
## Imprescindible para v1
1. Registro/login + perfiles de breeder.
2. Entidad de genética con ficha básica + tags.
3. Relaciones genéticas (madre/padre/cross) y árbol interactivo básico.
4. Proyectos privados de breeding.
5. Creación de cruza dentro de proyecto.
6. Lotes de fenotipos + evaluación simple (score, notas, estado: keeper/discard).
7. Visibilidad por recurso (público/privado/unlisted).

## Importante pero puede esperar
1. Comparador avanzado de fenotipos (matriz multicriterio).
2. Versionado de árbol con historial temporal.
3. Roles de equipo más sofisticados (editor/reviewer).
4. Importación CSV/plantillas de carga.
5. Comentarios/comunidad en perfiles públicos.

## Avanzado / futuro
1. Motor de recomendación de cruces basado en objetivos.
2. Métricas predictivas por linaje/familia.
3. Verificación criptográfica de hitos (proof-of-process).
4. API pública para investigadores.
5. Integración con laboratorio (terpenos/cannabinoides).

## Priorización (impacto x complejidad x velocidad)
- Alta diferenciación y baja complejidad relativa: árbol básico + creación de cruza + fenotipos.
- Alta diferenciación y complejidad media: permisos granulares + comparación fenotípica.
- Alta complejidad para después: predicción y verificación avanzada.

# 5. Core Features
1. **Explorador de genéticas:** buscador por nombre, breeder, familia, generación (F1/F2/BX/S1), tags y popularidad.
2. **Ficha/perfil de genética:** identidad genética, breeder origen, parentales, generación, objetivos, notas históricas, media gallery.
3. **Árbol genealógico interactivo:** vista centrada en genética seleccionada, navegación bidireccional (ancestros/descendencia), leyenda de tipos de relación.
4. **Creación de cruzas:** formulario estructurado (madre, padre, método, generación esperada, objetivo), con creación automática de nodo y relaciones.
5. **Seguimiento de fenotipos:** lotes por corrida, registro por individuo (código, rasgos, scores, decisión).
6. **Notas y observaciones:** notas por genética, por cruza y por fenotipo; soporte de notas privadas y públicas.
7. **Galería de imágenes:** imágenes por entidad con metadatos (fecha, etapa, autor, visibilidad).
8. **Proyectos de breeding:** contenedor operativo que agrupa cruzas, lotes y decisiones por objetivo.
9. **Visibilidad pública/privada:** control por proyecto y por elemento; opción de publicar solo resultados sin exponer proceso completo.

# 6. Information Architecture
## Navegación principal
- **Pública:** Home, Explorar, Genéticas, Breeders, Árboles destacados.
- **Autenticada (breeder):** Dashboard, Proyectos, Cruzas, Fenotipos, Biblioteca de genéticas, Configuración.

## Secciones y relación entre pantallas
- `Home -> Explorar -> Perfil Genética -> Árbol -> Perfil de nodo relacionado`.
- `Dashboard -> Proyecto -> Nueva Cruza -> Lote Fenotipos -> Comparación -> Decisión`.

## Estructura mental del usuario
- **Explorador:** “quiero entender de dónde viene y a qué se conecta”.
- **Breeder:** “quiero documentar qué hice, por qué elegí X y qué publicar”.

## Flujo principal: usuario explorador
1. Busca genética.
2. Abre perfil.
3. Cambia a vista árbol.
4. Navega a parental o descendiente.
5. Guarda favoritas o comparte enlace.

## Flujo principal: breeder documentando nueva línea
1. Crea/abre proyecto.
2. Registra nueva cruza (madre/padre + objetivo).
3. Genera lote fenotípico.
4. Carga observaciones y scores por fenotipo.
5. Marca seleccionados/descartes.
6. Publica resumen o mantiene privado.

# 7. Main Screens
1. **Home:** propuesta de valor, buscador global, árboles destacados, breeders destacados.
2. **Explorador/Search:** barra de búsqueda + filtros laterales + resultados en cards/lista.
3. **Perfil de genética:** header técnico, datos clave, parentales, descendencia, notas, imágenes, CTA a árbol.
4. **Árbol genealógico:** canvas interactivo con minimapa, filtros de profundidad y tipo de relación.
5. **Dashboard del breeder:** estado de proyectos, tareas pendientes, actividad reciente, métricas de selección.
6. **Detalle de proyecto genético:** objetivo, timeline de cruzas, lotes fenotípicos y decisiones acumuladas.
7. **Módulo de fenotipos:** tabla + vista comparativa de individuos, scores y estado final.
8. **Formulario de nueva cruza:** wizard simple (parentales -> método/generación -> objetivos -> visibilidad).

# 8. Data Model
## Entidades y significado
- **users:** cuentas base (auth, identidad).
- **breeders:** perfil público/profesional asociado a uno o varios users.
- **projects:** iniciativas de breeding con objetivo y alcance.
- **genetics:** líneas genéticas (canónicas o en desarrollo).
- **genetic_relationships:** aristas del grafo (parent_of, backcross_of, self_of, descendant_of).
- **crosses:** evento de cruza (qué se cruzó, cuándo, objetivo, resultado esperado).
- **phenotype_batches:** cohortes de evaluación fenotípica por cruza/corrida.
- **phenotypes:** individuos evaluados dentro de batch.
- **observations:** notas estructuradas o libres vinculables a múltiples entidades.
- **images:** activos visuales con metadatos y visibilidad.
- **tags:** taxonomía flexible (familia, perfil aromático, objetivo, status).
- **visibility_permissions:** ACL por recurso (owner/team/public/unlisted).

## Relaciones clave
- `users` M:N `breeders` (mediante membresía/roles).
- `breeders` 1:N `projects`.
- `projects` 1:N `crosses`, 1:N `phenotype_batches`.
- `genetics` M:N `genetics` via `genetic_relationships`.
- `crosses` N:1 `genetics` (mother), N:1 `genetics` (father), opcional N:1 `genetics` (result_genetic).
- `phenotype_batches` N:1 `crosses`; `phenotypes` N:1 `phenotype_batches`.
- `observations/images/tags` polimórficas (apuntan a genetics, crosses, phenotypes, projects).

## Mínimo necesario para arrancar
- users, breeders, projects, genetics, genetic_relationships, crosses, phenotype_batches, phenotypes, observations, visibility_permissions.
- images y tags pueden entrar en v1 si no bloquean velocidad.

# 9. Technical Architecture
## Stack recomendado
- **Frontend:** Next.js (App Router) + TypeScript + Tailwind + shadcn/ui.
- **Backend:** NestJS (modular) o Next.js API routes para v1; recomiendo NestJS si querés escalar dominio complejo.
- **DB:** PostgreSQL + Prisma ORM.
- **Auth:** Auth.js (si full Next) o Supabase Auth/Clerk.
- **Storage imágenes:** S3-compatible (AWS S3 / Cloudflare R2) + signed URLs.
- **Grafos/árbol:** React Flow para edición/inspección + ELK/Dagre para layout automático.
- **Buscador/filtros:** PostgreSQL Full-Text + trigram (pg_trgm); pasar a Meilisearch/Typesense cuando crezca catálogo.
- **Hosting/deploy:** Vercel (frontend) + Render/Fly.io (backend) + Neon/Supabase (Postgres administrado).

## Por qué este stack
- Productividad alta para iterar UX compleja.
- Type-safety end-to-end (TS + Prisma).
- PostgreSQL modela bien relaciones y permite extender a consultas de grafo/histórico.
- React Flow acelera la entrega de visualización interactiva sin construir motor custom desde cero.

# 10. UX/UI Guidelines
1. **Diseño por capas de complejidad:** vista básica por defecto, detalles avanzados bajo toggles/acordeones.
2. **Árbol legible:** foco en nodo central, profundidad controlable (1-2-3 saltos), minimapa y resaltado de path activo.
3. **Codificación visual consistente:** colores por tipo de relación (madre/padre/backcross/self), badges de generación.
4. **Navegación fluida entre nodos:** click abre quick-card con acciones (ver perfil, centrar, fijar comparación).
5. **Evitar sobrecarga técnica:** “resumen humano” arriba, bloque técnico abajo (metadata completa).
6. **Comparación fenotípica usable:** tabla sticky con criterios configurables y vista “solo diferencias”.
7. **Performance UX:** virtualización de listas, lazy loading de ramas del árbol, caché de consultas.
8. **Confianza de dato:** mostrar fuente, autor, fecha y nivel de verificación en cada ficha.

# 11. Differentiating Features (10)
1. **Timeline genético auditable** por proyecto (eventos + decisiones).
2. **Modo “Breeding Story” público** (narrativa visual de cómo nació una línea).
3. **Árbol comparativo de dos genéticas** con ancestro común resaltado.
4. **Matriz de selección fenotípica** configurable por objetivo (resina, vigor, estructura, aroma).
5. **Snapshots de decisión** (por qué se eligió keeper A vs B).
6. **Niveles de verificación de datos** (declarado, corroborado por terceros, documentado con evidencia).
7. **Plantillas de protocolos de selección** (indoor, outdoor, hash-focused, etc.).
8. **Publicación parcial inteligente** (ocultar parentales sensibles y mostrar solo rama final).
9. **Detección de inconsistencias genealógicas** (alertas de ciclos imposibles o generaciones incoherentes).
10. **Ficha “Evolución de línea”** (de cruza inicial a versión estabilizada).

# 12. Risks and Challenges + Mitigación
1. **Complejidad del modelo genético:** iniciar con ontología corta de relaciones; ampliar por versiones.
2. **Calidad/veracidad de datos:** sistema de confianza por fuente + historial de cambios + moderación comunitaria.
3. **UX de grafos complejos:** límites de profundidad por defecto, filtros, clustering por generaciones.
4. **Carga manual pesada:** formularios en wizard, duplicar desde cruza previa, import CSV.
5. **Adopción por breeders:** onboarding con plantillas reales y beneficio inmediato (trazabilidad + perfil público).
6. **Privacidad del trabajo genético:** ACL granular, proyectos privados, publicación parcial y enlaces unlisted.

# 13. Roadmap
## Fase 1: validación (0-8 semanas)
- Explorer público básico + perfiles de genética.
- Árbol interactivo inicial.
- Workspace breeder mínimo: proyectos, cruzas, lotes fenotipos.
- Meta: validar retención de breeders piloto y utilidad del grafo.

## Fase 2: producto usable (2-5 meses)
- Comparación fenotípica robusta.
- Colaboración por equipo/roles.
- Historial de cambios y mejores filtros de búsqueda.
- Meta: convertir uso ocasional en flujo operativo recurrente.

## Fase 3: diferenciación fuerte (6-12 meses)
- Modo storytelling público avanzado.
- Validación/verificación de datos por evidencia.
- Recomendaciones y analítica de breeding.
- Meta: posicionamiento como estándar de trazabilidad genética.

# 14. First Build Proposal (primeras 2 semanas)
## Qué haría exactamente
- Semana 1:
  1. Setup base (auth, DB, layout, design system).
  2. CRUD de genetics + relationships.
  3. Search básico + perfil de genética.
- Semana 2:
  1. Vista árbol interactiva con React Flow.
  2. Módulo breeder mínimo: proyecto + nueva cruza.
  3. Lote fenotipos simple con notas y estado keeper/discard.

## Pantallas a construir primero
1. Explorador/Search.
2. Perfil de genética.
3. Árbol genealógico.
4. Dashboard breeder (simple).
5. Nueva cruza + lote de fenotipos (MVP forms).

## Entidades mínimas
- users, breeders, projects, genetics, genetic_relationships, crosses, phenotype_batches, phenotypes, observations.

## Qué dejaría afuera sin culpa
- Recomendador inteligente.
- Marketplace/social feed.
- Integración de laboratorio.
- Permisos súper granulares por campo.
- Comparador fenotípico avanzado (solo versión básica en tabla).

# 15. Bonus
## 15.1 User stories (10)
1. Como **explorador**, quiero buscar una genética por nombre para entender rápidamente su origen.
2. Como **explorador**, quiero ver el árbol de una genética para navegar sus parentales y descendencia.
3. Como **breeder independiente**, quiero crear un proyecto para agrupar mi trabajo por objetivo genético.
4. Como **breeder**, quiero registrar una nueva cruza madre/padre para mantener trazabilidad del proceso.
5. Como **breeder**, quiero crear un lote fenotípico para evaluar individuos de una cruza específica.
6. Como **breeder**, quiero puntuar fenotipos por criterios para decidir cuáles conservar.
7. Como **breeder**, quiero marcar un fenotipo como keeper o descarte para justificar decisiones.
8. Como **breeder**, quiero guardar notas privadas por fenotipo para documentar hallazgos sensibles.
9. Como **banco pequeño**, quiero publicar solo parte de un proyecto para comunicar resultados sin exponer todo.
10. Como **investigador**, quiero ver relaciones verificadas y fuentes para confiar en la información genética.

## 15.2 Schema inicial (SQL orientativo)
```sql
create table users (
  id uuid primary key,
  email text unique not null,
  display_name text,
  created_at timestamptz default now()
);

create table breeders (
  id uuid primary key,
  slug text unique not null,
  name text not null,
  bio text,
  visibility text not null default 'public',
  created_at timestamptz default now()
);

create table breeder_members (
  breeder_id uuid references breeders(id) on delete cascade,
  user_id uuid references users(id) on delete cascade,
  role text not null default 'owner',
  primary key (breeder_id, user_id)
);

create table projects (
  id uuid primary key,
  breeder_id uuid not null references breeders(id) on delete cascade,
  name text not null,
  objective text,
  visibility text not null default 'private',
  created_at timestamptz default now()
);

create table genetics (
  id uuid primary key,
  breeder_id uuid references breeders(id),
  canonical_name text not null,
  generation text,
  status text default 'in_development',
  description text,
  visibility text not null default 'public',
  created_at timestamptz default now()
);

create table genetic_relationships (
  id uuid primary key,
  from_genetic_id uuid not null references genetics(id) on delete cascade,
  to_genetic_id uuid not null references genetics(id) on delete cascade,
  relation_type text not null, -- mother_of, father_of, backcross_of, self_of
  confidence smallint default 1,
  created_at timestamptz default now()
);

create table crosses (
  id uuid primary key,
  project_id uuid not null references projects(id) on delete cascade,
  mother_genetic_id uuid references genetics(id),
  father_genetic_id uuid references genetics(id),
  resulting_genetic_id uuid references genetics(id),
  generation_expected text,
  objective text,
  happened_at date,
  visibility text not null default 'private'
);

create table phenotype_batches (
  id uuid primary key,
  project_id uuid not null references projects(id) on delete cascade,
  cross_id uuid references crosses(id) on delete set null,
  name text not null,
  started_at date,
  visibility text not null default 'private'
);

create table phenotypes (
  id uuid primary key,
  batch_id uuid not null references phenotype_batches(id) on delete cascade,
  code text not null,
  vigor_score numeric(4,2),
  resin_score numeric(4,2),
  aroma_score numeric(4,2),
  structure_score numeric(4,2),
  decision text default 'pending', -- keeper/discard/pending
  created_at timestamptz default now()
);

create table observations (
  id uuid primary key,
  author_user_id uuid references users(id),
  entity_type text not null, -- project/genetic/cross/phenotype
  entity_id uuid not null,
  note text not null,
  visibility text not null default 'private',
  created_at timestamptz default now()
);

create table images (
  id uuid primary key,
  uploader_user_id uuid references users(id),
  entity_type text not null,
  entity_id uuid not null,
  storage_key text not null,
  caption text,
  visibility text not null default 'private',
  created_at timestamptz default now()
);

create table tags (
  id uuid primary key,
  name text unique not null,
  category text
);

create table entity_tags (
  tag_id uuid references tags(id) on delete cascade,
  entity_type text not null,
  entity_id uuid not null,
  primary key (tag_id, entity_type, entity_id)
);
```

## 15.3 Estructura de carpetas sugerida
```txt
/apps
  /web                # Next.js app
    /app
      /(public)
      /(breeder)
      /api
    /components
      /genetics
      /graph
      /phenotypes
      /ui
    /lib
      /auth
      /db
      /search
      /permissions
    /styles
/packages
  /domain             # tipos, reglas de negocio, validaciones
  /ui                 # design system compartido
  /config             # eslint, tsconfig, tailwind config
  /analytics          # eventos producto
/infrastructure
  docker-compose.yml
  terraform/
/docs
  product/
  architecture/
  adr/
```

# 16. ¿Cómo lo ejecuto? (Runbook práctico)

Abajo tenés una forma **realista** de correr una primera versión en local en 1 día, usando el stack recomendado (Next.js + PostgreSQL + Prisma).

## 16.1 Prerrequisitos
- Node.js 20+
- pnpm 9+
- Docker + Docker Compose

## 16.2 Bootstrap rápido del proyecto
```bash
# 1) crear carpeta base
mkdir breeders-genetics-platform && cd breeders-genetics-platform

# 2) iniciar app web (Next.js + TS)
pnpm create next-app@latest apps/web --ts --eslint --app --src-dir false --tailwind --import-alias "@/*"

# 3) inicializar workspace
cat > package.json << 'JSON'
{
  "name": "breeders-genetics-platform",
  "private": true,
  "workspaces": ["apps/*", "packages/*"],
  "scripts": {
    "dev": "pnpm --filter web dev",
    "db:up": "docker compose up -d",
    "db:down": "docker compose down",
    "db:migrate": "pnpm --filter web prisma migrate dev",
    "db:seed": "pnpm --filter web prisma db seed"
  }
}
JSON
```

## 16.3 Levantar PostgreSQL
Crear `docker-compose.yml` en la raíz:
```yaml
services:
  db:
    image: postgres:16
    container_name: breeders_db
    restart: unless-stopped
    environment:
      POSTGRES_DB: breeders
      POSTGRES_USER: breeders
      POSTGRES_PASSWORD: breeders
    ports:
      - "5432:5432"
    volumes:
      - pgdata:/var/lib/postgresql/data

volumes:
  pgdata:
```

Luego:
```bash
pnpm db:up
```

## 16.4 Configurar Prisma
En `apps/web`:
```bash
cd apps/web
pnpm add @prisma/client
pnpm add -D prisma
npx prisma init
```

Editar `apps/web/.env`:
```env
DATABASE_URL="postgresql://breeders:breeders@localhost:5432/breeders?schema=public"
```

Copiar el schema SQL del punto **15.2** y transformarlo a `schema.prisma` (o arrancar por tablas mínimas: `users`, `breeders`, `projects`, `genetics`, `genetic_relationships`, `crosses`, `phenotype_batches`, `phenotypes`, `observations`).

Migrar:
```bash
pnpm db:migrate
```

## 16.5 Pantallas mínimas para ver valor en la primera corrida
Implementar estas rutas en `apps/web/app`:
- `/` Home
- `/explore` Explorador
- `/genetics/[slug]` Perfil genética
- `/genetics/[slug]/tree` Árbol genealógico
- `/breeder/dashboard` Dashboard breeder
- `/breeder/projects/[id]` Proyecto
- `/breeder/crosses/new` Nueva cruza
- `/breeder/batches/[id]` Fenotipos

## 16.6 Seed mínimo recomendado
Cargar:
- 1 breeder
- 6 genetics
- 8 relaciones genéticas (madre/padre + descendencia)
- 1 proyecto
- 1 cruza
- 1 batch con 12 fenotipos

Con eso ya podés validar:
1. búsqueda
2. navegación de árbol
3. registro de cruza
4. selección keeper/discard

## 16.7 Correr en local
Desde la raíz:
```bash
pnpm install
pnpm dev
```
Abrir: `http://localhost:3000`

## 16.8 Definición de “listo para demo” (v0)
- Búsqueda funcional por nombre de genética.
- Perfil con parentales + descendencia.
- Árbol interactivo navegable entre nodos.
- Alta de cruza en proyecto breeder.
- Batch fenotípico con notas y decisión keeper/discard.
- Control simple de visibilidad (público/privado).

---

Si querés, el próximo paso es que te deje un **script de scaffolding** (`scripts/bootstrap.sh`) + `schema.prisma` inicial para levantar este v0 sin fricción.
