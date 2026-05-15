# main.py -- BankService FastAPI Entry Point
# Dependency Injection and router registration will be wired in CAM-12.

from fastapi import FastAPI

app = FastAPI(
    title="BankService API",
    description="API bancaria con Arquitectura Hexagonal (Ports & Adapters) y DDD.",
    version="0.1.0",
)


@app.get("/health", tags=["health"])
def health_check() -> dict:
    """Endpoint de verificación de vida del servicio."""
    return {"status": "ok", "service": "BankService"}
