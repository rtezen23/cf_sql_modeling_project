1. ¿Cuáles son los productos más vendidos?

```sql
select dv.id_producto, p.nombre_producto, count(*) 'n° ventas'
from detalle_ventas dv
INNER JOIN productos p
ON p.id_producto = dv.id_producto
GROUP BY dv.id_producto
ORDER BY 3 DESC
LIMIT 5
```

2. ¿Qué clientes han realizado más compras y cuánto han gastado en total?

```sql
select v.id_cliente, c.nombre, count(*) 'total_compras', SUM(dv.precio_unitario * dv.cantidad) total_gastado
from ventas v
INNER JOIN detalle_ventas dv on dv.id_venta = v.id_venta
INNER JOIN clientes c on v.id_cliente = c.id_cliente
GROUP BY v.id_cliente
HAVING v.id_cliente IS NOT NULL
ORDER BY total_compras DESC
LIMIT 3
```

3. ¿Cuál es la categoría más popular en ventas?

```sql
SELECT ca.id_categoria, ca.nombre_categoria, count(*) 'n° ventas' FROM detalle_ventas dv
INNER JOIN productos p ON dv.id_producto = p.id_producto
INNER JOIN categorias ca ON p.id_categoria = ca.id_categoria
GROUP BY ca.id_categoria
ORDER BY 3 DESC
LIMIT 1
```

4. ¿Qué cliente ha realizado más compras de la categoría más popular?

```sql
SELECT cli.nombre, cat.nombre_categoria, COUNT(*) 'n° ventas' 
FROM detalle_ventas dv
INNER JOIN productos p ON dv.id_producto = p.id_producto
INNER JOIN categorias cat ON p.id_categoria = cat.id_categoria
INNER JOIN ventas v on dv.id_venta = v.id_venta
INNER JOIN clientes cli ON v.id_cliente = cli.id_cliente
GROUP BY cli.nombre, cat.nombre_categoria
HAVING cat.nombre_categoria = ( SELECT nombre_categoria FROM
(
  SELECT ca.id_categoria, ca.nombre_categoria, count(*) 'n° ventas' FROM detalle_ventas dv
  INNER JOIN productos p ON dv.id_producto = p.id_producto
  INNER JOIN categorias ca ON p.id_categoria = ca.id_categoria
  GROUP BY ca.id_categoria
  ORDER BY 3 DESC
  LIMIT 1
))
ORDER BY 3 desc
LIMIT 1
```

5. ¿Qué proveedores han sido más utilizados y cuántas compras se han realizado a cada uno?

```sql
SELECT prov.nombre_proveedor, COUNT(*) FROM detalle_compras dc
INNER JOIN compras c ON dc.id_compra = c.id_compra
INNER JOIN proveedores prov ON c.id_proveedor = prov.id_proveedor
GROUP BY prov.nombre_proveedor
ORDER BY 2 DESC
```

6. ¿Qué categorías de productos generan más ingresos en ventas?

```sql
SELECT ca.id_categoria, ca.nombre_categoria, count(*) 'n° ventas', SUM(dv.cantidad * dv.precio_unitario) 'total_venta' FROM detalle_ventas dv
INNER JOIN productos p ON dv.id_producto = p.id_producto
INNER JOIN categorias ca ON p.id_categoria = ca.id_categoria
GROUP BY ca.id_categoria
ORDER BY 4 DESC
```

7. ¿Cuál ha sido la compra con la mayor cantidad de productos?

```sql
SELECT dv.id_venta, cli.nombre, SUM(dv.cantidad) 'productos_vendidos' FROM detalle_ventas dv
INNER JOIN ventas v on dv.id_venta = v.id_venta
INNER JOIN clientes cli ON v.id_cliente = cli.id_cliente
GROUP BY dv.id_venta
HAVING SUM(dv.cantidad) = (
 SELECT MAX(p_vendidos.productos_vendidos) FROM (
   SELECT dv.id_venta, cli.nombre, SUM(dv.cantidad) as 'productos_vendidos'
   	FROM detalle_ventas dv
    INNER JOIN ventas v on dv.id_venta = v.id_venta
    INNER JOIN clientes cli ON v.id_cliente = cli.id_cliente
    GROUP BY dv.id_venta
   ) as p_vendidos
)
```