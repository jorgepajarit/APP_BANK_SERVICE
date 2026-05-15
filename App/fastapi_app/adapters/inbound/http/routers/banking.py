from fastapi import APIRouter, Depends
from typing import List
from App.fastapi_app.adapters.inbound.http.schemas import (
    TransferRequest, FinancialSummaryResponse, MovementResponse
)
from App.fastapi_app.application.banking.services import BankingQueryService, TransferService
from App.fastapi_app.adapters.inbound.http.dependencies import (
    get_banking_query_service, get_transfer_service
)

router = APIRouter(prefix="/banking", tags=["banking"])

@router.get("/summary/{user_id}", response_model=FinancialSummaryResponse)
def get_summary(user_id: int, query_service: BankingQueryService = Depends(get_banking_query_service)):
    summary = query_service.get_user_financial_summary(user_id)
    return FinancialSummaryResponse(**summary)

@router.get("/accounts/{account_id}/movements", response_model=List[MovementResponse])
def get_movements(account_id: int, query_service: BankingQueryService = Depends(get_banking_query_service)):
    movements = query_service.get_movements(account_id)
    return [
        MovementResponse(
            id=m.id,
            account_id=m.account_id,
            type=m.type.name,
            amount=m.amount
        ) for m in movements
    ]

@router.post("/transfer")
def transfer(request: TransferRequest, transfer_service: TransferService = Depends(get_transfer_service)):
    transfer_service.transfer(
        source_id=request.source_account_id,
        target_id=request.target_account_id,
        amount=request.amount
    )
    return {"message": "Transfer successful"}
