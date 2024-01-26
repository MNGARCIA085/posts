
from pydantic import BaseModel



class Pagination(BaseModel):
    page_size: int = 10
    page: int = 1




