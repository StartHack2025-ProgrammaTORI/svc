from pydantic import BaseModel
from typing import Optional

class Consultant(BaseModel):
    _id: str
    uid: Optional[str] = None
    category: Optional[str] = None
    institution: Optional[str] = None
    name: Optional[str] = None
    description: Optional[str] = None
    focus_areas: Optional[str] = None
    contact: Optional[str] = None
    website: Optional[str] = None