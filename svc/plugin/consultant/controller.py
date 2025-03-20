from fastapi import APIRouter, HTTPException
from . import repository
router = APIRouter(prefix="/consultants", tags=["consultants"])

@router.get("")
async def get_consultants():
    return {"message": "Consultant created successfully", "data": repository.list()}
