# Dockerfile para el Backend (FastAPI)
FROM python:3.11-slim

WORKDIR /app

# Copiamos los requerimientos desde el contexto de construcción (raíz)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiamos el código del backend
COPY App/fastapi_app/ .

# Variables de entorno
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV PYTHONPATH=/app

EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
