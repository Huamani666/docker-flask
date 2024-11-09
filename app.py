from flask import Flask, send_file, jsonify
import paramiko
import os

app = Flask(__name__)

# Detalles de la conexión SSH
hostname = 'ssh-natureza.alwaysdata.net'  # Dirección IP o dominio del servidor
port = 22  # Puerto SSH por defecto
username = 'natureza_anon'
password = '(123456)'  # Preferiblemente usa autenticación con clave SSH en lugar de contraseña

# Ruta del archivo remoto en el servidor
ruta_remota = 'Huamani.xlsx'  # El archivo que subiste previamente

# Ruta local dentro de Replit (guardamos el archivo en el directorio actual)
ruta_local = 'Huamani.xlsx'


# Función para descargar el archivo desde el servidor remoto
def descargar_archivo():
    ssh = None  # Inicializamos la variable ssh fuera del bloque try para evitar el error de "unbound"

    try:
        # Crear una instancia SSHClient
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(
            paramiko.AutoAddPolicy())  # Permitir claves desconocidas

        # Conectarse al servidor remoto
        ssh.connect(hostname, port=port, username=username, password=password)
        print("Conexión exitosa.")

        # Usar SFTP para transferir el archivo desde el servidor remoto a la máquina local
        sftp = ssh.open_sftp()
        print(f"Descargando el archivo desde: {ruta_remota} a {ruta_local}...")

        # Descargar el archivo remoto a la ruta local
        sftp.get(ruta_remota, ruta_local)
        sftp.close()

        print(f'Archivo descargado con éxito a {ruta_local}')
        return ruta_local  # Devolver la ruta local del archivo descargado

    except Exception as e:
        print(f'Error al conectar o descargar el archivo: {e}')
        return None  # Devolver None si ocurre un error

    finally:
        # Asegurarse de cerrar la conexión SSH, incluso si ocurre un error
        if ssh:
            ssh.close()


# Ruta para descargar el archivo desde el servidor SSH a través de Flask
@app.route('/', methods=['GET'])
def download_file():
    # Descargar el archivo desde el servidor remoto
    ruta_local = descargar_archivo()

    if ruta_local:
        # Si el archivo fue descargado con éxito, lo enviamos al navegador
        return send_file(
            ruta_local,  # Ruta local del archivo descargado
            as_attachment=True,  # Esto forzará la descarga
            download_name=
            'Hectorarchivo.xlsx',  # Nombre del archivo descargado en el navegador
            mimetype=
            'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        )
    else:
        # Si hubo un error en la descarga, devolvemos un mensaje de error
        return jsonify({"error":
                        "Hubo un problema al descargar el archivo."}), 500


if __name__ == '__main__':
    # Ejecutar la aplicación Flask
    app.run(debug=True) 
