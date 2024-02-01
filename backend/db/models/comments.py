from pydantic import BaseModel
from datetime import datetime

class Comment(BaseModel):
    content: str
    author: str
    date: datetime = None




