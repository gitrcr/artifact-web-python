FROM python:3.9-slim AS builder

WORKDIR /app

# Instalar herramientas SOLO para compilar dependencias
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .

# Instalar dependencias en un directorio aislado
RUN pip install --upgrade pip \
    && pip install --no-cache-dir --prefix=/install -r requirements.txt

COPY . /app


# -----------------------------
# Etapa 2: runtime DISTROLESS
# -----------------------------
FROM gcr.io/distroless/python3-debian12

WORKDIR /app

# Copiar dependencias ya compiladas
COPY --from=builder /install /usr/local

# Copiar solo el código
COPY --from=builder /src /app

# Distroless no tiene useradd → usar usuario por defecto no-root
USER nonroot

EXPOSE 8081

CMD ["gunicorn", "--bind", "0.0.0.0:8081", "src.web:app"]
