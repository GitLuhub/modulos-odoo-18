# Contexto del Proyecto: Odoo 18 - Desarrollo Empresarial

> **Propósito de este archivo**: Proveer a cualquier agente IA el contexto completo y conciso del proyecto para entenderlo rápidamente y poder trabajar de forma efectiva.

---

## 1. Descripción General

Este es un **proyecto de portafolio profesional** que demuestra desarrollo de módulos personalizados para **Odoo 18** (ERP open-source), con prácticas DevOps modernas, CI/CD y contenedorización Docker. El proyecto está documentado en **español** (con código y nombres técnicos en inglés).

- **Licencia**: LGPL-3.0
- **Python**: 3.10+
- **Base de datos**: PostgreSQL 15+
- **Framework**: Odoo 18.0
- **Contenedorización**: Docker + Docker Compose

---

## 2. Estructura del Proyecto

```
odoo-18/
├── .github/workflows/          # CI/CD con GitHub Actions
│   ├── ci.yml                  # Linting (flake8, black, isort), Docker build, tests
│   └── staging.yml             # Deploy a AWS ECS vía ECR
├── addons/                     # Módulos personalizados de Odoo
│   ├── custom_module/          # Módulo de ESTUDIO (modelo separado)
│   └── project_pro/            # Módulo de PRODUCCIÓN (herencia)
├── config/
│   └── requirements.txt        # Dependencias Python
├── scripts/
│   ├── backup.sh               # Backup de PostgreSQL con pg_dump
│   ├── init-permissions.sh     # Permisos iniciales de BD
│   └── test.sh                 # Ejecutar tests de Odoo
├── docker-compose.yml          # Orquestación: Odoo + PostgreSQL + Adminer
├── Dockerfile                  # Imagen basada en odoo:18.0
├── pyproject.toml              # Config de Pyright, Pylance, Pylint, Ruff
├── .env.example                # Variables de entorno (DB, SMTP, Admin)
├── .gitignore                  # Ignora .env, data/, __pycache__, etc.
├── README.md                   # Documentación principal
├── ARCHITECTURE.md             # Arquitectura del sistema
├── DEPLOYMENT.md               # Guía de despliegue
├── CONTRIBUTING.md             # Guía de contribución
├── SECURITY.md                 # Política de seguridad
├── CODE_OF_CONDUCT.md          # Código de conducta
└── LICENSE                     # LGPL-3.0
```

---

## 3. Módulos de Odoo

### 3.1 `custom_module` — Módulo de Estudio

**Ubicación**: [`addons/custom_module/`](addons/custom_module/)

**Enfoque**: Crea un **modelo separado** (`_name = 'project.task.extended'`) — útil para aprender, pero NO es la práctica recomendada en producción.

**Manifest** ([`__manifest__.py`](addons/custom_module/__manifest__.py)):
- Nombre: "Project Management"
- Dependencias: `base`, `project`
- Incluye: vistas, seguridad, demo data, tests

**Modelos** ([`models/project_task_extended.py`](addons/custom_module/models/project_task_extended.py:8)):
| Modelo | `_name` | Descripción |
|--------|---------|-------------|
| `ProjectTaskExtended` | `project.task.extended` | Tarea extendida con prioridad, horas, deadline, checklist, tags |
| `ProjectTaskChecklist` | `project.task.checklist` | Items de checklist por tarea |
| `ProjectTaskTag` | `project.task.tag` | Etiquetas con color |

**Campos clave de `ProjectTaskExtended`**:
- `task_id` → Many2one a `project.task` (relación con tarea nativa)
- `priority` → Selection (Low/Medium/High/Urgent)
- `estimated_hours`, `actual_hours` → Float
- `remaining_hours` → Computed (`max(0, estimated - actual)`), stored
- `deadline` → Date
- `is_overdue` → Computed Boolean (deadline < hoy y tarea no terminada)
- `checklist_ids` → One2many a `project.task.checklist`
- `progress_percentage` → Computed Float (% items completados)
- `tag_ids` → Many2many a `project.task.tag`

**Vistas** ([`views/`](addons/custom_module/views/)):
- `project_task_views.xml` → Vistas tree y form propias para `project.task.extended`
- `project_menu.xml` → Menú propio "Project Extended" con configuración de tags

**Tests** ([`tests/test_project_task_extended.py`](addons/custom_module/tests/test_project_task_extended.py:6)):
- 11 tests unitarios con `TransactionCase`
- Cubren: creación, cálculo de horas restantes, overdue, progreso, validaciones, tags, checklist toggle

**Seguridad** ([`security/ir.model.access.csv`](addons/custom_module/security/ir.model.access.csv)):
- Usuarios (`base.group_user`): lectura/escritura/creación (sin eliminar)
- Managers (`project.group_project_manager`): acceso completo

---

### 3.2 `project_pro` — Módulo Profesional (Recomendado)

**Ubicación**: [`addons/project_pro/`](addons/project_pro/)

