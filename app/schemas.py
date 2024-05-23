from pydantic import BaseModel

class BookBase(BaseModel):
    title: str
    author: str

class BookCreate(BookBase):
    pass

class BookUpdate(BookBase):
    pass

class DeleteResponse(BaseModel):
    message: str

class Book(BookBase):
    id: int

    class Config:
        orm_mode = True
