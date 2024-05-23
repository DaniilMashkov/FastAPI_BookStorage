def test_create_book(client, pdf_file):
    with open(pdf_file, "rb") as file:
        response = client.post(
            "/books/",
            files={"file": ("test.pdf", file)},
            data={"title": "Test Book", "author": "Test Author"}
        )

    assert response.status_code == 200
    assert response.json()["title"] == "Test Book"
    assert response.json()["author"] == "Test Author"

    book_id = response.json()["id"]
    response = client.delete(f"/books/{book_id}")
    assert response.status_code == 200


def test_get_books(client, pdf_file):
    with open(pdf_file, "rb") as file:
        response = client.post(
            "/books/",
            files={"file": ("test.pdf", file)},
            data={"title": "Test Book", "author": "Test Author"}
        )

    assert response.status_code == 200
    book_id = response.json()["id"]

    response = client.get("/books/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)
    assert any(book["title"] == "Test Book" and book["author"] == "Test Author" for book in response.json())

    response = client.delete(f"/books/{book_id}")
    assert response.status_code == 200


def test_update_book(client, pdf_file):
    with open(pdf_file, "rb") as file:
        response = client.post(
            "/books/",
            files={"file": ("test.pdf", file)},
            data={"title": "Test Book", "author": "Test Author"}
        )

    assert response.status_code == 200
    book_id = response.json()["id"]

    response = client.put(
        f"/books/{book_id}",
        json={"title": "Updated Test Book", "author": "Updated Test Author"}
    )
    assert response.status_code == 200
    assert response.json()["title"] == "Updated Test Book"
    assert response.json()["author"] == "Updated Test Author"

    # Удаление созданной книги
    response = client.delete(f"/books/{book_id}")
    assert response.status_code == 200

def test_delete_book(client, pdf_file):
    with open(pdf_file, "rb") as file:
        response = client.post(
            "/books/",
            files={"file": ("test.pdf", file)},
            data={"title": "Test Book", "author": "Test Author"}
        )

    assert response.status_code == 200
    book_id = response.json()["id"]

    response = client.delete(f"/books/{book_id}")

    assert response.status_code == 200
    assert response.json()["message"] == "Book deleted successfully"


def test_get_book_file(client, pdf_file):
    with open(pdf_file, "rb") as file:
        response = client.post(
            "/books/",
            files={"file": ("test.pdf", file)},
            data={"title": "Test Book", "author": "Test Author"}
        )

    assert response.status_code == 200
    book_id = response.json()["id"]

    response = client.get(f"/books/{book_id}/file")
    assert response.status_code == 200
    assert response.headers["Content-Type"] == "application/octet-stream"

    response = client.delete(f"/books/{book_id}")
    assert response.status_code == 200
