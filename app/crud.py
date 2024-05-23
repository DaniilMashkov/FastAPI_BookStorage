import os
import hashlib
from sqlalchemy.orm import Session
from app.models import Book
from app.schemas import BookCreate, BookUpdate

UPLOAD_DIR = "uploads"

def save_file(file_data: bytes, file_name: str) -> str:
    if not os.path.exists(UPLOAD_DIR):
        os.makedirs(UPLOAD_DIR)
    file_path = os.path.join(UPLOAD_DIR, file_name)
    with open(file_path, "wb") as f:
        f.write(file_data)
    return file_path


def get_book(db: Session, book_id: int):
    return db.query(Book).get(book_id)

def get_books(db: Session, author: str = '', title: str = ''):
    query = db.query(Book)
    if author:
        query = query.filter(Book.author == author)
    if title:
        query = query.filter(Book.title == title)
    return query.all()


def create_book(db: Session, book: BookCreate,
                file_name: str, file_data: bytes):
    file_hash = hashlib.sha256(file_data).hexdigest()

    existing_book = db.query(Book).filter(Book.file_hash == file_hash).first()
    if existing_book:
        return None

    file_path = save_file(file_data, file_name)

    new_book = Book(
        **book.model_dump(),
        file_name=file_name,
        file_hash=file_hash,
        file_path=file_path)

    db.add(new_book)
    db.commit()
    db.refresh(new_book)

    return new_book

def update_book(db: Session, book_id: int, book: BookUpdate):
    db_book = db.query(Book).get(book_id)
    if db_book is None:
        return None
    db_book.title = book.title
    db_book.author = book.author
    db.commit()
    db.refresh(db_book)
    return db_book

def delete_book(db: Session, book_id: int):
    db_book = db.query(Book).get(book_id)
    if db_book is None:
        return None
    db.delete(db_book)
    db.commit()
    return db_book
