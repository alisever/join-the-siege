import logging
import os
import tempfile

from rapidfuzz import fuzz
from werkzeug.datastructures import FileStorage

from src.extract_text import extract_text

logger = logging.getLogger(__name__)

MINIMUM_CONFIDENCE = 70

FILE_CLASSES = {
    "drivers_licence": ["licence", "license", "driver", "driver", "driving", "driving"],
    "bank_statement": ["bank statement", "bank stmt", "statement", "bank report"],
    "invoice": ["invoice", "inv", "bill", "receipt", "tax invoice"],
    "passport": ["passport", "travel document"],
}


def classify_file(file: FileStorage) -> str:
    # Save the uploaded file temporarily
    with tempfile.NamedTemporaryFile(delete=False) as tmp:
        file.save(tmp.name)
        file_path = tmp.name

    try:
        filename = file.filename.lower()
        file_text = extract_text(file_path).lower()

    finally:
        os.unlink(file_path)

    combined_text = f"{filename} {file_text}"

    scores = {}

    for classification, keywords in FILE_CLASSES.items():
        score = max(fuzz.partial_ratio(keyword, combined_text) for keyword in keywords)
        if score < MINIMUM_CONFIDENCE:
            for keyword in keywords:
                keyword_score = fuzz.partial_ratio(keyword, combined_text)
                logger.warning("Keyword match for %s: %s with score %s", classification, keyword, keyword_score)
        scores[classification] = score

    sorted_scores = sorted(scores.items(), key=lambda x: x[1], reverse=True)

    best_match, best_score = sorted_scores[0]

    if best_score < MINIMUM_CONFIDENCE:
        logger.warning("Low confidence classification for %s: %s with score %s", file.filename, best_match, best_score)
        return "unknown_file"
    return best_match
