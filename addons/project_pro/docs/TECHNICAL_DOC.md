# Documentación Técnica: ProjectTaskPro

## 1. Visión General

El módulo `project_pro` extiende el modelo nativo `project.task` de Odoo utilizando herencia de clase. Esto permite agregar funcionalidades avanzadas de gestión de proyectos sin crear un modelo paralelo.

### Arquitectura de Herencia

```python
class ProjectTaskPro(models.Model):
    _name = 'project.task'      # Sobrescribe el modelo nativo
    _inherit = 'project.task'   # Hereda todas las propiedades
```

**Concepto clave**: Al usar `_name = 'project.task'` junto con `_inherit = 'project.task'`, estamos extendiendo el modelo nativo en lugar de crear uno nuevo. Todos los campos heredados están disponibles automáticamente.

---

## 2. Clase Principal: ProjectTaskPro

### 2.1 Definición de Campos

#### Campos Simples (Basic Fields)

```python
estimated_hours = fields.Float(string='Estimated Hours')
actual_hours = fields.Float(string='Actual Hours')
deadline = fields.Date(string='Deadline')
```

| Campo | Tipo | Descripción |
|-------|------|-------------|
| `estimated_hours` | Float | Horas estimadas para completar la tarea |
| `actual_hours` | Float | Horas realmente invertidas |
| `deadline` | Date | Fecha límite de entrega |

#### Campos Calculados (Computed Fields)

Los campos calculados se definen con:
- `compute`: función que calcula el valor
- `store=True`: guarda el valor en BD (se recalcula solo cuando cambian las dependencias)
- `depends`: especifica qué campos disparan el recalculo

##### Remaining Hours (Horas Restantes)

```python
remaining_hours = fields.Float(
    string='Remaining Hours',
    compute='_compute_remaining_hours',
    store=True
)

@api.depends('estimated_hours', 'actual_hours')
def _compute_remaining_hours(self):
    for task in self:
        task.remaining_hours = max(0, task.estimated_hours - task.actual_hours)
```

**Lógica**: 
- Calcula: `estimated_hours - actual_hours`
- Usa `max(0, ...)` para evitar valores negativos
- Se recalcula automáticamente cuando cambian horas estimadas o actuales

##### Is Overdue (¿Vencida?)

```python
is_overdue = fields.Boolean(
    string='Is Overdue',
    compute='_compute_is_overdue',
    store=True
)

@api.depends('deadline', 'state')
def _compute_is_overdue(self):
    today = fields.Date.today()
    for task in self:
        task.is_overdue = (
            task.deadline and
            task.deadline < today and
            task.state not in ['done', 'cancelled']
        )
```

**Lógica**:
- Marca como vencida si: tiene deadline Y la fecha es anterior a hoy Y la tarea no está terminada/cancelada
- Estados que evitan marcar como vencido: `done`, `cancelled`

##### Progress Percentage (% de Progreso)

```python
progress_percentage = fields.Float(
    string='Progress %',
    compute='_compute_progress',
    store=True
)

@api.depends('checklist_ids', 'checklist_ids.is_done')
def _compute_progress(self):
    for task in self:
        if not task.checklist_ids:
            task.progress_percentage = 0.0
        else:
            done_count = len(task.checklist_ids.filtered('is_done'))
            total_count = len(task.checklist_ids)
            task.progress_percentage = (done_count / total_count) * 100
```

**Lógica**:
- Si no hay checklist: 0%
- Si hay checklist: `(items_realizados / items_totales) * 100`
- Se actualiza automáticamente al marcar items

#### Campos Relacionales

##### One2many: Checklist

```python
checklist_ids = fields.One2many(
    'project.task.checklist.pro',
    'task_id',
    string='Checklist'
)
```

| Parámetro | Valor | Descripción |
|-----------|-------|-------------|
| comodel_name | `project.task.checklist.pro` | Modelo relacionado |
| inverse_name | `task_id` | Campo que relaciona de vuelta |
| string | `Checklist` | Etiqueta visible |

**Comportamiento**: Una tarea puede tener muchos items de checklist.

##### Many2many: Tags

```python
tag_ids = fields.Many2many(
    'project.task.tag.pro',
    'task_tag_pro_rel',
    'task_id',
    'tag_id',
    string='Tags'
)
```

| Parámetro | Valor | Descripción |
|-----------|-------|-------------|
| comodel_name | `project.task.tag.pro` | Modelo de etiquetas |
| relation | `task_tag_pro_rel` | Tabla intermedia |
| column1 | `task_id` | FK a tarea |
| column2 | `tag_id` | FK a etiqueta |

**Comportamiento**: Una tarea puede tener muchas etiquetas, y una etiqueta puede aplicarse a muchas tareas.

---

## 3. Validaciones (Constraints)

### 3.1 Validación de Horas Negativas

```python
@api.constrains('estimated_hours', 'actual_hours')
def _check_hours(self):
    for task in self:
        if task.estimated_hours < 0:
            raise ValidationError('Estimated hours cannot be negative')
        if task.actual_hours < 0:
            raise ValidationError('Actual hours cannot be negative')
```

**Cuándo se ejecuta**: Al crear o modificar un registro.
**Efecto**: Impide guardar si las horas son negativas.

---

## 4. Métodos Personalizados

### 4.1 action_complete_checklist

```python
def action_complete_checklist(self):
    self.ensure_one()
    for checklist in self.checklist_ids:
        checklist.is_done = True
    return True
```

