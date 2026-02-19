# Política de Seguridad

## Versión: 1.0.0

## Informe de Vulnerabilidades

Agradecemos los esfuerzos de los investigadores de seguridad y la comunidad para mejorar la seguridad de este proyecto. Si descubres una vulnerabilidad, por favor repórtala de manera responsable.

## Cómo Reportar

### Para Vulnerabilidades de Seguridad

1. **NO** crees un issue público
2. Envía un correo electrónico a: [tu-email@ejemplo.com]
3. Incluye la siguiente información:
   - Tipo de vulnerabilidad
   - Rutas completas de archivos relacionados
   - Pasos para reproducir el problema
   - Posible impacto
   - Información de contacto (opcional)

## Ámbitos Cubiertos

### Módulos Odoo

- `custom_module`: Módulo de estudio
- `project_pro`: Módulo profesional

### Ámbitos NO Cubiertos

- Configuración del servidor
- Infraestructura de red
- Base de datos (fuera del módulo)
- Issues de terceros

## Tiempo de Respuesta

| Tipo de Reporte | Tiempo de Respuesta |
|-----------------|---------------------|
| Crítico | 24-48 horas |
| Alto | 3-5 días |
| Medio | 1-2 semanas |
| Bajo | Según disponibilidad |

## Actualizaciones de Seguridad

Las actualizaciones de seguridad se publicarán como versiones del módulo y se anunciarán en el repositorio.

## Configuración de Seguridad Recomendada

### Base de Datos

- Usar contraseñas fuertes
- Habilitar SSL/TLS
- Restringir acceso por IP

### Odoo

- Cambiar contraseña de admin por defecto
- Habilitar HTTPS en producción
- Configurar limit_request
- Usar modo de producción

### Docker

- No exponer puertos innecesarios
- Usar imágenes oficiales
- Mantener contenedores actualizados

## Recursos Adicionales

- [Odoo Security Guidelines](https://www.odoo.com/documentation/18.0/administration/install.html)
- [Docker Security Best Practices](https://docs.docker.com/engine/security/)

---

*Gracias por ayudar a mantener este proyecto seguro.*
