import streamlit as st
import sqlite3
import pandas as pd
import os

# Obtener la ruta absoluta del directorio donde se encuentra este script
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
# Construir la ruta al archivo de la base de datos
DB_PATH = os.path.join(BASE_DIR, "tienda.db")

# Configuración de la página
st.set_page_config(
    page_title="Examen SQL - Tienda",
    page_icon="📊",
    layout="wide"
)

def get_db_connection():
    """Establece conexión con la base de datos SQLite."""
    st.write(f"Intentando conectar a: {DB_PATH}") # Para depuración
    
    if not os.path.exists(DB_PATH):
        st.error(f"¡ERROR CRÍTICO! El archivo de base de datos NO se encuentra en: {DB_PATH}")
        # Lista los archivos en el directorio base para ver qué hay realmente allí
        try:
            st.info(f"Contenido del directorio '{BASE_DIR}': {os.listdir(BASE_DIR)}")
        except Exception as list_err:
            st.warning(f"No se pudo listar el contenido del directorio {BASE_DIR}: {list_err}")
        return None
    else:
        # Muestra el tamaño del archivo para asegurarte de que no es un archivo vacío.
        file_size = os.path.getsize(DB_PATH)
        st.success(f"Archivo de base de datos ENCONTRADO en: {DB_PATH} (Tamaño: {file_size} bytes)")
        if file_size == 0:
            st.warning("Advertencia: El archivo de base de datos tiene un tamaño de 0 bytes. ¿Está vacío?")

    try:
        # -- CAMBIO IMPORTANTE AQUÍ --
        # Conectar usando formato URI para especificar modo de solo lectura (ro)
        # Esto es crucial para entornos de solo lectura como Render.
        conn_uri = f"file:{DB_PATH}?mode=ro"
        # Alternativa (aún más estricta si estás 100% seguro de que el archivo no cambiará):
        # conn_uri = f"file:{DB_PATH}?immutable=1"
        
        conn = sqlite3.connect(conn_uri, uri=True)
        
        # Verificar si la conexión es válida y si la tabla específica existe
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='detalle_ventas';")
        table_exists = cursor.fetchone()
        
        if table_exists:
            st.success("Conexión exitosa a SQLite y la tabla 'detalle_ventas' FUE encontrada.")
        else:
            st.error("Conexión exitosa a SQLite, PERO la tabla 'detalle_ventas' NO FUE encontrada.")
            # Listar todas las tablas encontradas para ayudar a depurar
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
            all_tables = cursor.fetchall()
            st.info(f"Tablas encontradas en la base de datos: {all_tables}")
            if not all_tables:
                st.warning("La base de datos parece estar vacía (no se encontraron tablas).")

        return conn
    except sqlite3.Error as e:
        st.error(f"Error de SQLite al conectar o verificar la tabla: {e}")
        return None
    except Exception as e: # Captura otros posibles errores en la conexión
        st.error(f"Error inesperado durante la configuración de la conexión: {e}")
        return None

def execute_query(query, params=None):
    """Ejecuta una consulta SQL y devuelve los resultados en un DataFrame."""
    conn = get_db_connection()
    if conn is None:
        return pd.DataFrame()  # Retorna un DataFrame vacío si no hay conexión
        
    try:
        if params:
            df = pd.read_sql_query(query, conn, params=params)
        else:
            df = pd.read_sql_query(query, conn)
        return df
    except sqlite3.Error as e:
        st.error(f"Error al ejecutar la consulta: {e}")
        st.code(query)  # Muestra la consulta que falló
        return pd.DataFrame()  # Retorna un DataFrame vacío en caso de error
    finally:
        if conn:
            conn.close()

# Título de la aplicación
st.title("📊 Análisis de Ventas - Tienda de Abarrotes y Papelería")
st.markdown("---")

# Crear pestañas para cada pregunta del examen
tab1, tab2, tab3, tab4, tab5, tab6, tab7 = st.tabs([
    "1. Productos más vendidos",
    "2. Clientes más frecuentes",
    "3. Categoría más popular",
    "4. Cliente estrella por categoría",
    "5. Proveedores más utilizados",
    "6. Categorías más rentables",
    "7. Mayor compra en cantidad"
])

