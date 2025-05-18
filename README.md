# Proyecto de Modelado SQL - Tienda de Abarrotes y Papelería

Este proyecto contiene el código y la base de datos para un sistema de gestión de una tienda de abarrotes y papelería en Perú.

## Estructura del Proyecto

- `app.py`: Aplicación principal con consultas SQL
- `add_records.py`: Script para agregar registros de ejemplo
- `truncate_tables.sql`: Script SQL para limpiar las tablas
- `tienda.db`: Base de datos SQLite

## Requisitos

- Python 3.8+
- SQLite3
- Librerías listadas en `requirements.txt`

## Instalación

1. Clona el repositorio
2. Crea un entorno virtual:
   ```
   python -m venv venv
   source venv/bin/activate  # En Windows: venv\Scripts\activate
   ```
3. Instala las dependencias:
   ```
   pip install -r requirements.txt
   ```

## Uso

Para ejecutar la aplicación:
```
python app.py
```

## Estructura de la Base de Datos

La base de datos contiene tablas para gestionar:
- Productos
- Categorías
- Proveedores
- Clientes
- Ventas
- Detalles de venta

## Licencia

MIT
