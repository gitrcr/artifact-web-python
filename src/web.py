from flask import Flask, render_template, request
from datetime import datetime
import socket
import os
import platform

app = Flask(__name__)

def get_container_info():
    """
    Extrae información básica del sistema y del contenedor.
    No requiere permisos especiales ni APIs externas.
    """
    hostname = socket.gethostname()
    
    try:
        # Intenta obtener la IP privada resolviendo el hostname
        private_ip = socket.gethostbyname(hostname)
    except socket.gaierror:
        private_ip = "No disponible"

    return {
        "hostname": hostname,          # Nombre del contenedor (o ID corto)
        "private_ip": private_ip,      # IP interna (ej. 10.x.x.x)
        "os_system": platform.system(), # Linux
        "os_release": platform.release(),
        "cpu_count": os.cpu_count(),   # Número de núcleos asignados
        "python_version": platform.python_version()
    }

def get_client_ip():
    """
    Obtiene la IP del cliente que hace la petición.
    Nota: Si estás detrás de un proxy/NAT, esto mostrará la IP del proxy o interna.
    """
    # Revisa cabeceras comunes por si hay un proxy delante
    headers = ['X-Forwarded-For', 'X-Real-IP', 'CF-Connecting-IP']
    for header in headers:
        if header in request.headers:
            return request.headers[header].split(',')[0].strip()
    return request.remote_addr

@app.route('/')
def index():
    fecha_hora = datetime.now().strftime('%d/%m/%Y, %H:%M:%S')
    
    # Datos para la plantilla
    context = {
        "fecha_hora": fecha_hora,
        "client_ip": get_client_ip(),
        "container": get_container_info()
    }
    
    return render_template('index.html', **context)

if __name__ == '__main__':    
    # debug=True es útil para desarrollo, quítalo en producción real
    app.run(host='0.0.0.0', port=80, debug=True)   