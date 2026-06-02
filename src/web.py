from flask import Flask, render_template, request
from datetime import datetime
import socket
import os


app = Flask(__name__)


from werkzeug.middleware.proxy_fix import ProxyFix
app.wsgi_app = ProxyFix(app.wsgi_app, x_for=1, x_proto=1, x_host=1, x_port=1)

def get_client_ip():
    """
    Obtiene la IP pública del cliente.
    Prioriza X-Forwarded-For si existe,否则 usa remote_addr.
    """
    # request.remote_addr ya está corregido por ProxyFix, pero podemos ser explícitos:
    if request.headers.get('X-Forwarded-For'):
        # X-Forwarded-For puede tener varias IPs: "cliente, proxy1, proxy2"
        # La primera es siempre la del cliente original.
        return request.headers.get('X-Forwarded-For').split(',')[0].strip()
    return request.remote_addr


def get_container_name():
    """
    Obtiene el nombre o ID del contenedor.
    En Docker, el hostname por defecto es el ID corto del contenedor.
    """
    hostname = socket.gethostname()
    # Opcional: Intentar leer el ID largo desde /etc/hostname o variables de entorno si se inyectan
    container_id = os.environ.get('HOSTNAME', hostname)
    return container_id


@app.route('/')
def index():
    # Obtener fecha y hora actual
    fecha_hora = datetime.now().strftime('%d/%m/%Y, %H:%M:%S')
    # Obtener IP del cliente
    ip_cliente = get_client_ip()
    container_name = get_container_name()
    return render_template('index.html', fecha_hora=fecha_hora, ip_cliente=ip_cliente, container_name=container_name)

if __name__ == '__main__':    
    app.run(host='0.0.0.0', port=8081, debug=True)   