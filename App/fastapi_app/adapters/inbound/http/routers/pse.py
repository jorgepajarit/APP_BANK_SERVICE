from fastapi import APIRouter, Depends
from App.fastapi_app.adapters.inbound.http.schemas import PSEPaymentRequest, PSEWebhookRequest
from App.fastapi_app.application.banking.services import PSEService
from App.fastapi_app.adapters.inbound.http.dependencies import get_pse_service

router = APIRouter(prefix="/pse", tags=["pse"])

@router.post("/payment")
def initiate_payment(request: PSEPaymentRequest, pse_service: PSEService = Depends(get_pse_service)):
    transaction_id = pse_service.initiate_payment(request.account_id, request.amount)
    return {"transaction_id": transaction_id, "status": "PENDING"}

@router.post("/webhook")
def process_webhook(request: PSEWebhookRequest, pse_service: PSEService = Depends(get_pse_service)):
    pse_service.process_webhook(request.transaction_id, request.status)
    return {"message": "Webhook processed successfully"}