**Enfoque**: Usa **herencia de clase** (`_inherit = 'project.task'`) — la práctica recomendada en Odoo. Extiende el modelo nativo directamente.

**Manifest** ([`__manifest__.py`](addons/project_pro/__manifest__.py)):
- Nombre: "Project Pro"
- Dependencias: `base`, `project`
- Sin demo data ni tests incluidos

**Modelos** ([`models/project_task_pro.py`](addons/project_pro/models/project_task_pro.py:5)):
| Modelo | `_name` | `_inherit` | Descripción |
|--------|---------|------------|-------------|
| `ProjectTaskPro` | `project.task` | `project.task` | Extiende tarea nativa con campos adicionales |
| `ProjectTaskChecklistPro` | `project.task.checklist.pro` | — | Items de checklist |
| `ProjectTaskTagPro` | `project.task.tag.pro` | — | Etiquetas con color |

**Campos añadidos a `project.task`** (misma lógica que custom_module):
- `estimated_hours`, `actual_hours`, `remaining_hours` (computed)
- `deadline`, `is_overdue` (computed)
- `checklist_ids` → One2many a `project.task.checklist.pro`
- `progress_percentage` (computed desde checklist)
- `tag_ids` → Many2many a `project.task.tag.pro` (tabla: `task_tag_pro_rel`)

**Vistas** ([`views/project_task_pro_views.xml`](addons/project_pro/views/project_task_pro_views.xml)):
- **Hereda** la vista form nativa (`project.view_task_form2`) usando `xpath`
- **Hereda** la vista kanban nativa (`project.view_project_task_kanban`)
- Agrega campos de tracking y checklist en las vistas existentes
- Menú de configuración bajo `project.menu_project_config` → "Project Pro" → "Tags Pro"

**Documentación incluida**:
- [`docs/TECHNICAL_DOC.md`](addons/project_pro/docs/TECHNICAL_DOC.md) — Documentación técnica detallada del módulo
- [`docs/USER_MANUAL.md`](addons/project_pro/docs/USER_MANUAL.md) — Manual de usuario con casos de uso

**Seguridad** ([`security/ir.model.access.csv`](addons/project_pro/security/ir.model.access.csv)):
- Solo define acceso para `checklist.pro` y `tag.pro` (el modelo `project.task` ya tiene permisos nativos)

---

## 4. Diferencia Clave entre los Dos Módulos

| Aspecto | `custom_module` | `project_pro` |
|---------|----------------|---------------|
| Patrón | Modelo separado (`_name` nuevo) | Herencia (`_inherit`) |
| Tabla BD | `project_task_extended` (nueva) | `project_task` (existente, extendida) |
| Vistas | Propias (form/tree independientes) | Hereda vistas nativas con `xpath` |
| Integración | Requiere `task_id` Many2one | Se integra directamente |
| Propósito | Aprendizaje | Producción |
| Tests | ✅ Incluidos (11 tests) | ❌ No incluidos |

---

## 5. Infraestructura Docker

### [`docker-compose.yml`](docker-compose.yml)
Tres servicios en red `odoo-network` (bridge):

| Servicio | Imagen | Puerto | Volúmenes |
|----------|--------|--------|-----------|
| `odoo` | `odoo:18.0` | `8069:8069` | `odoo-data`, `./addons → /mnt/extra-addons`, `./config/odoo.conf → /etc/odoo/odoo.conf` |
| `postgres` | `postgres:15` | — (interno) | `postgres-data` |
| `adminer` | `adminer` | `8080:8080` | — |

**Nota**: Las credenciales de PostgreSQL están hardcodeadas en el compose (`odoo/odoo`). El `.env.example` sugiere usar variables pero el compose no las referencia.

### [`Dockerfile`](Dockerfile)
- Base: `odoo:18.0`
- Instala: `git`, `vim`, `libpq-dev`, `black`, `flake8`, `isort`, `pytest`, `psycopg2-binary`
- Copia addons a `/mnt/extra-addons/` y config a `/etc/odoo/`
- Ejecuta como usuario `odoo`

---

## 6. CI/CD (GitHub Actions)

### [`ci.yml`](.github/workflows/ci.yml) — Integración Continua
**Trigger**: Push a `main`, `staging`, `feature/**` y PRs a `main`/`staging`

| Job | Acciones |
|-----|----------|
| `lint` | flake8 (max-line=120), black --check, isort --check-only |
| `docker-build` | Build imagen Docker, hadolint para validar Dockerfile |
| `tests` | Instala requirements.txt, ejecuta pytest en `addons/custom_module/tests/` (con `|| true`) |

### [`staging.yml`](.github/workflows/staging.yml) — Deploy a Staging
**Trigger**: Push a `staging` o manual (`workflow_dispatch`)

| Paso | Acción |
|------|--------|
| 1 | Configura credenciales AWS |
| 2 | Login a Amazon ECR |
| 3 | Build y push imagen Docker a ECR |
| 4 | Deploy a ECS (`aws ecs update-service`) |
| 5 | Smoke test con `curl` |

