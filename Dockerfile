FROM continuumio/miniconda3:latest

WORKDIR /app

# Copiamos el archivo de entorno
COPY environment.yml .

# Creamos el entorno "cassandra" y limpiamos archivos temporales
RUN conda env create -f environment.yml && conda clean -afy

# Copiamos el resto de la aplicación
COPY . .

EXPOSE 5000

# Ejecutamos la aplicación dentro del entorno "cassandra"
CMD ["conda", "run", "-n", "cassandra", "python", "app.py"]