# Pregunta 1: Productos más vendidos
with tab1:
    st.header("1. ¿Cuáles son los productos más vendidos?")
    
    # Mostrar la consulta SQL
    sql_query = """
    SELECT dv.id_producto, p.nombre_producto, count(*) as 'n° ventas'
    FROM detalle_ventas dv
    INNER JOIN productos p ON p.id_producto = dv.id_producto
    GROUP BY dv.id_producto
    ORDER BY 3 DESC
    LIMIT 5
    """
    
    with st.expander("🔍 Ver consulta SQL"):
        st.code(sql_query, language="sql")
    
    # Ejecutar y mostrar resultados
    df = execute_query(sql_query)
    if not df.empty:
        st.dataframe(df, use_container_width=True)
    else:
        st.warning("No se encontraron datos para mostrar.")

# Pregunta 2: Clientes más frecuentes
with tab2:
    st.header("2. ¿Qué clientes han realizado más compras y cuánto han gastado en total?")
    
    # Mostrar la consulta SQL
    sql_query = """
    SELECT v.id_cliente, c.nombre, count(*) as 'total_compras', 
           SUM(dv.precio_unitario * dv.cantidad) as total_gastado
    FROM ventas v
    INNER JOIN detalle_ventas dv ON dv.id_venta = v.id_venta
    INNER JOIN clientes c ON v.id_cliente = c.id_cliente
    GROUP BY v.id_cliente
    HAVING v.id_cliente IS NOT NULL
    ORDER BY total_compras DESC
    LIMIT 3
    """
    
    with st.expander("🔍 Ver consulta SQL"):
        st.code(sql_query, language="sql")
    
    # Ejecutar y mostrar resultados
    df = execute_query(sql_query)
    if not df.empty:
        st.dataframe(df.style.format({"total_gastado": "S/. {:.2f}"}), use_container_width=True)
    else:
        st.warning("No se encontraron datos para mostrar.")

# Pregunta 3: Categoría más popular
with tab3:
    st.header("3. ¿Cuál es la categoría más popular en ventas?")
    
    # Mostrar la consulta SQL
    sql_query = """
    SELECT ca.id_categoria, ca.nombre_categoria, count(*) as 'n° ventas' 
    FROM detalle_ventas dv
    INNER JOIN productos p ON dv.id_producto = p.id_producto
    INNER JOIN categorias ca ON p.id_categoria = ca.id_categoria
    GROUP BY ca.id_categoria
    ORDER BY 3 DESC
    LIMIT 1
    """
    
    with st.expander("🔍 Ver consulta SQL"):
        st.code(sql_query, language="sql")
    
    # Ejecutar y mostrar resultados
    df = execute_query(sql_query)
    if not df.empty:
        st.dataframe(df, use_container_width=True)
    else:
        st.warning("No se encontraron datos para mostrar.")

# Pregunta 4: Cliente estrella por categoría
with tab4:
    st.header("4. ¿Qué cliente ha realizado más compras de la categoría más popular?")
    
    # Mostrar la consulta SQL
    sql_query = """
    SELECT cli.nombre, cat.nombre_categoria, COUNT(*) as 'n° ventas' 
    FROM detalle_ventas dv
    INNER JOIN productos p ON dv.id_producto = p.id_producto
    INNER JOIN categorias cat ON p.id_categoria = cat.id_categoria
    INNER JOIN ventas v on dv.id_venta = v.id_venta
    INNER JOIN clientes cli ON v.id_cliente = cli.id_cliente
    GROUP BY cli.nombre, cat.nombre_categoria
    HAVING cat.nombre_categoria = ( 
        SELECT nombre_categoria FROM (
            SELECT ca.id_categoria, ca.nombre_categoria, count(*) as ventas 
            FROM detalle_ventas dv
            INNER JOIN productos p ON dv.id_producto = p.id_producto
            INNER JOIN categorias ca ON p.id_categoria = ca.id_categoria
            GROUP BY ca.id_categoria
            ORDER BY 3 DESC
            LIMIT 1
        )
    )
    ORDER BY 3 DESC
    LIMIT 1
    """
    
    with st.expander("🔍 Ver consulta SQL"):
        st.code(sql_query, language="sql")
    
    # Ejecutar y mostrar resultados
    df = execute_query(sql_query)
    if not df.empty:
        st.dataframe(df, use_container_width=True)
    else:
        st.warning("No se encontraron datos para mostrar.")

