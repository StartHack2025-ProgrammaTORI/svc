from fastapi import APIRouter, HTTPException
from svc.utils.userRecomendation import userRec
from svc.utils.dataset import answers
router = APIRouter(prefix="/recommendations", tags=["recommendations"])

@router.get("")
async def get_recomendation():
    return {"message": "Consultant created successfully", "data": userRec.find_best_match(answers)}
