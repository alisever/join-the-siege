from collections.abc import Generator
from http import HTTPStatus
from io import BytesIO
from typing import Any

import pytest
from flask.testing import FlaskClient
from pytest_mock import MockerFixture

from src.app import allowed_file, app


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
