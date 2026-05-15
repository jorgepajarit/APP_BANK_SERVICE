# Dockerfile para el Frontend (Flask)
FROM python:3.11-slim

WORKDIR /app

# Copiamos los requerimientos desde el contexto de construcción (raíz)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiamos el código del frontend
COPY App/flask_app/ .

# Configuración por defecto de la URL de la API (sobrescribible por docker-compose)
ENV API_BASE_URL="http://banco_fastapi:8000"
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

EXPOSE 5000

CMD ["python", "app.py"]
