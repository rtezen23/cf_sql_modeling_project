import streamlit as st
import sqlite3
import pandas as pd
import plotly.express as px

# Configuración de la página
st.set_page_config(
    page_title="Análisis de Ventas - Tienda",
    page_icon="📊",
    layout="wide"
)

def get_db_connection():
    """Establece conexión con la base de datos SQLite."""
    return sqlite3.connect('tienda.db')

def execute_query(query, params=None):
    """Ejecuta una consulta SQL y devuelve los resultados en un DataFrame."""
    conn = get_db_connection()
    try:
        if params:
            df = pd.read_sql_query(query, conn, params=params)
        else:
            df = pd.read_sql_query(query, conn)
        return df
    finally:
        conn.close()

# Título de la aplicación
st.title("📊 Análisis de Ventas - Tienda de Abarrotes y Papelería")
st.markdown("---")

# Crear pestañas para cada consulta
tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
    "Productos más vendidos",
    "Clientes más frecuentes",
    "Categorías más populares",
    "Clientes por categoría",
    "Ventas por mes",
    "Productos por proveedor"
])

# Consulta 1: Productos más vendidos
with tab1:
    st.header("1. Productos más vendidos")
    query = """
    SELECT dv.id_producto, p.nombre_producto, COUNT(*) as ventas
    FROM detalle_ventas dv
    INNER JOIN productos p ON p.id_producto = dv.id_producto
    GROUP BY dv.id_producto
    ORDER BY ventas DESC
    LIMIT 5
    """
    df = execute_query(query)
    
    if not df.empty:
        # Mostrar tabla
        st.dataframe(df, use_container_width=True)
        
        # Mostrar gráfico de barras
        fig = px.bar(df, x='nombre_producto', y='ventas',
                    title='Top 5 Productos Más Vendidos',
                    labels={'nombre_producto': 'Producto', 'ventas': 'N° de Ventas'})
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.warning("No se encontraron datos para mostrar.")

# Consulta 2: Clientes con más compras
with tab2:
    st.header("2. Clientes más frecuentes")
    query = """
    SELECT v.id_cliente, c.nombre, COUNT(*) as total_compras, 
           SUM(dv.precio_unitario * dv.cantidad) as total_gastado
    FROM ventas v
    INNER JOIN detalle_ventas dv ON dv.id_venta = v.id_venta
    INNER JOIN clientes c ON v.id_cliente = c.id_cliente
    WHERE v.id_cliente IS NOT NULL
    GROUP BY v.id_cliente
    ORDER BY total_compras DESC
    LIMIT 3
    """
    df = execute_query(query)
    
    if not df.empty:
        # Mostrar tabla
        st.dataframe(df.style.format({"total_gastado": "S/. {:.2f}"}), use_container_width=True)
        
        # Mostrar gráfico de barras
        fig = px.bar(df, x='nombre', y='total_gastado',
                    title='Clientes con Mayor Gasto Total',
                    labels={'nombre': 'Cliente', 'total_gastado': 'Total Gastado (S/.)'})
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.warning("No se encontraron datos para mostrar.")

# Consulta 3: Categorías más populares
with tab3:
    st.header("3. Categorías más populares")
    query = """
    SELECT ca.id_categoria, ca.nombre_categoria, COUNT(*) as ventas 
    FROM detalle_ventas dv
    INNER JOIN productos p ON dv.id_producto = p.id_producto
    INNER JOIN categorias ca ON p.id_categoria = ca.id_categoria
    GROUP BY ca.id_categoria
    ORDER BY ventas DESC
    LIMIT 5
    """
    df = execute_query(query)
    
    if not df.empty:
        # Mostrar tabla
        st.dataframe(df, use_container_width=True)
        
        # Mostrar gráfico de pastel
        fig = px.pie(df, values='ventas', names='nombre_categoria',
                    title='Distribución de Ventas por Categoría')
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.warning("No se encontraron datos para mostrar.")

