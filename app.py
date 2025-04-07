import os
import json
import uuid
from datetime import datetime, timedelta
from flask import Flask, request, jsonify
from cassandra.cluster import Cluster
from cassandra.auth import PlainTextAuthProvider

app = Flask(__name__)

# Variables globales para la conexión
cluster = None
session = None

def get_connection():
    cloud_config = {
        'secure_connect_bundle': 'data/secure-connect-test-cassandra.zip'
    }
    
    with open("data/test_cassandra-token.json") as f:
        se = json.load(f)
    
    CLIENT_ID = se["clientId"]
    CLIENT_SECRET = se["secret"]
    
    auth_provider = PlainTextAuthProvider(CLIENT_ID, CLIENT_SECRET)
    cluster = Cluster(cloud=cloud_config, auth_provider=auth_provider)
    session = cluster.connect()
    return cluster, session

def create_tables(session, cluster):
    session.set_keyspace('test')

    # Tabla de clientes
    session.execute("""
    CREATE TABLE IF NOT EXISTS clientes (
        cliente_id UUID PRIMARY KEY,
        nombre TEXT,
        apellido TEXT,
        email TEXT,
        telefono TEXT,
        direccion TEXT
    )
    """)

    # Tabla de pedidos por cliente
    session.execute("""
    CREATE TABLE IF NOT EXISTS pedidos_por_cliente (
        cliente_id uuid,
        pedido_id uuid,
        fecha timestamp,
        total decimal,
        estado text,
        PRIMARY KEY (cliente_id, pedido_id)
    ) WITH CLUSTERING ORDER BY (pedido_id DESC);
    """)

    # Tabla de pedidos por fecha
    session.execute("""
    CREATE TABLE IF NOT EXISTS pedidos_por_fecha (
        fecha date,
        pedido_id uuid,
        cliente_id uuid,
        total decimal,
        estado text,
        PRIMARY KEY (fecha, pedido_id)
    ) WITH CLUSTERING ORDER BY (pedido_id DESC);
    """)

    # Tabla de productos por pedido
    session.execute("""
    CREATE TABLE IF NOT EXISTS productos_por_pedido (
        pedido_id uuid,
        producto_id uuid,
        nombre_producto text,
        cantidad int,
        precio_unitario decimal,
        PRIMARY KEY (pedido_id, producto_id)
    );
    """)

def set_data():
    num_clientes = 5
    num_pedidos_por_cliente = 3
    num_productos_por_pedido = 2

    clientes = []
    pedidos = []

    query_cliente = """
        INSERT INTO clientes (cliente_id, nombre, apellido, email, telefono, direccion)
        VALUES (%s, %s, %s, %s, %s, %s)
    """
    for i in range(num_clientes):
        cliente_id = uuid.uuid4()
        clientes.append(cliente_id)
        nombre = f'Nombre{i}'
        apellido = f'Apellido{i}'
        email = f'cliente{i}@example.com'
        telefono = f'555-00{i}'
        direccion = f'Calle {i} # {100 + i}'
        session.execute(query_cliente, (
            cliente_id,
            nombre,
            apellido,
            email,
            telefono,
            direccion
        ))

    query_pedido_cliente = """
        INSERT INTO pedidos_por_cliente (cliente_id, pedido_id, fecha, total, estado)
        VALUES (%s, %s, %s, %s, %s)
    """
    query_pedido_fecha = """
        INSERT INTO pedidos_por_fecha (fecha, pedido_id, cliente_id, total, estado)
        VALUES (%s, %s, %s, %s, %s)
    """
    for cliente_id in clientes:
        for j in range(num_pedidos_por_cliente):
            pedido_id = uuid.uuid4()
            fecha_pedido = datetime.now() - timedelta(days=j % 5)
            total = round(50.0 + 10.0 * j, 2)
            estado = 'completado'

            session.execute(query_pedido_cliente, (
                cliente_id,
                pedido_id,
                fecha_pedido,
                total,
                estado
            ))
            
            session.execute(query_pedido_fecha, (
                fecha_pedido.date(),
                pedido_id,
                cliente_id,
                total,
                estado
            ))
            
            pedidos.append((cliente_id, pedido_id, fecha_pedido))

    query_producto = """
        INSERT INTO productos_por_pedido (pedido_id, producto_id, nombre_producto, cantidad, precio_unitario)
        VALUES (%s, %s, %s, %s, %s)
    """
    for cliente_id, pedido_id, fecha in pedidos:
        for k in range(num_productos_por_pedido):
            producto_id = uuid.uuid4()
            nombre_producto = f'Producto_{k}'
            cantidad = k + 1
            precio_unitario = round(19.99 + k * 5.0, 2)
            session.execute(query_producto, (
                pedido_id,
                producto_id,
                nombre_producto,
                cantidad,
                precio_unitario
            ))
            
def obtener_datos(tabla):
    try:
        rows = session.execute(f"SELECT * FROM {tabla}")
        resultados = [str(row) for row in rows]
        return "<br>".join(resultados) if resultados else "No hay datos disponibles."
    except Exception as e:
        return f"Error al consultar la tabla {tabla}: {str(e)}"


@app.route("/")
def index():
    return "<h1>Bienvenido a la API de Cassandra</h1><p>Usa /clientes, /pedidos_por_cliente, /pedidos_por_fecha o /productos_por_pedido para ver los datos.</p>"


@app.route("/clientes")
def mostrar_clientes():
    return obtener_datos("clientes")


@app.route("/pedidos_por_cliente")
def mostrar_pedidos_por_cliente():
    return obtener_datos("pedidos_por_cliente")


@app.route("/pedidos_por_fecha")
def mostrar_pedidos_por_fecha():
    return obtener_datos("pedidos_por_fecha")


@app.route("/productos_por_pedido")
def mostrar_productos_por_pedido():
    return obtener_datos("productos_por_pedido")

if __name__ == '__main__':
    cluster, session = get_connection()
    create_tables(session, cluster)
    set_data()
    app.run(debug=True)
