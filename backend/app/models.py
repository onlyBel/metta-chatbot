from pydantic import BaseModel
from typing import Optional

class Fact(BaseModel):
    subject: str
    predicate: str
    obj: str
    source: Optional[str] = None

class AskRequest(BaseModel):
    question: str

