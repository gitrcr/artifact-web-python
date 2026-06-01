from flask import Flask, render_template, request
from datetime import datetime

app = Flask(__name__)

@app.route('/')
def index():
    fecha_hora = datetime.utcnow().strftime('%d/%m/%Y, %H:%M:%S UTC')
    ip_cliente = request.headers.get('X-Forwarded-For', request.remote_addr)
    return render_template('index.html', fecha_hora=fecha_hora)

# Only for local development. In production, use a WSGI server like Gunicorn or uWSGI.
#if __name__ == "__main__":
#    app.run(host="0.0.0.0", port=8081, debug=True)