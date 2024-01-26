from pydantic import BaseModel
from typing import List
from datetime import datetime

class Comment(BaseModel):
    content: str
    author: str
    date: datetime = None


