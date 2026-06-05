from flask import Flask, render_template, request
from datetime import datetime
import socket
import os
import platform

app = Flask(__name__)

def get_container_info():
    hostname = socket.gethostname()
    try:
        private_ip = socket.gethostbyname(hostname)
    except socket.gaierror:
        private_ip = "unknown"

    return {
        "hostname": hostname,
        "private_ip": private_ip,
        "os_system": platform.system(),
        "os_release": platform.release(),
        "cpu_count": os.cpu_count(),
        "python_version": platform.python_version()
    }

def get_client_ip():    
    headers = ['X-Forwarded-For', 'X-Real-IP', 'CF-Connecting-IP']
    for header in headers:
        if header in request.headers:
            return request.headers[header].split(',')[0].strip()
    return request.remote_addr

@app.route('/')
def index():
    date_time = datetime.now().strftime('%d/%m/%Y, %H:%M:%S')
    
    context = {
        "date_time": date_time,
        "client_ip": get_client_ip(),
        "container": get_container_info()
    }
    
    return render_template('index.html', **context)

if __name__ == '__main__':    
    app.run(host='0.0.0.0', port=80, debug=True)