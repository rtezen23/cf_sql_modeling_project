---
trigger: always_on
---

Estas son las consideraciones para este proyecto:

* Es un proyecto personal para hacer un frontend sencillo a la base de datos sqlite que tengo
* La base de datos se llama tienda.db y contiene tablas relacionadas a un negocio pequeño de venta al por menor de abarrotes y papelería en Perú
* La opción más sencilla creo que sería usar streamlit con python, ya que solo quiero mostrar el resultado de consultas sql en una tabla o visualizaciones similares, y añadir algún texto explicativo de mi análisis en cada sql
* Usa venv para crear el entorno virtual y añade el requirements.txt de las librerías actuales

Estas son las tablas, columnas y tipos de datos de la base de datos tienda.db:

| Tabla            | Columna             | Tipo      |
|------------------|---------------------|-----------|
| categorias       | id_categoria        | INTEGER   |
| categorias       | nombre_categoria    | TEXT      |
| clientes         | id_cliente          | INTEGER   |
| clientes         | nombre              | TEXT      |
| clientes         | telefono            | TEXT      |
| compras          | id_compra           | INTEGER   |
| compras          | fecha_compra        | DATE      |
| compras          | id_proveedor        | INTEGER   |
| detalle_compras  | id_detalle_compra   | INTEGER   |
| detalle_compras  | id_compra           | INTEGER   |
| detalle_compras  | id_producto         | INTEGER   |
| detalle_compras  | cantidad            | INTEGER   |
| detalle_compras  | precio_unitario     | REAL      |
| detalle_ventas   | id_detalle_venta    | INTEGER   |
| detalle_ventas   | id_venta            | INTEGER   |
| detalle_ventas   | id_producto         | INTEGER   |
| detalle_ventas   | cantidad            | INTEGER   |
| detalle_ventas   | precio_unitario     | REAL      |
| marcas           | id_marca            | INTEGER   |
| marcas           | nombre_marca        | TEXT      |
| productos        | id_producto         | INTEGER   |
| productos        | nombre_producto     | TEXT      |
| productos        | id_categoria        | INTEGER   |
| productos        | id_marca            | INTEGER   |
| productos        | precio_venta        | REAL      |
| productos        | precio_compra       | REAL      |
| productos        | stock               | INTEGER   |
| productos        | unidad_medida       | TEXT      |
| productos        | tamano              | TEXT      |
| productos        | especificaciones    | TEXT      |
| proveedores      | id_proveedor        | INTEGER   |
| proveedores      | nombre_proveedor    | TEXT      |
| proveedores      | contacto            | TEXT      |
| ventas           | id_venta            | INTEGER   |
| ventas           | fecha_venta         | DATE      |
| ventas           | id_cliente          | INTEGER   |
