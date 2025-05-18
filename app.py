import sqlite3
from sqlite3 import Error

def crear_conexion():
    """Crea una conexión a la base de datos SQLite"""
    try:
        conn = sqlite3.connect('tienda.db')
        conn.execute("PRAGMA foreign_keys = 1")  # Habilitar claves foráneas
        return conn
    except Error as e:
        print(e)
    return None

def crear_tablas(conn):
    """Crea todas las tablas de la base de datos"""
    tablas = [
        """
        CREATE TABLE IF NOT EXISTS categorias (
            id_categoria INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre_categoria TEXT NOT NULL UNIQUE
        );
        """,
        """
        CREATE TABLE IF NOT EXISTS marcas (
            id_marca INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre_marca TEXT NOT NULL UNIQUE
        );
        """,
        """
        CREATE TABLE IF NOT EXISTS proveedores (
            id_proveedor INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre_proveedor TEXT NOT NULL,
            contacto TEXT NOT NULL
        );
        """,
        """
        CREATE TABLE IF NOT EXISTS clientes (
            id_cliente INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            telefono TEXT UNIQUE
        );
        """,
        """
        CREATE TABLE IF NOT EXISTS productos (
            id_producto INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre_producto TEXT NOT NULL,
            id_categoria INTEGER NOT NULL,
            id_marca INTEGER NOT NULL,
            precio_venta REAL NOT NULL CHECK(precio_venta > 0),
            precio_compra REAL NOT NULL CHECK(precio_compra > 0),
            stock INTEGER NOT NULL CHECK(stock >= 0),
            unidad_medida TEXT NOT NULL CHECK(unidad_medida IN ('unidad', 'kg', 'litro')),
            tamano TEXT,
            especificaciones TEXT,  -- SQLite no tiene tipo JSON nativo, se usa TEXT
            FOREIGN KEY (id_categoria) REFERENCES categorias(id_categoria),
            FOREIGN KEY (id_marca) REFERENCES marcas(id_marca)
        );
        """,
        """
        CREATE TABLE IF NOT EXISTS ventas (
            id_venta INTEGER PRIMARY KEY AUTOINCREMENT,
            fecha_venta DATE NOT NULL DEFAULT (date('now')),
            id_cliente INTEGER,
            FOREIGN KEY (id_cliente) REFERENCES clientes(id_cliente)
        );
        """,
        """
        CREATE TABLE IF NOT EXISTS detalle_ventas (
            id_detalle_venta INTEGER PRIMARY KEY AUTOINCREMENT,
            id_venta INTEGER NOT NULL,
            id_producto INTEGER NOT NULL,
            cantidad INTEGER NOT NULL CHECK(cantidad > 0),
            precio_unitario REAL NOT NULL CHECK(precio_unitario > 0),
            FOREIGN KEY (id_venta) REFERENCES ventas(id_venta),
            FOREIGN KEY (id_producto) REFERENCES productos(id_producto)
        );
        """,
        """
        CREATE TABLE IF NOT EXISTS compras (
            id_compra INTEGER PRIMARY KEY AUTOINCREMENT,
            fecha_compra DATE NOT NULL DEFAULT (date('now')),
            id_proveedor INTEGER NOT NULL,
            FOREIGN KEY (id_proveedor) REFERENCES proveedores(id_proveedor)
        );
        """,
        """
        CREATE TABLE IF NOT EXISTS detalle_compras (
            id_detalle_compra INTEGER PRIMARY KEY AUTOINCREMENT,
            id_compra INTEGER NOT NULL,
            id_producto INTEGER NOT NULL,
            cantidad INTEGER NOT NULL CHECK(cantidad > 0),
            precio_unitario REAL NOT NULL CHECK(precio_unitario > 0),
            FOREIGN KEY (id_compra) REFERENCES compras(id_compra),
            FOREIGN KEY (id_producto) REFERENCES productos(id_producto)
        );
        """
    ]

    try:
        cursor = conn.cursor()
        for tabla in tablas:
            cursor.execute(tabla)
        conn.commit()
    except Error as e:
        print(f"Error al crear tablas: {e}")

def insertar_datos_iniciales(conn):
    """Inserta datos de ejemplo para pruebas"""
    datos = [
        # Categorías
        "INSERT INTO categorias (nombre_categoria) VALUES ('Abarrotes'), ('Papelería');",
        
        # Marcas
        "INSERT INTO marcas (nombre_marca) VALUES ('Gloria'), ('BIC'), ('Faber-Castell');",
        
        # Proveedores
        """INSERT INTO proveedores (nombre_proveedor, contacto) 
           VALUES ('Distribuidora Perú', '999-111111'), 
                  ('Papeles S.A.', '999-222222');""",
                  
        # Clientes
        """INSERT INTO clientes (nombre, telefono) 
           VALUES ('Juan Pérez', '555-123456'), 
                  ('María Gómez', '555-654321');""",
                  
        # Productos (ejemplo con JSON)
        """INSERT INTO productos (
            nombre_producto, id_categoria, id_marca, precio_venta, 
            precio_compra, stock, unidad_medida, tamano, especificaciones
        ) VALUES 
            (
                'Leche Evaporada', 1, 1, 4.5, 3.0, 100, 'unidad', '1L', 
                '{"tipo": "Entera", "empaque": "lata"}'
            ),
            (
                'Cuaderno A4', 2, 2, 12.0, 8.0, 50, 'unidad', '200 hojas', 
                '{"tipo_hoja": "cuadriculada", "color_portada": "azul"}'
            );"""
    ]

    try:
        cursor = conn.cursor()
        for dato in datos:
            cursor.execute(dato)
        conn.commit()
        print("¡Datos iniciales insertados correctamente!")
    except Error as e:
        print(f"Error al insertar datos: {e}")

if __name__ == '__main__':
    conn = crear_conexion()
    if conn:
        crear_tablas(conn)
        insertar_datos_iniciales(conn)  # Opcional: Comenta si no quieres datos de prueba
        conn.close()
        print("Base de datos 'tienda.db' creada exitosamente.")