from flask import Flask, render_template
from datetime import datetime

app = Flask(__name__)

@app.route('/')
def index():
    # Obtener fecha y hora actual
    fecha_hora = datetime.now().strftime('%d/%m/%Y, %H:%M:%S')
    return render_template('index.html', fecha_hora=fecha_hora)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8081, debug=True)   