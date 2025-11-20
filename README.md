# Nakel Picking - Consolidated Batch Report

## Descripción

Este módulo para Odoo 18 modifica la impresión de lotes de transferencias (stock.picking.batch) para consolidar las cantidades de productos, agrupándolas de manera inteligente.

## Características

- **Consolidación Detallada**: Agrupa productos por:
  - Producto
  - Lote/Número de Serie
  - Paquete origen y destino
  - Ubicación origen
  - Ubicación destino

- **Resumen Simplificado**: Vista alternativa que consolida solo por producto

- **Compatible con**:
  - Seguimiento por lotes
  - Paquetes
  - Olas (waves)
  - Preparación de múltiples órdenes
  - Picking multi ubicación

## Instalación

1. Copia este módulo en tu directorio de addons de Odoo
2. Actualiza la lista de aplicaciones
3. Busca "Nakel Picking - Consolidated Batch Report"
4. Instala el módulo

## Uso

Una vez instalado el módulo, tendrás disponibles dos nuevos reportes en los lotes de transferencias:

### 1. Batch Transfer Consolidated (Reporte Detallado)

Este reporte muestra:
- Información del lote (nombre, responsable, estado, fecha)
- Lista de transferencias incluidas en el lote
- Tabla consolidada con columnas:
  - Producto (código y nombre)
  - Lote/Serial
  - Paquete (origen → destino)
  - Ubicación origen
  - Ubicación destino
  - Cantidad consolidada
  - Unidad de medida
  - Transferencias fuente
- Resumen por producto (totales generales)

### 2. Batch Transfer Summary (Resumen Simplificado)

Este reporte muestra solo:
- Información básica del lote
- Tabla simple con:
  - Código del producto
  - Nombre del producto
  - Cantidad total consolidada
  - Unidad de medida

## Cómo acceder a los reportes

1. Ve a **Inventario > Operaciones > Lotes/Olas**
2. Abre un lote de transferencias
3. Haz clic en el botón **Imprimir**
4. Selecciona:
   - "Batch Transfer Consolidated" para el reporte detallado
   - "Batch Transfer Summary" para el resumen simple

## Ejemplo de uso

**Escenario**: Tienes un lote con 3 transferencias que incluyen:
- Picking 1: Producto A (10 unidades) en Lote L001, de WH/Stock → WH/Output
- Picking 2: Producto A (5 unidades) en Lote L001, de WH/Stock → WH/Output
- Picking 3: Producto A (8 unidades) en Lote L002, de WH/Stock → WH/Output

**Reporte Consolidado** mostrará:
- Producto A | Lote L001 | - | WH/Stock | WH/Output | **15.00** | Unidades | Picking 1, Picking 2
- Producto A | Lote L002 | - | WH/Stock | WH/Output | **8.00** | Unidades | Picking 3

**Resumen Simple** mostrará:
- Producto A | **23.00** | Unidades

## Estructura técnica

```
nakel_picking/
├── __init__.py
├── __manifest__.py
├── models/
│   ├── __init__.py
│   └── stock_picking_batch.py
└── reports/
    └── stock_picking_batch_report.xml
```

### Métodos principales

**`_get_consolidated_lines()`**: Consolida líneas agrupando por producto, lote, paquete y ubicaciones.

**`_get_consolidated_lines_by_product()`**: Consolida solo por producto (para resumen simple).

## Licencia

LGPL-3

## Autor

Nakel

## Versión

18.0.1.0.0
