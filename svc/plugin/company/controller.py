from fastapi import APIRouter, HTTPException
from . import repository
router = APIRouter(prefix="/companies", tags=["companies"])

@router.get("")
async def get_question(index: int = None):
    return { "data": repository.get_question(index)}

@router.post("")
async def answer_questions(body: dict = None):
    if body == None or body['index_answer'] == None or body['index_question'] == None:
        raise HTTPException(status_code=400, detail="Answer is required")
    return { "data": repository.answer_question(body['index_question'], body['index_answer'])}
