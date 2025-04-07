# Flask API con Integración a Cassandra

Este repositorio contiene una aplicación desarrollada con Flask que interactúa con una base de datos Cassandra para gestionar clientes, pedidos y productos. Se han desarrollado scripts independientes para la inserción y consulta de datos para cada entidad, y se ofrece un Dockerfile para facilitar la contenerización de la aplicación.

## Estructura del Proyecto

- **app.py**: Archivo principal que define los endpoints de la API utilizando Flask.
- **clientes.py**: Funciones para inyectar y consultar datos en la tabla `cliente`.
- **pedidos.py**: Funciones para inyectar y consultar datos en la tabla `pedido`.
- **productos.py**: Funciones para inyectar y consultar datos en la tabla `producto`.
- **Dockerfile**: Archivo de configuración para crear la imagen Docker de la aplicación.
- **requirements.txt**: Lista de dependencias necesarias (por ejemplo, `Flask` y `cassandra-driver`).
- **data/**: Directorio que debe contener los archivos de conexión a Cassandra (como el secure connect bundle y el archivo JSON con credenciales).

## Requisitos

- **Docker**: Para construir y ejecutar el contenedor de la aplicación.
- **Cassandra o Astra DB**: Para la conexión a la base de datos. Asegúrate de tener el keyspace (por ejemplo, `prueba`) y las tablas creadas. Los scripts incluyen funciones para crearlas si no existen.
- **Python 3.8**: Si deseas ejecutar la aplicación de forma local sin Docker.

## Configuración

### Conexión a Cassandra

1. Coloca el bundle seguro (por ejemplo, `secure-connect-test-cassandra.zip`) y el archivo de credenciales (por ejemplo, `test_cassandra-token.json`) en el directorio `data/`.
2. Verifica que el keyspace `prueba` y las tablas (`cliente`, `pedido` y `producto`) estén creados. La aplicación incluye funciones para crearlos si no existen.

### Ejecución Local

1. Instala las dependencias:
   ```bash
   pip install -r requirements.txt
   ```
2. Ejecuta la aplicación:
    ```bash
   python app.py
   ```
### Ejecución con Docker

1. Construye la imagen Docker:
    ```bash
    docker build -t mi-app-flask-cassandra .
    ``` 

2. Ejecuta el contenedor:
    ```bash
    docker run -p 5000:5000 mi-app-flask-cassandra
    ```