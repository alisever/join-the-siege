import os
from collections.abc import Generator
from http import HTTPStatus
from io import BytesIO
from typing import Any

import pytest
from flask.testing import FlaskClient
from pytest_mock import MockerFixture

from src.app import allowed_file, app

FILES_FOLDER = os.path.join(os.path.dirname(__file__), "../files")


@pytest.fixture
def client() -> Generator[FlaskClient, Any, None]:
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client


@pytest.mark.parametrize(
    ("filename", "expected"),
    [
        ("file.pdf", True),
        ("file.png", True),
        ("file.jpg", True),
        ("file.docx", True),
        ("file.txt", False),
        ("file", False),
    ],
)
def test_allowed_file(filename: str, expected: str) -> None:
    assert allowed_file(filename) == expected


def test_no_file_in_request(client: FlaskClient) -> None:
    response = client.post("/classify_file")
    assert response.status_code == HTTPStatus.BAD_REQUEST


def test_no_selected_file(client: FlaskClient) -> None:
    data = {"file": (BytesIO(b""), "")}  # Empty filename
    response = client.post(
        "/classify_file",
        data=data,
        content_type="multipart/form-data",
    )
    assert response.status_code == HTTPStatus.BAD_REQUEST


def test_success(client: FlaskClient, mocker: MockerFixture) -> None:
    mocker.patch("src.app.classify_file", return_value="test_class")

    data = {"file": (BytesIO(b"dummy content"), "file.pdf")}
    response = client.post(
        "/classify_file",
        data=data,
        content_type="multipart/form-data",
    )
    assert response.status_code == HTTPStatus.OK
    assert response.get_json() == {"file_class": "test_class"}


@pytest.mark.parametrize(
    ("file_name", "expected_class"),
    [
        ("bank_statement_1.pdf", "bank_statement"),
        ("bank_statement_5.docx", "bank_statement"),
        ("drivers_license_1.jpg", "drivers_licence"),
        ("invoice_1.pdf", "invoice"),
        ("passport_1.jpg", "passport"),
        ("scan_1.pdf", "invoice"),
    ],
)
def test_classify_file(client: FlaskClient, file_name: str, expected_class: str) -> None:
    file_path = os.path.join(FILES_FOLDER, file_name)
    with open(file_path, "rb") as f:
        data = {"file": (f, file_name)}
        response = client.post(
            "/classify_file",
            data=data,
            content_type="multipart/form-data",
        )
    assert response.status_code == HTTPStatus.OK
    assert response.get_json() == {"file_class": expected_class}
