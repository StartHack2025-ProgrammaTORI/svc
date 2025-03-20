from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
from typing import Optional
from pydantic_mongo import PydanticObjectId

class Answer(BaseModel):
    id: str  # Change this to make it public
    text: str

class Question(BaseModel):
    id: PydanticObjectId = Field(alias="_id")
    question: str
    options: list[Answer]
    uid: str
    answer: Optional[str] = None
    created_at: datetime = datetime.now()

class QuestionAnswer(BaseModel):
    question: str
    answer: str
