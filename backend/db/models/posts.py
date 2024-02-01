from pydantic import BaseModel
from typing import Optional
from .common import Pagination



class Post(BaseModel):
    title: str
    content: str
    
    
class PostCreate(Post):
    author: str 


class PostEdit(Post):
    pass


# for filtering
class PostFilter(Pagination):
    title: Optional[str] = None
    title__contains: Optional[str] = None
    content: Optional[str] = None
    content__contains: Optional[str] = None
    # date
    author: Optional[str] = None
    author__username: Optional[str] = None









