import json
import os
from typing import List
from ..models.symptom_model import SymptomInput
from ..models.triage_model import TriageResult
from ..utils.nlp_utils import normalize_text, extract_symptoms
from ..config.settings import settings


class SymptomService:
    def __init__(self, emergency_rules: List[dict]):
        self.emergency_rules = emergency_rules

    def triage(self, payload: SymptomInput) -> TriageResult:
        text = normalize_text(payload.text or "")
        symptoms = payload.symptoms or extract_symptoms(text)

        reasons: List[str] = []

        for rule in self.emergency_rules:
            if any(k in text for k in rule.get("keywords", [])):
                reasons.append(rule.get("reason", "Emergency keyword match"))
        if reasons:
            return TriageResult(level="emergency", reasons=reasons, advice=self._advice_for("emergency", payload.language), language=payload.language, confidence=1.0)

        # Placeholder ML classifier: simple heuristic ranking
        urgency_score = 0
        for s in symptoms:
            if s in {"fever", "vomiting", "diarrhea"}:
                urgency_score += 1
            if s in {"chest pain", "breathlessness", "severe bleeding"}:
                urgency_score += 3

        if urgency_score >= 3:
            level = "urgent"
            confidence = 0.7
            reasons = ["Symptoms indicate medium-to-high urgency"]
        else:
            level = "homecare"
            confidence = 0.6
            reasons = ["Symptoms mild, suitable for home care with monitoring"]

        return TriageResult(level=level, reasons=reasons, advice=self._advice_for(level, payload.language), language=payload.language, confidence=confidence)

    def _advice_for(self, level: str, language: str) -> str:
        if level == "emergency":
            return {
                "en": "Immediate medical attention required. Call local emergency services or go to the nearest hospital.",
                "hi": "तुरंत चिकित्सा सहायता लें। नजदीकी अस्पताल जाएं या आपातकालीन सेवाओं को कॉल करें।",
            }.get(language, "Immediate medical attention required.")
        if level == "urgent":
            return {
                "en": "Consult a doctor within 24 hours. Keep hydrated and monitor symptoms.",
                "hi": "24 घंटे के भीतर डॉक्टर से संपर्क करें। पानी पीते रहें और लक्षणों पर नज़र रखें।",
            }.get(language, "Consult a doctor within 24 hours.")
        return {
            "en": "Home care is likely sufficient. Rest, fluids, and monitor for any worsening.",
            "hi": "घरेलू देखभाल पर्याप्त हो सकती है। आराम करें, तरल पिएँ और स्थिति बिगड़ने पर ध्यान दें।",
        }.get(language, "Home care is likely sufficient.")


def _load_rules() -> List[dict]:
    path = settings.EMERGENCY_RULES_PATH
    if os.path.exists(path):
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    return [
        {"keywords": ["severe bleeding", "unconscious", "no pulse", "stroke"], "reason": "Severe emergency symptoms"},
        {"keywords": ["chest pain", "breathlessness"], "reason": "Possible cardiac/respiratory emergency"},
    ]


_global_symptom_service: SymptomService | None = None


def get_symptom_service() -> SymptomService:
    global _global_symptom_service
    if _global_symptom_service is None:
        _global_symptom_service = SymptomService(emergency_rules=_load_rules())
    return _global_symptom_service

