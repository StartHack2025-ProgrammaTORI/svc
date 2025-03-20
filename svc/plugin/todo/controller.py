from fastapi import APIRouter
from . import repository
router = APIRouter(prefix="/todos", tags=["todos"])

@router.get("")
async def get_todos():
    return { "data": repository.get_todos() }