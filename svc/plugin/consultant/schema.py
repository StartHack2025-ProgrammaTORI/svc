from pydantic import BaseModel
from typing import Optional
from pydantic_mongo import PydanticObjectId
from pydantic import Field

class Consultant(BaseModel):
    id: PydanticObjectId = Field(alias="_id")
    uid: Optional[str] = None
    category: Optional[str] = None
    institution: Optional[str] = None
    name: Optional[str] = None
    description: Optional[str] = None
    focus_areas: Optional[str] = None
    contact: Optional[str] = None
    website: Optional[str] = None
    revenue: Optional[str] = None
    is_b2b: Optional[bool] = None
    black_list_company: list[str] = []
    black_list_focus_area: list[str] = []