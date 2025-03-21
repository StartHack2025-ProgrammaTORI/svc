from svc.utils.dataset import read_csv
import os
from svc.utils.database import db
from .schema import Consultant
from bson import ObjectId
dataset = read_csv(os.environ["DB"])

def consultant_list(black_list_focus_area: list = None, black_list_company: list = None):
    find = {}
    if black_list_focus_area is not None:
        find["focus_areas"] = { "$nin": black_list_focus_area }
    if black_list_company is not None:
        find["_id"] = { "$nin": [ObjectId(c) for c in black_list_company] }

    db_results = db.company.find(find)
    return [Consultant(**item).dict() for item in db_results]

def create_user(body: dict):
    db.user.insert_one(body)
    return body

def get_user(uid: str):
    return db.user.find_one({"uid": uid})

def create_consultant(body: Consultant):
    return db.company.insert_one(body.dict()).inserted_id

def get_consultant(_id: str):
    return db.company.find_one({"_id": _id})

def get_consultant_by_uid(uid: str):
    return db.company.find_one({"uid": uid})

def update_black_list(_id: str, decision, consultant: dict):
    if decision == "area":
        return db.company.update_one({"_id": _id}, {"$push": {"black_list_area": consultant['focus_areas']}})
    elif decision == "company":
        return db.company.update_one({"_id": _id}, {"$push": {"black_list_company": consultant['id']}})

def update_consultant_details(
    _id: str,
    name: str = None, 
    description: str = None, 
    contact: str = None,
    revenue: str = None,
    is_b2b: bool = None,
    ):
    update_fields = {}
    if name is not None:
        update_fields["name"] = name
    if description is not None:
        update_fields["description"] = description
    if contact is not None:
        update_fields["contact"] = contact
    if revenue is not None:
        update_fields["revenue"] = revenue
    if is_b2b is not None:
        update_fields["is_b2b"] = is_b2b

    return db.company.update_one({"_id": ObjectId(_id)}, {"$set": update_fields})

