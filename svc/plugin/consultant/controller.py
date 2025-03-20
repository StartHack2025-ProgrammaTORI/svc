from fastapi import APIRouter, HTTPException, Depends
from . import repository
from svc.hook.auth.index import validate_token
from .schema import Consultant

router = APIRouter(prefix="/consultants", tags=["consultants"])

@router.get("")
async def get_consultants():
    return {"message": "Consultant created successfully", "data": repository.consultant_list()}

@router.post("")
async def create_consultant(
    body: Consultant = None,
    user: dict = Depends(validate_token)
):
    print(user)
    u = repository.get_user(user["uid"])
    print(u)
    if u:
        return {"message": "Consultant already exists", "data": repository.consultant_list()}
    company = repository.create_consultant(body)
    repository.create_user({
        "uid": user["uid"],
        "email": user["email"],
        "company": company
    })
    return {"message": "Consultant created successfully", "data": repository.consultant_list()}
