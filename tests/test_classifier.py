import os
from io import BytesIO

import pytest
from rapidfuzz import fuzz
from werkzeug.datastructures import FileStorage

from src.classifier import MINIMUM_CONFIDENCE, classify_file
from src.extract_text import detect_mime_type, extract_pdf_text

FILES_FOLDER = os.path.join(os.path.dirname(__file__), "../files")


@pytest.mark.parametrize(
    ("file_name", "expected_class"),
    [
        ("bank_statement_1.pdf", "bank_statement"),
        ("bank_statement_2", "bank_statement"),
        ("bank_statement_3.docx", "bank_statement"),
        ("drivers_licence_2.jpg", "drivers_licence"),
        ("drivers_license_1.jpg", "drivers_licence"),
        ("driving_license_3.jpg", "drivers_licence"),
        ("invoice.pdf", "invoice"),
        ("invoice_2.pdf", "invoice"),
        ("2025_invoice.pdf", "invoice"),
        ("unknown_file.txt", "unknown_file"),
        ("qwertyuiop.docx", "unknown_file"),
        (".env", "unknown_file"),
    ],
)
def test_classify_file_by_name(file_name: str, expected_class: str) -> None:
    dummy_file = FileStorage(
        stream=BytesIO(b"Dummy data"),
        filename=file_name,
        content_type="application/octet-stream",
    )
    result = classify_file(dummy_file)
    assert result == expected_class


@pytest.mark.parametrize(
    ("file_name", "expected_class"),
    [
        ("bank_statement_1.pdf", "application/pdf"),
        ("bank_statement_2.pdf", "application/pdf"),
        ("bank_statement_3.pdf", "application/pdf"),
        ("bank_statement_4.docx", "application/zip"),
        ("bank_statement_5.docx", "application/zip"),
        ("drivers_license_1.jpg", "image/jpeg"),
        ("drivers_licence_2.jpg", "image/jpeg"),
        ("drivers_license_3.jpg", "image/jpeg"),
        ("invoice_1.pdf", "application/pdf"),
        ("invoice_2.pdf", "application/pdf"),
        ("invoice_3.pdf", "application/pdf"),
        ("invoice_4.docx", "application/zip"),
    ],
)
def test_mime_detection(file_name: str, expected_class: str) -> None:
    file_path = os.path.join(FILES_FOLDER, file_name)
    assert detect_mime_type(file_path) == expected_class


@pytest.mark.parametrize(
    ("file_name", "expected_class"),
    [
        ("scan_1.pdf", "invoice"),
        ("scan_2.pdf", "bank_statement"),
        ("scan_3.pdf", "invoice"),
        ("scan_4.pdf", "drivers_licence"),
    ],
)
def test_scanned_pdf_ocr_fallback(file_name: str, expected_class: str) -> None:
    text = extract_pdf_text(os.path.join(FILES_FOLDER, file_name))
    score = fuzz.partial_ratio(expected_class, text.lower())
    assert score > MINIMUM_CONFIDENCE


@pytest.mark.parametrize(
    ("file_name", "expected_class"),
    [
        ("bank_statement_1.pdf", "bank_statement"),
        ("bank_statement_2.pdf", "bank_statement"),
        ("bank_statement_3.pdf", "bank_statement"),
        ("bank_statement_4.docx", "bank_statement"),
        ("bank_statement_5.docx", "bank_statement"),
        ("drivers_license_1.jpg", "drivers_licence"),
        ("drivers_licence_2.jpg", "drivers_licence"),
        ("drivers_license_3.jpg", "drivers_licence"),
        ("invoice_1.pdf", "invoice"),
        ("invoice_2.pdf", "invoice"),
        ("invoice_3.pdf", "invoice"),
        ("invoice_4.docx", "invoice"),
    ],
)
def test_classify_file(file_name: str, expected_class: str) -> None:
    file_path = os.path.join(FILES_FOLDER, file_name)
    with open(file_path, "rb") as f:
        file = FileStorage(
            stream=f,
            filename="unhelpful_name",
            content_type="application/octet-stream",
        )
        result = classify_file(file)
    assert result == expected_class
