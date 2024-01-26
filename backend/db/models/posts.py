from pydantic import BaseModel
from typing import List
from datetime import datetime
from .comments import Comment


class Post(BaseModel):
    title: str
    content: str
    author: str
    
class PostCreate(Post):
    pass

class PostView(Post):
    comments: List[Comment] = []
    date: datetime = None







