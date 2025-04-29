import os
from io import BytesIO

import pytest
from werkzeug.datastructures import FileStorage

from src.classifier import classify_file

FILES_FOLDER = os.path.join(os.path.dirname(__file__), "../files")


@pytest.mark.parametrize(
    ("file_name", "expected_class"),
    [
        ("bank_statement_1.pdf", "bank_statement"),
        ("bank_statement_2.pdf", "bank_statement"),
        ("bank_statement_3.pdf", "bank_statement"),
        ("drivers_licence_2.jpg", "drivers_licence"),
        ("drivers_license_1.jpg", "drivers_licence"),
        ("drivers_license_3.jpg", "drivers_licence"),
        ("invoice_1.pdf", "invoice"),
        ("invoice_2.pdf", "invoice"),
        ("invoice_3.pdf", "invoice"),
        ("unknown_file_1.txt", "unknown_file"),
        ("unknown_file_2.docx", "unknown_file"),
        ("unknown_file_3.pptx", "unknown_file"),
        ("unknown_file_4.jpg", "unknown_file"),
        ("unknown_file_5.png", "unknown_file"),
    ],
)
def test_classify_file(file_name: str, expected_class: str) -> None:
    dummy_file = FileStorage(
        stream=BytesIO(b"Dummy data"),
        filename=file_name,
        content_type="application/octet-stream",
    )
    result = classify_file(dummy_file)
    assert result == expected_class
