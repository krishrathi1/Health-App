import re
from typing import List


def normalize_text(text: str) -> str:
    text = text.lower().strip()
    text = re.sub(r"\s+", " ", text)
    return text


def extract_symptoms(text: str) -> List[str]:
    keywords = [
        "fever",
        "cough",
        "headache",
        "chest pain",
        "breathlessness",
        "vomiting",
        "diarrhea",
        "severe bleeding",
    ]
    return [k for k in keywords if k in text]

