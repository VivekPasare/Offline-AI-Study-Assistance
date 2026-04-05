from pydantic import BaseModel
from typing import Optional, List

class QueryRequest(BaseModel):
    query: str
    mode: str = "Normal"  # Normal, Simple, Example
    language: str = "English"  # English, Hindi
    history: Optional[List[dict]] = []

class SummarizeRequest(BaseModel):
    text: str
    language: str = "English"

class QueryResponse(BaseModel):
    answer: str
    mode: str
    language: str