**Secrets requeridos**: `AWS_ACCESS_KEY_ID`, `AWS_SECRET_ACCESS_KEY`, `AWS_REGION`

---

## 7. Scripts de Utilidad

| Script | Función |
|--------|---------|
| [`scripts/backup.sh`](scripts/backup.sh) | Backup de PostgreSQL con `pg_dump`, limpia backups >7 días |
| [`scripts/test.sh`](scripts/test.sh) | Crea BD de test, ejecuta tests de Odoo con `--test-enable` |
| [`scripts/init-permissions.sh`](scripts/init-permissions.sh) | Configura timezone UTC, grants, extensiones (uuid-ossp, postgis) |

---

## 8. Configuración de Desarrollo

### Variables de Entorno ([`.env.example`](.env.example))
```
DB_HOST, DB_PORT, DB_USER, DB_PASSWORD, DB_NAME
SMTP_SERVER, SMTP_PORT, SMTP_USER, SMTP_PASSWORD, SMTP_SSL
ADMIN_PASSWORD
LONGPOLLING_PORT (opcional)
```

### Herramientas de Calidad de Código ([`pyproject.toml`](pyproject.toml))
- **Pyright/Pylance**: Incluye `addons/`, extraPaths para Odoo
- **Pylint**: Permite extensiones `odoo`, `odoo.addons`
- **Ruff**: Target Python 3.10

### Dependencias Python ([`config/requirements.txt`](config/requirements.txt))
```
psycopg2-binary==2.9.9, python-dotenv==1.0.0
black==23.12.1, flake8==7.0.0, isort==5.13.2, pytest==7.4.4
```

---

## 9. Convenciones del Proyecto

- **Commits**: Semánticos (`feat:`, `fix:`, `docs:`, `refactor:`, `test:`, `chore:`)
- **Branching**: `main` (producción), `staging` (integración), `feature/*` (desarrollo)
- **Python**: PEP 8, clases en PascalCase, métodos/campos en snake_case
- **XML**: Indentación de 4 espacios
- **Idioma**: Documentación en español, código en inglés

---

## 10. Cómo Ejecutar el Proyecto

```bash
# 1. Clonar y configurar
git clone <repo-url> && cd odoo-18
cp .env.example .env  # Editar con valores reales

# 2. Iniciar servicios
docker-compose up -d

# 3. Acceder
# Odoo: http://localhost:8069
# Adminer: http://localhost:8080

# 4. Instalar módulo
# Apps → Buscar "Project Pro" → Instalar

# 5. Ejecutar tests
docker-compose exec odoo odoo -d odoo_test --test-enable --stop-after-init -i project_pro
```

---

## 11. Puntos de Atención para Agentes IA

1. **Módulo principal**: `project_pro` es el módulo de producción. `custom_module` es solo para estudio.
2. **Herencia Odoo**: `project_pro` usa `_inherit = 'project.task'` (extiende el modelo nativo, NO crea uno nuevo).
3. **Vistas XML**: `project_pro` hereda vistas nativas con `xpath`. Cualquier modificación debe respetar los `inherit_id` existentes.
4. **No hay `odoo.conf` en el repo**: Está en `.gitignore`. El `docker-compose.yml` lo monta desde `./config/odoo.conf`.
5. **Tests solo en `custom_module`**: `project_pro` no tiene tests unitarios aún.
6. **Credenciales hardcodeadas en compose**: PostgreSQL usa `odoo/odoo` directamente en el YAML.
7. **CI ejecuta tests con `|| true`**: Los tests no bloquean el pipeline actualmente.
8. **Archivos ignorados por git**: `ODOO18_SKILL.md` y `Plan Optimizado para Portafolio Profesional.md` son documentos personales no versionados.
9. **El Dockerfile instala herramientas de dev** (black, flake8, etc.) — no es ideal para producción.
10. **AWS ECS/ECR**: El deploy a staging está configurado pero requiere infraestructura AWS previa.

---

## 12. Mapa de Archivos Clave por Tarea

| Si necesitas... | Revisa estos archivos |
|-----------------|----------------------|
| Entender el modelo de datos | `addons/project_pro/models/project_task_pro.py` |
| Modificar vistas | `addons/project_pro/views/project_task_pro_views.xml` |
| Agregar permisos | `addons/project_pro/security/ir.model.access.csv` |
| Configurar Docker | `docker-compose.yml`, `Dockerfile` |
| Modificar CI/CD | `.github/workflows/ci.yml`, `.github/workflows/staging.yml` |
| Agregar dependencias Python | `config/requirements.txt` |
| Entender la arquitectura | `ARCHITECTURE.md` |
| Ver cómo se hacen tests | `addons/custom_module/tests/test_project_task_extended.py` |
| Configurar el entorno | `.env.example`, `pyproject.toml` |
| Agregar un nuevo módulo | Crear directorio en `addons/`, seguir estructura de `project_pro` |
