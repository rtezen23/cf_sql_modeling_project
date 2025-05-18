import sqlite3
from sqlite3 import Error
from faker import Faker
import random
from datetime import datetime, timedelta

fake = Faker('es_ES')  # Datos en español

def crear_conexion():
    """Crea una conexión a la base de datos SQLite"""
    try:
        conn = sqlite3.connect('tienda.db')
        conn.execute("PRAGMA foreign_keys = 1")
        return conn
    except Error as e:
        print(e)
    return None

def poblar_tablas(conn):
    """Poblar todas las tablas con datos realistas"""
    cursor = conn.cursor()

    # --- 1. Poblar categorías ---
    categorias = [
        ('Abarrotes',),
        ('Papelería',),
        ('Limpieza',)
    ]
    cursor.executemany("INSERT INTO categorias (nombre_categoria) VALUES (?)", categorias)

    # --- 2. Poblar marcas ---
    marcas = [
        ('Gloria',), ('Nestlé',), ('Coca-Cola',), ('Bimbo',),
        ('BIC',), ('Faber-Castell',), ('Norma',), ('Sapolio',)
    ]
    cursor.executemany("INSERT INTO marcas (nombre_marca) VALUES (?)", marcas)

    # --- 3. Poblar proveedores ---
    proveedores = [
        ('Distribuidora Perú', '999-111111'),
        ('Suministros Papelería', '999-222222'),
        ('Limpieza Total S.A.', '999-333333'),
        ('Alimentos Andinos', '999-444444'),
        ('Bebidas del Sur', '999-555555')
    ]
    cursor.executemany("INSERT INTO proveedores (nombre_proveedor, contacto) VALUES (?,?)", proveedores)

    # --- 4. Poblar clientes (30 clientes) ---
    clientes = []
    for _ in range(30):
        nombre = fake.name()
        telefono = fake.phone_number()[:15]
        clientes.append((nombre, telefono))
    cursor.executemany("INSERT INTO clientes (nombre, telefono) VALUES (?,?)", clientes)

    # --- 5. Poblar productos (20 productos) ---
    productos_data = [
        # Abarrotes (id_categoria=1)
        ('Arroz Costeño', 1, 1, 5.0, 3.5, 0, 'kg', '5 kg', '{"tipo": "Extra", "empaque": "saco"}'),
        ('Aceite Primor', 1, 4, 12.0, 8.0, 0, 'litro', '1 litro', '{"tipo": "Vegetal", "origen": "soya"}'),
        ('Leche Evaporada', 1, 1, 4.5, 3.0, 0, 'unidad', '1L', '{"tipo": "Entera", "empaque": "lata"}'),
        ('Galletas Soda Field', 1, 4, 3.0, 2.0, 0, 'unidad', 'Paquete 200g', '{"sabor": "Original", "unidades": 12}'),
        
        # Papelería (id_categoria=2)
        ('Cuaderno Norma A4', 2, 7, 15.0, 10.0, 0, 'unidad', '100 hojas', '{"tipo_hoja": "cuadriculada", "color": "azul"}'),
        ('Lápices Faber-Castell', 2, 6, 2.5, 1.5, 0, 'unidad', 'Pack x12', '{"mina": "HB", "colores": "mixtos"}'),
        ('Borradores Norma', 2, 7, 1.0, 0.5, 0, 'unidad', 'Pack x5', '{"forma": "rectangular", "color": "blanco"}'),
        ('Resaltadores BIC', 2, 5, 8.0, 5.0, 0, 'unidad', 'Pack x4', '{"colores": "amarillo, rosa, verde, azul"}'),
        
        # Limpieza (id_categoria=3)
        ('Detergente Sapolio', 3, 8, 10.0, 7.0, 0, 'unidad', '1 kg', '{"aroma": "limón", "presentación": "polvo"}'),
        ('Escoba Industrial', 3, 8, 25.0, 18.0, 0, 'unidad', '1.5 m', '{"material": "plástico", "uso": "interior"}')
    ]
    cursor.executemany(
        """INSERT INTO productos (nombre_producto, id_categoria, id_marca, precio_venta, precio_compra, 
        stock, unidad_medida, tamano, especificaciones) VALUES (?,?,?,?,?,?,?,?,?)""",
        productos_data
    )

    # --- 6. Poblar compras (20 compras) ---
    for _ in range(20):
        id_proveedor = random.randint(1, 5)
        fecha_compra = fake.date_between(start_date='-1y', end_date='today')
        cursor.execute(
            "INSERT INTO compras (fecha_compra, id_proveedor) VALUES (?,?)",
            (fecha_compra, id_proveedor)
        )
        id_compra = cursor.lastrowid

        # Detalle de compra (1-5 productos por compra)
        for _ in range(random.randint(1, 5)):
            id_producto = random.randint(1, 10)
            cantidad = random.randint(10, 100)
            precio_unitario = cursor.execute(
                "SELECT precio_compra FROM productos WHERE id_producto = ?", (id_producto,)
            ).fetchone()[0]
            cursor.execute(
                """INSERT INTO detalle_compras (id_compra, id_producto, cantidad, precio_unitario) 
                VALUES (?,?,?,?)""",
                (id_compra, id_producto, cantidad, precio_unitario)
            )
            # Actualizar stock (simulación)
            cursor.execute(
                "UPDATE productos SET stock = stock + ? WHERE id_producto = ?",
                (cantidad, id_producto)
            )

    # --- 7. Poblar ventas (100 ventas) ---
    for _ in range(100):
        id_cliente = random.randint(1, 30) if random.random() > 0.3 else None  # 30% ventas sin cliente
        fecha_venta = fake.date_between(start_date='-6mo', end_date='today')
        cursor.execute(
            "INSERT INTO ventas (fecha_venta, id_cliente) VALUES (?,?)",
            (fecha_venta, id_cliente)
        )
        id_venta = cursor.lastrowid

        # Detalle de venta (1-5 productos por venta)
        for _ in range(random.randint(1, 5)):
            id_producto = random.randint(1, 10)
            cantidad = random.randint(1, 5)
            precio_unitario = cursor.execute(
                "SELECT precio_venta FROM productos WHERE id_producto = ?", (id_producto,)
            ).fetchone()[0]
            
            # Verificar stock
            stock_actual = cursor.execute(
                "SELECT stock FROM productos WHERE id_producto = ?", (id_producto,)
            ).fetchone()[0]
            
            if stock_actual >= cantidad:
                cursor.execute(
                    """INSERT INTO detalle_ventas (id_venta, id_producto, cantidad, precio_unitario) 
                    VALUES (?,?,?,?)""",
                    (id_venta, id_producto, cantidad, precio_unitario)
                )
                # Actualizar stock
                cursor.execute(
                    "UPDATE productos SET stock = stock - ? WHERE id_producto = ?",
                    (cantidad, id_producto)
                )
            else:
                continue  # Saltar producto sin stock

    conn.commit()
    print("¡Base de datos poblada con éxito!")

if __name__ == '__main__':
    conn = crear_conexion()
    if conn:
        poblar_tablas(conn)
        conn.close()
        print("""
        ¡Listo! La base de datos 'tienda.db' ahora tiene:
        - 3 categorías
        - 8 marcas
        - 5 proveedores
        - 30 clientes
        - 10 productos
        - 20 compras con detalles
        - 100 ventas con detalles (y stock actualizado)
        """)