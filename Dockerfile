# -----------------------------------------------------------
# ETAPA 1: BUILD (Solo para compilar dependencias pesadas)
# -----------------------------------------------------------
FROM python:3.9-slim AS builder

WORKDIR /app

# Instalar SOLO lo necesario para compilar (ej. cryptography, pandas)
# Si tus deps son puras Python, puedes quitar esta línea.
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copiar solo requirements para aprovechar la caché de Docker
COPY requirements.txt .

# Instalar dependencias sin caché y en una carpeta concreta
RUN pip install --no-cache-dir --prefix=/install -r requirements.txt

# -----------------------------------------------------------
# ETAPA 2: RUNTIME (Imagen final ligera)
# -----------------------------------------------------------
FROM python:3.9-slim

# Variables de entorno para Python (mejoran logs y rendimiento)
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

# Copiar SOLO las dependencias instaladas desde el builder
# Esto excluye gcc, build-essential y archivos temporales
COPY --from=builder /install /usr/local

# Copiar el código de la aplicación
# (Asegúrate de tener un .dockerignore bueno para no copiar basura)
COPY . /app

# Crear usuario no-root (seguridad)
# RUN useradd -u 5678 --disabled-password --gecos "" appuser && chown -R appuser /app
# USER appuser

EXPOSE 80

ENV FLASK_RUN_HOST=0.0.0.0

# Ejecutar la app (usa gunicorn en producción si es posible)
CMD ["python", "src/web.py"]   