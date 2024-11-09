FROM python:3.8-slim-buster

# Evita que la salida de Python se bufee
ENV PYTHONUNBUFFERED=1

# Establece el directorio de trabajo
WORKDIR /app

# Copia el archivo de dependencias y ejecuta pip
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copia el resto de la aplicación
COPY . .

# Variables de entorno para la configuración de Flask
ENV FLASK_APP=app.py
ENV FLASK_RUN_HOST=0.0.0.0
ENV FLASK_RUN_PORT=5001

# Comando para iniciar la aplicación
CMD ["flask", "run"]
