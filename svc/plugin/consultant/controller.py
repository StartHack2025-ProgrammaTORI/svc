from fastapi import APIRouter, HTTPException, Depends
from . import repository
from svc.hook.auth.index import validate_token
from .schema import Consultant

router = APIRouter(prefix="/consultants", tags=["consultants"])

@router.get("")
async def get_consultant(user: dict = Depends(validate_token)):
    db_user = repository.get_user(user['uid'])
    my_company = repository.get_consultant_populated(db_user['company'])
    my_company['_id'] = str(my_company['id'])
    return {"message": "Consultant created successfully", "data": my_company}

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

@router.put("")
async def update_consultant(
    body: dict,
    user: dict = Depends(validate_token)
):
    db_user = repository.get_user(user['uid'])
    my_company = repository.get_consultant(db_user['company'])
    repository.update_consultant_details(
        my_company['_id'],
        body["name"] if "name" in body else None,
        body["description"] if "description" in body else None,
        body["contact"] if "contact" in body else None,
        body["revenue"] if "revenue" in body else None,
        body["is_b2b"] if "is_b2b" in body else None,
    )
    return {"message": "Consultant created successfully", "data": repository.consultant_list()}
