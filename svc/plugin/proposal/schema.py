from pydantic import BaseModel
from typing import Optional
from pydantic_mongo import PydanticObjectId
from pydantic import Field
from datetime import datetime
from enum import Enum
from svc.plugin.consultant.schema import Consultant

class Status(str, Enum):
    SUGGESTED = "SUGGESTED"
    PENDING = "PENDING"
    ACCEPTED = "ACCEPTED"
    REJECTED = "REJECTED"
    
class Role(str, Enum):
    RECEIVER = "RECEIVER"
    SENDER = "PROVIDER"
    
class InputProposal(BaseModel):
    consultancy_receiver: str # company id
    consultancy_provider: str # company id
    status: Status = Status.SUGGESTED
    reason_of_rejection: Optional[str] = None
    reason_of_match: Optional[str] = None
    created_at: datetime = datetime.now()
    
class Proposal(BaseModel):
    id: PydanticObjectId = Field(alias="_id")
    consultancy_receiver: str # company id
    consultancy_provider: str # company id
    status: Status = Status.SUGGESTED
    reason_of_rejection: Optional[str] = None
    reason_of_match: Optional[str] = None
    created_at: datetime = datetime.now()
    
class ProposalPopulated(BaseModel):
    id: PydanticObjectId = Field(alias="_id")
    consultancy_receiver: Consultant
    consultancy_provider: Consultant
    status: Status = Status.SUGGESTED
    reason_of_rejection: Optional[str] = None
    reason_of_match: Optional[str] = None
    created_at: datetime = datetime.now()