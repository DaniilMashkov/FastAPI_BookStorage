import os
import tempfile
import pytest
from fastapi.testclient import TestClient
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

from app.main import app

@pytest.fixture(scope='module')
def pdf_file():
    temp_file = tempfile.NamedTemporaryFile(delete=True, suffix=".pdf")
    temp_file.close()

    c = canvas.Canvas(temp_file.name, pagesize=letter)
    c.drawString(100, 750, "This is a test PDF file.")
    c.save()

    yield temp_file.name

    os.remove(temp_file.name)

@pytest.fixture(scope='module')
def client():
    return TestClient(app)
