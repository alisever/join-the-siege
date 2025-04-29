import zipfile
from sys import platform

import docx2txt
import fitz  # PyMuPDF
import magic
import pytesseract
from PIL import Image

MINIMUM_PDF_TEXT_LENGTH = 10

# Set the tesseract_cmd path for Windows
if platform.startswith("win32"):
    # Adjust the path to where Tesseract is installed on your system
    pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"


def detect_mime_type(file_path: str) -> str:
    mime = magic.Magic(mime=True)
    return mime.from_file(file_path)


def is_docx_file(file_path: str) -> bool:
    try:
        with zipfile.ZipFile(file_path, "r") as zipf:
            return "word/document.xml" in zipf.namelist()
    except zipfile.BadZipFile:
        return False


def extract_text(file_path: str) -> str:
    mime_type = detect_mime_type(file_path)

    if mime_type == "application/pdf":
        return extract_pdf_text(file_path)
    if mime_type.startswith("image/"):
        return extract_image_text(file_path)
    if mime_type == "application/zip" and is_docx_file(file_path):
        return extract_docx_text(file_path)
    if mime_type == "text/plain":
        return extract_txt_text(file_path)
    return ""


def extract_pdf_text(file_path: str) -> str:
    text = ""
    with fitz.open(file_path) as doc:
        for _, page in enumerate(doc):
            page_text = page.get_text()

            if len(page_text.strip()) >= MINIMUM_PDF_TEXT_LENGTH:
                text += page_text

            # Fallback to using OCR
            else:
                pix = page.get_pixmap(dpi=300)
                img = Image.frombytes("RGB", (pix.width, pix.height), pix.samples)
                ocr_text = pytesseract.image_to_string(img)
                text += ocr_text

    return text


def extract_image_text(file_path: str) -> str:
    image = Image.open(file_path)
    return pytesseract.image_to_string(image)


def extract_docx_text(file_path: str) -> str:
    return docx2txt.process(file_path)


def extract_txt_text(file_path: str) -> str:
    with open(file_path, encoding="utf-8") as f:
        return f.read()
