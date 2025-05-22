-- Primero desactivamos las restricciones de clave foránea
PRAGMA foreign_keys = OFF;

-- Truncamos las tablas en orden (primero las tablas hijo)
DELETE FROM detalle_ventas;
DELETE FROM detalle_compras;
DELETE FROM ventas;
DELETE FROM compras;
DELETE FROM productos;
DELETE FROM categorias;
DELETE FROM marcas;
DELETE FROM proveedores;
DELETE FROM clientes;

-- Reseteamos los contadores autoincrement
DELETE FROM sqlite_sequence;

-- Reactivamos las restricciones de clave foránea
PRAGMA foreign_keys = ON; 


PRAGMA table_info(detalle_ventas);

.tables

.schema detalle_ventas

SELECT 
    m.name AS tabla,
    p.name AS columna,
    p.type AS tipo
FROM 
    sqlite_master m
JOIN 
    pragma_table_info(m.name) p
WHERE 
    m.type = 'table'
ORDER BY 
    m.name, p.cid;
