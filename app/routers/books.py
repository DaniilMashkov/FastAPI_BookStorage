from typing import List
from io import StringIO
import csv
import hashlib
import os

from fastapi import APIRouter, HTTPException, UploadFile, \
    File, Query, Form, Depends

from fastapi.responses import StreamingResponse, FileResponse

from sqlalchemy.orm import Session

from app import crud, schemas
from app.models import Book
from app.database import get_db

router = APIRouter(
    prefix="/books",
    tags=["books"]
)

@router.post("/",
             response_model=schemas.Book,
             summary='Upload book',
             description='Accepts PDF files up to 2MB in size.\
                    Uploading the same file is restricted.\
                    Book titles with authors must be unique.')
async def create_book(
    title: str = Form(...),
    author: str = Form(...),
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    if file.content_type != "application/pdf":
        raise HTTPException(status_code=400, detail="File must be a PDF")

    file_data = await file.read()

    if len(file_data) > 2 * 1024 * 1024:
        raise HTTPException(status_code=400, detail="File size exceeds 2MB")

    file_hash = hashlib.sha256(file_data).hexdigest()
    existing_file = db.query(Book).filter(Book.file_hash == file_hash).first()
    if existing_file:
        raise HTTPException(status_code=400,
                            detail="File with the same content already exists")

    existing_book = db.query(Book).filter(
        Book.title == title, Book.author == author).first()
    if existing_book:
        raise HTTPException(
            status_code=400,
            detail="Book with the same author and title already exists")

    db_book = crud.create_book(
        db=db,
        book=schemas.BookCreate(
            title=title, author=author),
        file_name=file.filename,
        file_data=file_data)

    if not db_book:
        raise HTTPException(status_code=400, detail="Book uploading failed")
    return db_book

@router.get("/{book_id}/file")
def get_book_file(book_id: int, db: Session = Depends(get_db)):
    db_book = crud.get_book(db, book_id=book_id)
    if db_book is None:
        raise HTTPException(status_code=404, detail="Book not found")

    def generate():
        with open(db_book.file_path, "rb") as file:
            yield from file

    headers = {
        "Content-Disposition": f"attachment; filename={db_book.file_name}",
        "Content-Type": "application/octet-stream"
    }

    return StreamingResponse(generate(), headers=headers)

@router.get("/", response_model=List[schemas.Book], summary='Get book list')
def read_books(
    author: str = Query(None),
    title: str = Query(None),
    db: Session = Depends(get_db)
):
    books = crud.get_books(db, author=author, title=title)
    return books

@router.get("/csv", response_class=FileResponse)
def get_books_csv(db: Session = Depends(get_db)):
    books = crud.get_books(db)
    output = StringIO()
    writer = csv.writer(output)
    writer.writerow(["ID", "Title", "Author", "File Name"])
    for book in books:
        writer.writerow([book.id, book.title, book.author, book.file_name])
    output.seek(0)

    headers = {
        "Content-Disposition": "attachment; filename=books.csv",
        "Content-Type": "application/octet-stream"
    }
    return StreamingResponse(output, media_type="text/csv", headers=headers)

@router.put("/{book_id}", response_model=schemas.Book)
def update_book(book_id: int, book: schemas.BookUpdate, db: Session = Depends(get_db)):
    db_book = crud.update_book(db=db, book_id=book_id, book=book)
    if db_book is None:
        raise HTTPException(status_code=404, detail="Book not found")
    return db_book

@router.delete("/{book_id}", response_model=schemas.DeleteResponse)
async def delete_book(
    book_id: int,
    db: Session = Depends(get_db)
):
    db_book = crud.get_book(db=db, book_id=book_id)
    if not db_book:
        raise HTTPException(status_code=404, detail="Book not found")

    if db_book.file_path:
        if os.path.exists(db_book.file_path):
            os.remove(db_book.file_path)

    crud.delete_book(db=db, book_id=book_id)

    return {"message": "Book deleted successfully"}
