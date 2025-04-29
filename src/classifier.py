import logging
import os

from rapidfuzz import fuzz
from werkzeug.datastructures import FileStorage

logger = logging.getLogger(__name__)

MINIMUM_CONFIDENCE = 70

FILE_CLASSES = [
    "drivers_licence",
    "bank_statement",
    "invoice",
]


def classify_file(file: FileStorage) -> str:
    filename = file.filename.lower()
    filename = os.path.splitext(filename)[0]
    # file_bytes = file.read()  # noqa ERA001

    best_match, best_score = "unknown_file", 0

    for classification in FILE_CLASSES:
        score = fuzz.partial_ratio(classification, filename)
        if score > best_score:
            best_match, best_score = classification, score

    if best_score < MINIMUM_CONFIDENCE:
        logger.warning("Low confidence classification for %s: %s with score %s", file.filename, best_match, best_score)
        return "unknown_file"

    return best_match
