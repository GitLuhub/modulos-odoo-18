# Guía de Contribución

¡Gracias por tu interés en contribuir a este proyecto! Este documento te guiará a través del proceso de contribución.

## Código de Conducta

Al participar en este proyecto, te comprometes a seguir nuestro [Código de Conducta](CODE_OF_CONDUCT.md).

## ¿Cómo puedo contribuir?

### Reportar Bugs

Si encuentras un bug, por favor:

1. Busca en los issues existentes para ver si ya fue reportado
2. Si no existe, crea un nuevo issue con:
   - Título descriptivo
   - Pasos para reproducir el bug
   - Comportamiento esperado vs actual
   - Capturas de pantalla si es posible
   - Versión de Odoo y módulo

### Sugerir Mejoras

Para sugerir nuevas funcionalidades:

1. Abre un issue con la etiqueta `enhancement`
2. Describe el caso de uso
3. Explica por qué sería útil
4. Incluye ejemplos de uso

### Pull Requests

#### Proceso de Pull Request

1. **Fork** el repositorio
2. Crea una rama desde `develop`:
   ```bash
   git checkout develop
   git pull origin develop
   git checkout -b feature/nombre-funcionalidad
   ```

3. **Desarrolla** tu funcionalidad
   - Sigue las convenciones de código
   - Escribe tests para nuevas funcionalidades
   - Actualiza la documentación si es necesario

4. **Commit** tus cambios usando mensajes semánticos:
   ```bash
   git commit -m "feat: add new feature"
   git commit -m "fix: resolve bug in task tracking"
   git commit -m "docs: update user manual"
   ```

5. **Push** a tu fork:
   ```bash
   git push origin feature/nombre-funcionalidad
   ```

6. Crea un **Pull Request** hacia `develop`

#### Convenciones de Código

- **Python**: Sigue PEP 8
- **Nombrado**:
  - Clases: `PascalCase` (ej. `ProjectTaskPro`)
  - Métodos: `snake_case` (ej. `_compute_remaining_hours`)
  - Campos: `snake_case`
- **Vistas XML**: Usa indentación de 4 espacios
- **Comentarios**: En español o inglés, sé consistente

#### Tipos de Commits

| Tipo | Descripción |
|------|-------------|
| `feat` | Nueva funcionalidad |
| `fix` | Corrección de bug |
| `docs` | Documentación |
| `style` | Formateo, sin cambio de lógica |
| `refactor` | Refactorización |
| `test` | Tests |
| `chore` | Tareas menores |

#### Antes de Enviar el PR

- [ ] Los tests pasan
- [ ] El código sigue las convenciones
- [ ] La documentación está actualizada
- [ ] Los commits son atómicos y descriptivos

## Estructura del Proyecto

```
odoo-18/
├── addons/
│   ├── custom_module/     # Módulo para estudio
│   └── project_pro/      # Módulo profesional
├── config/               # Configuración
├── scripts/              # Utilidades
├── .github/workflows/    # CI/CD
├── docker-compose.yml    # Orquestación
├── Dockerfile
└── README.md
```

## Configuración del Entorno de Desarrollo

### Requisitos

- Docker y Docker Compose
- Python 3.10+
- PostgreSQL 15+

### Instalación Local

```bash
# 1. Clonar el repositorio
git clone https://github.com/tu-usuario/odoo-18.git
cd odoo-18

# 2. Configurar entorno
cp .env.example .env

# 3. Iniciar servicios
docker-compose up -d

# 4. Acceder a Odoo
# http://localhost:8069
```

## Preguntas

Si tienes preguntas, no dudes en abrir un issue con la etiqueta `question`.

---

¡Tu contribución es valiosa!
