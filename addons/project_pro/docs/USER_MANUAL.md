# Manual de Usuario: Project Pro

## 1. Introducción

**Project Pro** es un módulo que extiende las funcionalidades del módulo Project nativo de Odoo. Agrega herramientas avanzadas de gestión de proyectos para un seguimiento más preciso del trabajo.

### ¿Qué hace este módulo?

- **Seguimiento de tiempo**: Horas estimadas vs. horas reales
- **Gestión de vencimiento**: Alertas automáticas de tareas vencidas
- **Progreso por checklist**: Seguimiento visual del avance
- **Etiquetas personalizadas**: Organización flexible de tareas

---

## 2. Instalación

### Pasos para instalar

1. Accede a Odoo
2. Ve a **Apps**
3. Busca "Project Pro"
4. Haz clic en **Instalar**

![Instalación](https://via.placeholder.com/800x400?text=Instalar+Project+Pro)

---

## 3. Configuración Inicial

### 3.1 Crear Etiquetas Personalizadas

Antes de usar las etiquetas, créealas:

1. Ve a **Proyecto → Configuración → Project Pro → Tags Pro**
2. Crea nuevas etiquetas con:
   - **Nombre**: Ej. "Urgente", "Bug", "Feature"
   - **Color**: Selecciona un color (1-10)

![Crear etiquetas](https://via.placeholder.com/800x300?text=Crear+Etiquetas)

---

## 4. Uso Diario

### 4.1 Crear una Tarea con Seguimiento

1. Ve a **Proyecto → Tareas**
2. Crea una nueva tarea
3. Rellena los campos de Project Pro:

| Campo | Descripción | Ejemplo |
|-------|-------------|---------|
| **Estimated Hours** | Horas que planeas dedicar | 8 |
| **Actual Hours** | Horas dedicadas | 3 |
| **Deadline** | Fecha límite | 25/02/2026 |
| **Tags** | Etiquetas de categorización | Urgente |

**Nota**: El campo "Remaining Hours" se calcula automáticamente.

![Formulario de tarea](https://via.placeholder.com/800x500?text=Formulario+de+Tarea)

---

## 5. Funcionalidades Detalladas

### 5.1 Seguimiento de Tiempo

#### Campo: Estimated Hours (Horas Estimadas)
Indica cuántas horas planeas dedicar a la tarea.

**Ejemplo**:
- Estimas que la tarea tarda 8 horas
- Escribes: `8`

#### Campo: Actual Hours (Horas Reales)
Registra las horas que has trabajado realmente.

**Ejemplo**:
- Has trabajado 3 horas hoy
- Actualizas: `3`

#### Campo: Remaining Hours (Horas Restantes)
**Se calcula automáticamente**: `Estimated - Actual`

| Estimated | Actual | Remaining |
|-----------|--------|-----------|
| 8 | 3 | 5 |
| 8 | 8 | 0 |
| 8 | 10 | 0 |

> **Consejo**: Mantén actualizadas las horas reales para ver el progreso.

---

### 5.2 Gestión de Vencimientos

#### Campo: Deadline (Fecha Límite)
Establece una fecha límite para la tarea.

#### Campo: Is Overdue (¿Vencida?)
**Se calcula automáticamente**. La tarea se marca como vencida cuando:

- ✓ Tiene fecha límite
- ✓ La fecha ya pasó
- ✓ No está terminada o cancelada

**Ejemplo visual**:

| Estado | Deadline | Hoy | Is Overdue |
|--------|----------|-----|------------|
| En progreso | 15/02/2026 | 18/02/2026 | ✓ Sí |
| En progreso | 20/02/2026 | 18/02/2026 | ✗ No |
| Done | 15/02/2026 | 18/02/2026 | ✗ No |

---

### 5.3 Checklist de Progreso

El checklist te permite desglosar tareas grandes en pasos pequeños.

#### Agregar Items al Checklist

1. Abre una tarea
2. En la sección **Checklist**, agrega items:
   - "Investigar requisitos"
   - "Desarrollar código"
   - "Hacer pruebas"
   - "Documentar"

#### Marcar como Completado

Haz clic en el checkbox de cada item:
- ☐ = Pendiente
- ☑ = Completado

#### Ver Progreso Automático

El campo **Progress %** muestra el avance:

| Items | Completados | Progreso |
|-------|------------|----------|
| 4 | 0 | 0% |
| 4 | 1 | 25% |
| 4 | 2 | 50% |
| 4 | 4 | 100% |

#### Completar Todo el Checklist

Para marcar todos los items de una vez:
1. Busca el botón **"Mark All Complete"** en la tarea
2. Clic → Todos los items se marcan como hechos

---

### 5.4 Etiquetado de Tareas

Las etiquetas permiten categorizar y filtrar tareas.

#### Asignar Etiquetas

1. En el formulario de tarea, busca el campo **Tags**
2. Selecciona una o más etiquetas
3. Las etiquetas aparecen como badges coloreados

#### Usos Prácticos

| Etiqueta | Uso |
|----------|-----|
| 🔴 Urgente | Tareas que requieren atención inmediata |
| 🔵 Bug | Problemas a resolver |
| 🟢 Feature | Nuevas funcionalidades |
| 🟡 Revisión | Tareas pendientes de revisión |
| ⚪ Documentación | Tareas de documentación |

---

## 6. Vistas Disponibles

### 6.1 Vista Kanban

En la vista Kanban verás el progreso como barra:

```
┌─────────────┬─────────────┬─────────────┐
│  TO DO      │  IN PROGRESS│  DONE       │
├─────────────┼─────────────┼─────────────┤
│ ┌─────────┐ │ ┌─────────┐ │ ┌─────────┐ │
│ │Task A   │ │ │Task B   │ │ │Task C   │ │
│ │▓▓▓▓░░░░ │ │ │▓▓▓▓▓▓▓▓ │ │ │░░░░░░░░░ │ │
│ │ 25%     │ │ │ 100%    │ │ │ 0%      │ │
│ └─────────┘ │ └─────────┘ │ └─────────┘ │
└─────────────┴─────────────┴─────────────┘
```

### 6.2 Vista Lista

Muestra todos los campos de seguimiento:

| Tarea | Estimated | Actual | Remaining | Deadline | Progress |
|-------|-----------|--------|-----------|----------|----------|
| Task A | 8h | 3h | 5h | 25/02 | 25% |
| Task B | 4h | 4h | 0h | 20/02 | 100% |

---

## 7. Casos de Uso

### Caso 1: Seguimiento de Proyecto

**Escenario**: Estás desarrollando un sistema nuevo.

**Paso a paso**:
1. Crea un proyecto "Desarrollo Sistema"
2. Para cada tarea grande, crea sub-tareas
3. Estima las horas en cada sub-tarea
4. Registra las horas reales diariamente
5. Observa el progreso en la barra de %

**Resultado**: Sabes exactamente cuánto falta y si vas atrasado.

---

### Caso 2: Gestión de Bugs

**Escenario**: Tienes muchos bugs reportados.

**Paso a paso**:
1. Crea etiquetas: "Bug", "Urgente", "Baja Prioridad"
2. Etiqueta cada bug según urgencia
3. Establece deadline para cada uno
4. Usa el checklist: "Reproducir", "Diagnosticar", "Corregir", "Probar"

**Resultado**: Bugs priorizados y con seguimiento claro.

---

### Caso 3: Revisión de Código

**Escenario**: Necesitas revisar tareas de tu equipo.

**Paso a paso**:
1. Crea etiqueta "Revisión"
2. Cuando asignas una tarea, agrega la etiqueta
3. El responsable agrega checklist: "Revisar código", "Probar", "Aprobar"

**Resultado**: Visibilidad del estado de revisión.

---

## 8. Consejos y Mejores Prácticas

### ✓ Haz

- **Actualiza las horas reales** al final de cada día
- **Usa checklists** para tareas complejas
- **Establece deadlines realistas**
- **Usa etiquetas** para filtrar y buscar

### ✗ No Haz

- No dejes "Actual Hours" en 0 si has trabajado
- No ignores las alertas de overdue
- No crees checklists de un solo item (no tiene sentido)

---

## 9. Preguntas Frecuentes

### ¿Por qué "Remaining Hours" muestra 0 aunque estimé más?

**R**: El cálculo es `estimated - actual`. Si llegaste a cero, ¡ya terminaste las horas estimadas! Considera incrementar las horas estimadas si falta trabajo.

### ¿Puedo usar el módulo sin el checklist?

**R**: Sí, el checklist es opcional. Puedes usar solo el seguimiento de horas.

### ¿Las etiquetas se comparten entre proyectos?

**R**: Sí, las etiquetas son globales. Se pueden usar en cualquier proyecto.

### ¿Qué pasa si elimino una tarea con checklist?

**R**: Se eliminan automáticamente todos los items del checklist (CASCADE).

---

## 10. Glosario

| Término | Definición |
|---------|------------|
| **Estimated Hours** | Horas planificadas para la tarea |
| **Actual Hours** | Horas realmente trabajadas |
| **Remaining Hours** | Horas que faltan (calculado) |
| **Deadline** | Fecha límite de la tarea |
| **Is Overdue** | Indicador de tarea vencida |
| **Checklist** | Lista de items para completar |
| **Progress %** | Porcentaje de avance (calculado) |
| **Tags** | Etiquetas para categorización |

---

## 11. Soporte

Si tienes problemas:

1. **Consulta la documentación técnica**: `/addons/project_pro/docs/TECHNICAL_DOC.md`
2. **Verifica los logs**: `docker compose logs -f odoo`
3. **Actualiza el módulo**: Apps → Project Pro → Actualizar

---

*Documento generado para Odoo 18 - Módulo Project Pro v1.0.0*
