from sqlalchemy import Column, Integer, String
from app.database import Base


class Book(Base):
    __tablename__ = "books"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    author = Column(String, index=True)
    file_name = Column(String)
    file_path = Column(String, unique=True)
    file_hash = Column(String, unique=True, index=True)
