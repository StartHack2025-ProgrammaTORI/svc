from pydantic import BaseModel
from typing import Optional
from pydantic_mongo import PydanticObjectId
from pydantic import Field
from datetime import datetime
from enum import Enum

class Status(str, Enum):
    PENDING = "PENDING"
    ACCEPTED = "ACCEPTED"
    REJECTED = "REJECTED"
    
class InputProposal(BaseModel):
    consultancy_receiver: str # company id
    consultancy_provider: str # company id
    status: Status = Status.PENDING
    reason_of_rejection: Optional[str] = None
    reason_of_match: Optional[str] = None
    created_at: datetime = datetime.now()
    
class Proposal(BaseModel):
    id: PydanticObjectId = Field(alias="_id")
    consultancy_receiver: str # company id
    consultancy_provider: str # company id
    status: Status = Status.PENDING
    reason_of_rejection: Optional[str] = None
    reason_of_match: Optional[str] = None
    created_at: datetime = datetime.now()