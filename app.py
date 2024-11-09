from flask import Flask, send_file, jsonify
import pandas as pd
import paramiko
import os

app = Flask(__name__)

# Ruta para generar y descargar el archivo Excel
@app.route('/')
def crear_excel():
    # Datos de ejemplo
    data = {
        "Nombre": ["Ana", "Juan", "Carlos"],
        "Edad": [28, 34, 29],
        "Ciudad": ["Lima", "Cusco", "Arequipa"]
    }

    # Crear DataFrame a partir de los datos
    df = pd.DataFrame(data)

    # Guardar el DataFrame en un archivo Excel
    archivo_excel = "Huamani.xlsx"
    df.to_excel(archivo_excel, index=False)

    print("Archivo Excel creado con éxito.")

    # Retornar el archivo al cliente para descarga
    return send_file(archivo_excel, as_attachment=True)

# Ruta para subir el archivo al servidor SSH
@app.route('/subir_a_ssh', methods=['GET'])
def subir_a_ssh():
    # Datos de conexión - reemplaza estos valores o usa variables de entorno para mayor seguridad
    hostname = 'ssh-natureza.alwaysdata.net' 
    port = 22
    username = 'natureza_anon'
    password = '(123456)'

    # Rutas de archivo
    archivo_local = 'archivo.xlsx'  # Asegúrate de que el archivo exista
    archivo_remoto = '/Huamani.xlsx'

    try:
        # Conectar al servidor SSH
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(hostname, port=port, username=username, password=password)

        # Subir el archivo usando SFTP
        sftp = ssh.open_sftp()
        sftp.put(archivo_local, archivo_remoto)
        sftp.close()

        # Cerrar la conexión
        ssh.close()

        print("Archivo subido con éxito al servidor.")
        return jsonify({"mensaje": "Archivo subido con éxito al servidor."})

    except Exception as e:
        print(f"Error al subir el archivo: {e}")
        return jsonify({"error": str(e)}), 500

@app.route('/')
def index():
    return 'Hello from Flask'

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