# Consulta 4: Clientes por categoría
with tab4:
    st.header("4. Clientes por categoría")
    
    # Primero obtenemos las categorías para el selector
    categorias = execute_query("SELECT id_categoria, nombre_categoria FROM categorias")
    categoria_seleccionada = st.selectbox(
        'Selecciona una categoría:',
        categorias['nombre_categoria'].tolist()
    )
    
    # Obtenemos el ID de la categoría seleccionada
    categoria_id = categorias[categorias['nombre_categoria'] == categoria_seleccionada]['id_categoria'].iloc[0]
    
    # Consulta para obtener los clientes de la categoría seleccionada
    query = """
    SELECT cli.nombre, COUNT(*) as compras, 
           SUM(dv.precio_unitario * dv.cantidad) as total_gastado
    FROM detalle_ventas dv
    INNER JOIN productos p ON dv.id_producto = p.id_producto
    INNER JOIN ventas v ON dv.id_venta = v.id_venta
    INNER JOIN clientes cli ON v.id_cliente = cli.id_cliente
    WHERE p.id_categoria = ?
    GROUP BY cli.nombre
    ORDER BY compras DESC
    LIMIT 5
    """
    df = execute_query(query, (categoria_id,))
    
    if not df.empty:
        st.subheader(f"Clientes en la categoría: {categoria_seleccionada}")
        st.dataframe(df.style.format({"total_gastado": "S/. {:.2f}"}), use_container_width=True)
        
        # Mostrar gráfico de barras
        if len(df) > 0:
            fig = px.bar(df, x='nombre', y='compras',
                       title=f'Clientes con más compras en {categoria_seleccionada}',
                       labels={'nombre': 'Cliente', 'compras': 'N° de Compras'})
            st.plotly_chart(fig, use_container_width=True)
    else:
        st.warning(f"No se encontraron clientes para la categoría {categoria_seleccionada}.")

# Consulta 5: Ventas por mes
with tab5:
    st.header("5. Ventas por mes")
    query = """
    SELECT strftime('%Y-%m', v.fecha_venta) as mes,
           COUNT(DISTINCT v.id_venta) as total_ventas,
           SUM(dv.precio_unitario * dv.cantidad) as monto_total
    FROM ventas v
    INNER JOIN detalle_ventas dv ON v.id_venta = dv.id_venta
    GROUP BY mes
    ORDER BY mes
    """
    df = execute_query(query)
    
    if not df.empty:
        # Mostrar tabla
        st.dataframe(df.style.format({"monto_total": "S/. {:.2f}"}), use_container_width=True)
        
        # Mostrar gráfico de líneas
        fig = px.line(df, x='mes', y='monto_total',
                     title='Evolución de Ventas Mensuales',
                     labels={'mes': 'Mes', 'monto_total': 'Monto Total (S/.)'})
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.warning("No se encontraron datos de ventas por mes.")

# Consulta 6: Productos por proveedor
with tab6:
    st.header("6. Productos por proveedor")
    
    # Primero obtenemos los proveedores para el selector
    proveedores = execute_query("SELECT id_proveedor, nombre FROM proveedores")
    proveedor_seleccionado = st.selectbox(
        'Selecciona un proveedor:',
        proveedores['nombre'].tolist()
    )
    
    # Obtenemos el ID del proveedor seleccionado
    proveedor_id = proveedores[proveedores['nombre'] == proveedor_seleccionado]['id_proveedor'].iloc[0]
    
    # Consulta para obtener los productos del proveedor seleccionado
    query = """
    SELECT p.id_producto, p.nombre_producto, p.precio_venta, 
           COUNT(dv.id_detalle) as veces_vendido,
           SUM(dv.cantidad) as unidades_vendidas,
           SUM(dv.precio_unitario * dv.cantidad) as ingreso_total
    FROM productos p
    LEFT JOIN detalle_ventas dv ON p.id_producto = dv.id_producto
    WHERE p.id_proveedor = ?
    GROUP BY p.id_producto
    ORDER BY veces_vendido DESC
    """
    df = execute_query(query, (proveedor_id,))
    
    if not df.empty:
        st.subheader(f"Productos del proveedor: {proveedor_seleccionado}")
        
        # Formatear la tabla
        df_display = df.copy()
        df_display = df_display.rename(columns={
            'id_producto': 'ID',
            'nombre_producto': 'Producto',
            'precio_venta': 'Precio',
            'veces_vendido': 'Veces Vendido',
            'unidades_vendidas': 'Unidades Vendidas',
            'ingreso_total': 'Ingreso Total'
        })
        
        # Mostrar tabla con formato
        st.dataframe(
            df_display.style.format({
                'Precio': 'S/. {:.2f}',
                'Ingreso Total': 'S/. {:.2f}'
            }),
            use_container_width=True
        )
        
        # Mostrar gráfico de barras
        if len(df) > 0:
            fig = px.bar(df, x='nombre_producto', y='veces_vendido',
                       title=f'Productos más vendidos de {proveedor_seleccionado}',
                       labels={'nombre_producto': 'Producto', 'veces_vendido': 'Veces Vendido'})
            st.plotly_chart(fig, use_container_width=True)
    else:
        st.warning(f"No se encontraron productos para el proveedor {proveedor_seleccionado}.")

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
