# Odoo 18 - Desarrollo Empresarial

[![License: LGPL v3](https://img.shields.io/badge/License-LGPL%20v3-blue.svg)](https://www.gnu.org/licenses/lgpl-3.0)
[![Docker](https://img.shields.io/docker/pulls/odoo/odoo)](https://hub.docker.com/r/odoo/odoo)
[![Python 3.10+](https://img.shields.io/badge/Python-3.10%2B-yellow)](https://www.python.org/)

Entorno de desarrollo profesional para Odoo 18 con módulos personalizados, CI/CD y mejores prácticas DevOps.

## Tabla de Contenidos

- [Resumen](#resumen)
- [Características](#características)
- [Inicio Rápido](#inicio-rápido)
- [Estructura del Proyecto](#estructura-del-proyecto)
- [Módulos](#módulos)
- [Configuración](#configuración)
- [Desarrollo](#desarrollo)
- [Pruebas](#pruebas)
- [CI/CD](#cicd)
- [Contribuir](#contribuir)
- [Licencia](#licencia)

## Resumen

Este proyecto demuestra desarrollo profesional de Odoo con:

- Desarrollo de módulos personalizados (estudio y producción)
- Contenedores con Docker
- CI/CD con GitHub Actions
- Mejores prácticas DevOps

## Características

### Módulos

| Módulo | Descripción | Tipo |
|--------|-------------|------|
| `custom_module` | Módulo de estudio - modelo separado | Demo |
| `project_pro` | Módulo profesional - herencia | Producción |

### Capacidades

- **Seguimiento de Tiempo**: Horas estimadas vs reales
- **Seguimiento de Progreso**: Progreso basado en checklist
- **Gestión de Fechas Límite**: Detección automática de vencimiento
- **Etiquetas Personalizadas**: Categorización de tareas con colores

## Inicio Rápido

### Requisitos Previos

- Docker 20.10+
- Docker Compose 2.0+
- Git

### Instalación

```bash
# 1. Clonar repositorio
git clone https://github.com/tu-usuario/odoo-18.git
cd odoo-18

# 2. Configurar entorno
cp .env.example .env
# Editar .env con tus valores

# 3. Configurar directorio de datos (WSL)
mkdir -p data && chmod -R 777 data

# 4. Iniciar servicios
docker-compose up -d

# 5. Acceder a Odoo
# Web: http://localhost:8069
# Adminer: http://localhost:8080
```

### Primera Configuración

1. Abre http://localhost:8069
2. Crea una nueva base de datos
3. Instala el módulo "Project Pro" desde Apps

## Estructura del Proyecto

```
odoo-18/
├── .github/workflows/       # Pipelines CI/CD
├── .vscode/                 # Configuración VS Code
├── addons/
│   ├── custom_module/      # Módulo de estudio
│   │   ├── models/
│   │   ├── views/
│   │   ├── security/
│   │   ├── tests/
│   │   └── docs/
│   └── project_pro/        # Módulo profesional
│       ├── models/
│       ├── views/
│       ├── security/
│       ├── docs/
│       └── __init__.py
├── config/                  # Archivos de configuración
├── scripts/                 # Utilidades
├── data/                    # Datos de Odoo (gitignore)
├── docker-compose.yml       # Orquestación de contenedores
├── Dockerfile              # Imagen de Odoo
├── pyproject.toml          # Configuración Python
├── LICENSE                 # Licencia LGPL-3
├── CONTRIBUTING.md         # Guía de contribución
├── CODE_OF_CONDUCT.md      # Código de conducta
├── SECURITY.md             # Política de seguridad
├── README.md               # Este archivo
└── ODOO18_SKILL.md        # Lecciones aprendidas Odoo 18
```

## Módulos

### Project Pro (Recomendado)

Módulo profesional usando herencia de clase (`_inherit`):

- Se integra directamente con `project.task` nativo
- Extiende las vistas existentes
- Mejor rendimiento y mantenibilidad

**Instalación**: Apps → Buscar "Project Pro" → Instalar

### Custom Module (Estudio)

Módulo de estudio usando modelo separado (`_name`):

- Crea un modelo independiente
- Requiere vistas propias
- Bueno para aprender

**Instalación**: Apps → Buscar "Gestión de Proyecto" → Instalar

## Configuración

### Variables de Entorno

Crear archivo `.env`:

```bash
# Base de datos
DB_HOST=postgres
DB_PORT=5432
DB_USER=odoo
DB_PASSWORD=tu_contraseña_segura
DB_NAME=odoo

# SMTP
SMTP_SERVER=smtp.ejemplo.com
SMTP_PORT=587
SMTP_USER=tu_email@ejemplo.com
SMTP_PASSWORD=tu_contraseña

# Odoo
ADMIN_PASSWORD=tu_contraseña_admin
```

### Configuración de Odoo

Editar `config/odoo.conf` para configuración personalizada.

## Desarrollo

### Ejecutar Pruebas

```bash
# Con Docker
docker-compose exec odoo odoo -d odoo_test --test-enable --stop-after-init -i project_pro

# Script local
./scripts/test.sh
```

### Ver Logs

```bash
# Todos los servicios
docker-compose logs -f

# Servicio específico
docker-compose logs -f odoo
docker-compose logs -f postgres
```

### Acceso al Shell

```bash
docker-compose exec odoo bash
docker-compose exec postgres psql -U odoo
```

## Pruebas

### Ejecutar Tests

```bash
# Hacer ejecutable el script
chmod +x scripts/test.sh

# Ejecutar pruebas
./scripts/test.sh
```

### Verificación Manual

1. Accede a Odoo
2. Ve a Proyecto → Tareas
3. Crea una nueva tarea
4. Verifica que los campos de Project Pro aparezcan

## CI/CD

### Workflows

| Workflow | Dispara | Descripción |
|----------|---------|-------------|
| CI | Push/PR | Linting, pruebas, build Docker |
| CD | Staging | Desplegar a entorno staging |

### Secrets de GitHub

Configurar en configuración del repositorio:

- `AWS_ACCESS_KEY_ID`
- `AWS_SECRET_ACCESS_KEY`
- `AWS_REGION`
- `DB_PASSWORD`
- `SMTP_PASSWORD`

## Contribuir

¡Las contribuciones son bienvenidas! Por favor lee nuestra [Guía de Contribución](CONTRIBUTING.md).

### Flujo de Desarrollo

1. Haz Fork del repositorio
2. Crea rama de característica: `git checkout -b feature/caracteristica`
3. Commitea cambios: `git commit -m 'feat: agregar caracteristica'`
4. Push: `git push origin feature/caracteristica`
5. Abre Pull Request

### Mensajes de Commit

Usar commits semánticos:

- `feat:` Nueva característica
- `fix:` Corrección de bug
- `docs:` Documentación
- `refactor:` Refactorización
- `test:` Pruebas
- `chore:` Tareas menores

## Documentación

- [Arquitectura](ARCHITECTURE.md) - Arquitectura del sistema
- [Despliegue](DEPLOYMENT.md) - Guía de despliegue
- [Docs Técnicas](addons/project_pro/docs/TECHNICAL_DOC.md) - Documentación técnica del módulo
- [Manual de Usuario](addons/project_pro/docs/USER_MANUAL.md) - Guía para usuarios
- [Odoo 18 Skills](ODOO18_SKILL.md) - Lecciones aprendidas

## Licencia

Este proyecto está licenciado bajo la Licencia GNU Lesser General Public License v3.0 - ver el archivo [LICENSE](LICENSE) para más detalles.

## Soporte

- Issues: GitHub Issues
- Discusiones: GitHub Discussions

---

Hecho con ❤️ para la Comunidad Odoo
