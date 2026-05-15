from fastapi import FastAPI
from App.fastapi_app.adapters.inbound.http.routers import auth, banking, pse
from App.fastapi_app.adapters.inbound.http.exception_handlers import domain_error_handler
from App.fastapi_app.domain.exceptions import DomainError

app = FastAPI(title="BankService API", description="Hexagonal Architecture Bank API")

app.add_exception_handler(DomainError, domain_error_handler)

app.include_router(auth.router)
app.include_router(banking.router)
app.include_router(pse.router)

@app.get("/health")
def health_check():
    return {"status": "ok"}
