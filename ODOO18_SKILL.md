# Odoo 18 - Lecciones Aprendidas y Best Practices

## 1. Configuración del Entorno (WSL2 + Docker)

### Permisos de Datos
**Problema**: Errores `Permission Denied` al escribir en volúmenes Docker
**Solución**: Antes de ejecutar `docker compose up`, crear directorio con permisos:
```bash
mkdir -p data && chmod -R 777 data
```

---

## 2. Modelos y Seguridad

### Regla General
> **SIEMPRE** definir los modelos Python antes de referenciarlos en archivos de seguridad (CSV)

### Estructura de Access.csv
```csv
id,name,model_id:id,group_id:id,perm_read,perm_write,perm_create,perm_unlink
```
- `model_id:id`: Formato `model_nombre_del_modelo` (guiones bajos, sin puntos)
- Los modelos deben existir en Python antes de cargar el CSV

### Nombres de Tablas Many2many
**Problema**: Conflictos con nombres de tablas relacionales existentes
**Solución**: Usar nombres únicos y descriptivos:
```python
# Malo
'task_tag_rel'

# Bueno
'project_task_extended_tag_rel'
```

---

## 3. Vistas XML - Cambios Odoo 17→18

### Nomenclatura de Vistas
| Odoo 17 | Odoo 18 |
|---------|---------|
| `<tree>` | `<list>` |
| `view_mode="tree,form"` | `view_mode="list,form"` |

### Ejemplo Correcto
```xml
<record id="view_task_tree" model="ir.ui.view">
    <field name="name">task.tree</field>
    <field name="model">project.task.extended</field>
    <field name="arch" type="xml">
        <list>
            <field name="name"/>
            <field name="priority"/>
        </list>
    </field>
</record>

<record id="action_task" model="ir.actions.act_window">
    <field name="name">Tasks</field>
    <field name="res_model">project.task.extended</field>
    <field name="view_mode">list,form</field>
</record>
```

---

## 4. Referencias Externas (XMLID)

### Problema Común
Referenciar IDs de otros módulos que no existen o cambiaron:
```xml
<!-- MALO - dependencia externa frágil -->
<field name="action" ref="project.act_project_project_2_task_task"/>
```

### Solución
Definir acciones locales propias:
```xml
<!-- BUENO - acción local -->
<record id="action_my_action" model="ir.actions.act_window">
    <field name="name">My Action</field>
    <field name="res_model">my.model</field>
    <field name="view_mode">list,form</field>
</record>

<field name="action" ref="action_my_action"/>
```

---

## 5. Desarrollo de Módulos

### Estructura de Módulo
```
module_name/
├── __manifest__.py      # Dependencias, datos, configuración
├── __init__.py
├── models/
│   ├── __init__.py
│   └── *.py             # Definiciones de modelos
├── views/
│   └── *.xml            # Vistas, acciones, menús
├── security/
│   └── ir.model.access.csv
├── tests/
│   ├── __init__.py
│   └── test_*.py
└── demo/
    └── demo.xml
```

### Manifest - Dependencias
```python
'depends': ['base', 'project'],
```

### Actualización vs Reinstalación
- **Actualizar**: Después de修改 Python/XML → cukup klik "Actualizar"
- **Reinstalar**: Solo para cambios estructurales en BD

---

## 6. Campos y Computados

### Campos Comunes
```python
# Many2one
task_id = fields.Many2one('project.task', string='Task')

# One2many
checklist_ids = fields.One2many('model.name', 'field_id', string='Checklist')

# Many2many
tag_ids = fields.Many2many(
    'project.task.tag',
    'rel_table_name',
    'left_id',
    'right_id',
    string='Tags'
)

# Computed con depends y store
computed_field = fields.Float(
    compute='_compute_method',
    store=True,
    depends=['field1', 'field2']
)
```

### Validaciones
```python
@api.constrains('field_name')
def _check_constraint(self):
    for record in self:
        if record.field_name < 0:
            raise ValidationError(_('Error message'))
```

---

## 7. Errores Comunes y Soluciones

| Error | Causa | Solución |
|-------|-------|----------|
| `No matching record found for external id` | Modelo no definido en Python | Crear clase Model antes del CSV |
| `Invalid view type: 'tree'` | Sintaxis Odoo 17 | Cambiar a `<list>` |
| `Permission Denied` (Docker) | Permisos de carpeta | `chmod -R 777 data/` |
| `Missing required value for field Model` | CSV referencia modelo inexistente | Verificar model_id:id en CSV |

---

## 8. Debug y Troubleshooting

### Verificar Errores de Módulo
```bash
# Logs de Odoo
docker compose logs -f odoo

# Reiniciar y rebuild
docker compose build
docker compose up -d
```

### Forzar Actualización
Desde UI: Apps → Buscar módulo → Actualizar

---

## 9. Git/GitHub Integration

### Commits Semánticos
```
feat: add new feature
fix: bug fix
docs: documentation
refactor: code refactoring
```

### CI/CD
- Workflows en `.github/workflows/`
- Tests: `pytest` para Python
- Linting: `flake8`

---

## 11. VS Code - Configuración de Linting

### Problema
Pylance no puede resolver importaciones de `odoo`:
```python
from odoo import models, fields, api, _
from odoo.exceptions import ValidationError
```

### Solución
Crear `.vscode/settings.json`:
```json
{
    "python.analysis.extraPaths": [
        "/usr/lib/python3/dist-packages",
        "/mnt/extra-addons"
    ],
    "python.analysis.autoImportCompletions": true
}
```

### Alternativa
Crear `pyproject.toml` en la raíz del proyecto:
```toml
[tool.pyright]
include = ["addons"]
extraPaths = [
    "/usr/lib/python3/dist-packages",
    "/mnt/extra-addons"
]
```

> **Nota**: Los paths dependen del entorno (Docker, WSL, local). Ajustar según sea necesario.

---

## 12. Checklist Antes de Entregar

- [ ] Permisos de carpeta `data/` configurados
- [ ] Modelos Python definidos antes de CSV
- [ ] Vistas usan `<list>` (no `<tree>`)
- [ ] Referencias externas son locales o verificadas
- [ ] Nombres de relaciones Many2many únicos
- [ ] Tests passing
- [ ] Módulo actualiza sin errores

---

## 13. Advertencias de Pylance/VS Code

### Problema
VS Code muestra errores:
```
No se ha podido resolver la importación "odoo"
No se ha podido resolver la importación "odoo.exceptions"
```

### Análisis
El problema es que VS Code busca paquetes en el sistema local, pero Odoo está instalado en el contenedor Docker.

Las siguientes importaciones son **equivalentes**:
```python
# Forma 1 (estándar)
from odoo import models, fields, api, _

# Forma 2 (explícita)
from odoo import models, fields, api
from odoo.exceptions import ValidationError
from odoo.tools.translate import _
```

### Solución
1. **Ignorar las advertencias** - El código funciona correctamente en el contenedor
2. **Configurar extraPaths** en `.vscode/settings.json` (requiere que la ruta exista)
3. **Instalar Odoo localmente** (no recomendado, es complejo)

### Conclusión
> Las advertencias de Pylance son un problema del IDE, no del código. El módulo funciona correctamente en el entorno Docker de Odoo.
