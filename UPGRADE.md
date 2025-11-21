# Instrucciones de Actualización del Módulo

## ⚠️ IMPORTANTE: El módulo fue modificado

El módulo ahora **reemplaza automáticamente** el reporte estándar de lotes en lugar de crear reportes adicionales.

## Pasos para actualizar el módulo

### Opción 1: Actualización desde la interfaz de Odoo (Recomendado)

1. **Activar modo desarrollador** (si no está activado):
   - Ve a **Ajustes**
   - Al final de la página, haz clic en **Activar el modo de desarrollador**

2. **Actualizar lista de aplicaciones**:
   - Ve a **Aplicaciones**
   - Haz clic en el menú de hamburguesa (☰) en la esquina superior izquierda
   - Selecciona **Actualizar lista de aplicaciones**
   - Confirma la actualización

3. **Actualizar el módulo**:
   - Ve a **Aplicaciones**
   - Elimina el filtro "Aplicaciones" de la barra de búsqueda
   - Busca "Nakel Picking"
   - Haz clic en el botón **Actualizar** (si ya estaba instalado)
   - O haz clic en **Instalar** (si es la primera vez)

4. **Verificar la actualización**:
   - Ve a **Inventario > Operaciones > Lotes/Olas**
   - Abre cualquier lote existente
   - Haz clic en **Imprimir**
   - El reporte consolidado debería generarse automáticamente

### Opción 2: Actualización desde línea de comandos

```bash
# Si Odoo está corriendo, reinicia con actualización del módulo
odoo-bin -u nakel_picking -d nombre_de_tu_base_de_datos

# O si usas docker
docker-compose restart
docker-compose exec odoo odoo -u nakel_picking -d nombre_de_tu_base_de_datos --stop-after-init
```

### Opción 3: Actualización manual (si las anteriores fallan)

1. Desinstala el módulo:
   - Ve a **Aplicaciones**
   - Busca "Nakel Picking"
   - Haz clic en **Desinstalar**

2. Reinicia el servidor de Odoo

3. Vuelve a instalar el módulo:
   - Ve a **Aplicaciones**
   - Haz clic en **Actualizar lista de aplicaciones**
   - Busca "Nakel Picking"
   - Haz clic en **Instalar**

## Verificación del funcionamiento

Después de la actualización, verifica que:

1. ✅ Al imprimir un lote, el reporte muestra:
   - Primera página con la lista de traslados y códigos de barras
   - Siguientes páginas con productos consolidados agrupados por ruta

2. ✅ Los productos duplicados se consolidan en una sola línea

3. ✅ Las cantidades se suman correctamente

## Resolución de problemas

### El reporte sigue mostrando productos duplicados

**Causa**: El módulo no se actualizó correctamente.

**Solución**:
```bash
# Limpia la caché y actualiza el módulo
odoo-bin -u nakel_picking -d tu_base_de_datos --stop-after-init

# Si usas docker
docker-compose restart
```

### El reporte da error al generarse

**Causa**: Puede haber un error en la sintaxis del template.

**Solución**:
1. Revisa los logs de Odoo:
   ```bash
   # Si usas docker
   docker-compose logs -f odoo

   # Si corres Odoo directamente
   tail -f /var/log/odoo/odoo-server.log
   ```

2. Busca errores relacionados con `nakel_picking` o `stock_picking_batch`

3. Si encuentras un error, repórtalo con el mensaje completo del log

### El módulo no aparece en la lista de aplicaciones

**Causa**: La ruta del módulo no está en el `addons_path` de Odoo.

**Solución**:
1. Verifica la configuración de Odoo:
   ```bash
   # En el archivo de configuración de Odoo (odoo.conf)
   addons_path = /ruta/a/addons,/ruta/a/nakel_picking
   ```

2. Reinicia Odoo

3. Actualiza la lista de aplicaciones

## Contacto y Soporte

Si tienes problemas con la actualización, proporciona:
- Versión de Odoo
- Mensaje de error completo (si aplica)
- Logs de Odoo al momento del error
