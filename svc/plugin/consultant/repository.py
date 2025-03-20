from svc.utils.dataset import read_csv, answers
import os
from svc.utils.database import db
from .schema import Consultant

dataset = read_csv(os.environ["DB"])

def consultant_list():
    db_results = db.company.find({})
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