# Pregunta 5: Proveedores más utilizados
with tab5:
    st.header("5. ¿Qué proveedores han sido más utilizados y cuántas compras se han realizado a cada uno?")
    
    # Mostrar la consulta SQL
    sql_query = """
    SELECT prov.nombre_proveedor, COUNT(*) as 'n° compras'
    FROM detalle_compras dc
    INNER JOIN compras c ON dc.id_compra = c.id_compra
    INNER JOIN proveedores prov ON c.id_proveedor = prov.id_proveedor
    GROUP BY prov.nombre_proveedor
    ORDER BY 2 DESC
    """
    
    with st.expander("🔍 Ver consulta SQL"):
        st.code(sql_query, language="sql")
    
    # Ejecutar y mostrar resultados
    df = execute_query(sql_query)
    if not df.empty:
        st.dataframe(df, use_container_width=True)
    else:
        st.warning("No se encontraron datos para mostrar.")

# Pregunta 6: Categorías más rentables
with tab6:
    st.header("6. ¿Qué categorías de productos generan más ingresos en ventas?")
    
    # Mostrar la consulta SQL
    sql_query = """
    SELECT ca.id_categoria, ca.nombre_categoria, count(*) as 'n° ventas', 
           SUM(dv.cantidad * dv.precio_unitario) as 'total_venta' 
    FROM detalle_ventas dv
    INNER JOIN productos p ON dv.id_producto = p.id_producto
    INNER JOIN categorias ca ON p.id_categoria = ca.id_categoria
    GROUP BY ca.id_categoria
    ORDER BY 4 DESC
    """
    
    with st.expander("🔍 Ver consulta SQL"):
        st.code(sql_query, language="sql")
    
    # Ejecutar y mostrar resultados
    df = execute_query(sql_query)
    if not df.empty:
        st.dataframe(df.style.format({"total_venta": "S/. {:.2f}"}), use_container_width=True)
    else:
        st.warning("No se encontraron datos para mostrar.")

# Pregunta 7: Mayor compra en cantidad
with tab7:
    st.header("7. ¿Cuál ha sido la compra con la mayor cantidad de productos?")
    
    # Mostrar la consulta SQL
    sql_query = """
    SELECT dv.id_venta, cli.nombre, SUM(dv.cantidad) as 'productos_vendidos' 
    FROM detalle_ventas dv
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
    """
    
    with st.expander("🔍 Ver consulta SQL"):
        st.code(sql_query, language="sql")
    
    # Ejecutar y mostrar resultados
    df = execute_query(sql_query)
    if not df.empty:
        st.dataframe(df, use_container_width=True)
    else:
        st.warning("No se encontraron datos para mostrar.")

# Información adicional en la barra lateral
with st.sidebar:
    st.title("ℹ️ Información")
    st.markdown("""
    ### Análisis de Ventas
    
    Esta aplicación muestra análisis detallados de las ventas de la tienda de abarrotes y papelería.
    
    **Características:**
    - Productos más vendidos
    - Clientes más frecuentes
    - Análisis por categorías
    - Evolución de ventas
    - Análisis por proveedor
    
    *Selecciona una pestaña para ver los diferentes informes.*
    """)
    
    # Mostrar estadísticas rápidas
    try:
        total_ventas = execute_query("SELECT COUNT(*) as total FROM ventas")['total'].iloc[0]
        total_clientes = execute_query("SELECT COUNT(DISTINCT id_cliente) as total FROM ventas WHERE id_cliente IS NOT NULL")['total'].iloc[0]
        
        st.markdown("---")
        st.metric("Total de Ventas", f"{total_ventas:,}")
        st.metric("Clientes Únicos", f"{total_clientes:,}")
    except:
        pass
