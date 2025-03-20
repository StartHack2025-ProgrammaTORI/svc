from fastapi import APIRouter, HTTPException, Depends
from svc.hook.auth.index import validate_token
from . import repository

router = APIRouter(prefix="/questions", tags=["questions"])


@router.get("")
async def get_question(index: int = None, user: dict = Depends(validate_token)):
    return { "data": await repository.get_question(index, user['uid'])}

@router.post("")
async def answer_questions(body: dict = None, user: dict = Depends(validate_token)):
    if body == None or body['index_answer'] == None or body['index_question'] == None:
        raise HTTPException(status_code=400, detail="Answer is required")
    return { "data": repository.answer_question(body['index_question'], body['index_answer'], user['uid'])}