| Elemento | Descripción |
|----------|-------------|
| `self.ensure_one()` | Garantiza que solo se procesa un registro |
| Itera sobre checklist | Marca todos los items como realizados |
| Retorna `True` | Acción completada exitosamente |

---

## 5. Modelos Auxiliares

### 5.1 ProjectTaskChecklistPro

Modelo para items de checklist.

```python
class ProjectTaskChecklistPro(models.Model):
    _name = 'project.task.checklist.pro'
    _description = 'Task Checklist Pro'
    _order = 'sequence'

    task_id = fields.Many2one(
        'project.task',
        string='Task',
        required=True,
        ondelete='cascade'
    )

    name = fields.Char(string='Description', required=True)
    is_done = fields.Boolean(string='Done', default=False)
    sequence = fields.Integer(string='Sequence', default=10)
```

| Campo | Tipo | Descripción |
|-------|------|-------------|
| `task_id` | Many2one | Tarea padre (relación) |
| `name` | Char | Descripción del item |
| `is_done` | Boolean | ¿Completado? |
| `sequence` | Integer | Orden de visualización |

**Comportamiento especial**: `ondelete='cascade'` - si se elimina la tarea, se eliminan los items.

**Método toggle_done**: Alterna el estado de completado.

### 5.2 ProjectTaskTagPro

Modelo para etiquetas de tareas.

```python
class ProjectTaskTagPro(models.Model):
    _name = 'project.task.tag.pro'
    _description = 'Task Tag Pro'
    _order = 'name'

    name = fields.Char(string='Tag Name', required=True)
    color = fields.Integer(string='Color', default=10)
```

| Campo | Tipo | Descripción |
|-------|------|-------------|
| `name` | Char | Nombre de la etiqueta |
| `color` | Integer | Color de visualización |

---

## 6. Diagrama de Relaciones

```
┌─────────────────────────────┐       ┌─────────────────────────────┐
│      project.task          │       │  project.task.checklist.pro │
│    (Modelo nativo)         │       │                             │
├─────────────────────────────┤       ├─────────────────────────────┤
│ * name                     │       │ * task_id ─────────────┐     │
│ * date_deadline            │       │ * name                 │     │
│ * state                    │       │ * is_done              │     │
│ * ...                      │       │ * sequence             │     │
│                            │       │                       │     │
│ ── Campos Extension ──     │       │                       │     │
│ + estimated_hours          │◄──────┤ 1:N                    │     │
│ + actual_hours             │       │                        │     │
│ + remaining_hours (calc)  │       └────────────────────────┘     │
│ + deadline                 │       
│ + is_overdue (calc)       │       
│ + checklist_ids (1:N)     │       ┌─────────────────────────────┐
│ + progress_percentage     │       │  project.task.tag.pro       │
│ + tag_ids (N:M)           │◄─────►│                             │
└─────────────────────────────┘       ├─────────────────────────────┤
                                     │ * name                     │
                                     │ * color                    │
                                     └─────────────────────────────┘
```

---

## 7. Decoradores y Anotaciones

### 7.1 @api.depends

Indica qué campos deben cambiar para recalcular el campo calculado.

```python
@api.depends('estimated_hours', 'actual_hours')
```

**Equivalente SQL**: El campo se recalcula cuando `estimated_hours` o `actual_hours` cambian en la base de datos.

### 7.2 @api.constrains

Define validaciones que se ejecutan al guardar.

```python
@api.constrains('field1', 'field2')
```

**Diferencia con @depends**:
- `@depends`: Para campos calculados
- `@constrains`: Para validaciones

### 7.3 fields.Float

Para valores numéricos con decimales.

```python
fields.Float(string='Nombre', default=0.0)
```

### 7.4 fields.Date

Para fechas.

```python
fields.Date.today()  # Fecha actual
fields.Date.from_string()  # Convertir string a fecha
```

---

## 8. Mejores Prácticas Aplicadas

| Práctica | Implementación |
|----------|---------------|
| Campos calculados con `store=True` | Mejor rendimiento en BD |
| Nombres de relaciones únicos | `task_tag_pro_rel` |
| Validaciones con mensajes claros | `ValidationError` |
| Código limpio y documentado | Métodos con lógica simple |
| Herencia en lugar de modelo nuevo | Mejor integración |

---

## 9. Flujo de Ejecución

### Crear una tarea con tracking:

1. Usuario crea tarea → Se guarda en `project.task`
2. Usuario define horas estimadas → Se guarda en `estimated_hours`
3. Usuario define deadline → Se guarda en `deadline`
4. **Automático**: Se calcula `remaining_hours` (store=True)
5. **Automático**: Se calcula `is_overdue` si aplica (store=True)
6. Usuario agrega checklist → Se crea registro en `project.task.checklist.pro`
7. **Automático**: Se calcula `progress_percentage` (store=True)

### Marcar item como done:

1. Usuario marca checkbox → `is_done = True`
2. **Automático**: Se recalcula `progress_percentage`

---

## 10. Referencias Externas

- [Documentación oficial Odoo - Campos](https://www.odoo.com/documentation/18.0/developer/reference/backend/orm.html#fields)
- [Odoo ORM API](https://www.odoo.com/documentation/18.0/developer/reference/backend/orm.html)
- [Computed Fields](https://www.odoo.com/documentation/18.0/developer/reference/backend/orm.html#computed-fields)
