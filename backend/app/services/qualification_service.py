"""Deterministic lead qualification service.

See docs/LEAD_QUALIFICATION_SPECIFICATION.md.

Score 0–100 based on:
- Intent clarity (20)
- Budget clarity (20)
- Timeframe (20)
- Location (15)
- Property requirements (10)
- Contactability (10)
- Engagement (5)

Levels: LOW 0–39 | MEDIUM 40–69 | HIGH 70–100
"""

from dataclasses import dataclass
from decimal import Decimal
from typing import Any, Optional


@dataclass
class QualificationResult:
    score: int
    qualification_level: str  # LOW | MEDIUM | HIGH | UNKNOWN
    urgency: str  # LOW | MEDIUM | HIGH | UNKNOWN
    version: str = "qualification-v1"
    missing_information: list[str] | None = None


class QualificationService:
    """Pure deterministic scoring — no AI."""

    VERSION = "qualification-v1"

    def calculate(self, lead_data: dict[str, Any]) -> QualificationResult:
        score = 0
        missing: list[str] = []

        # Intent clarity (20)
        intent = lead_data.get("intent")
        if intent and intent not in ("UNKNOWN", None):
            score += 20
        else:
            missing.append("intent")

        # Budget clarity (20)
        budget_min = lead_data.get("budget_min")
        budget_max = lead_data.get("budget_max")
        if budget_min is not None or budget_max is not None:
            score += 20
        else:
            missing.append("budget")

        # Timeframe (20)
        timeframe = lead_data.get("timeframe")
        if timeframe and timeframe not in ("UNKNOWN", None):
            score += 20
        else:
            missing.append("timeframe")

        # Location (15)
        location = lead_data.get("location_text")
        if location:
            score += 15
        else:
            missing.append("location")

        # Property requirements (10)
        prop_type = lead_data.get("property_type")
        bedrooms = lead_data.get("bedrooms")
        if prop_type or bedrooms is not None:
            score += 10
        else:
            missing.append("property_type_or_bedrooms")

        # Contactability (10) — simplified for MVP
        if lead_data.get("email") or lead_data.get("phone"):
            score += 10
        else:
            missing.append("contact")

        # Engagement (5) — placeholder; can use message count later
        score += 5

        level = self._score_to_level(score)
        urgency = self._derive_urgency(timeframe)

        return QualificationResult(
            score=min(score, 100),
            qualification_level=level,
            urgency=urgency,
            version=self.VERSION,
            missing_information=missing or None,
        )

    @staticmethod
    def _score_to_level(score: int) -> str:
        if score >= 70:
            return "HIGH"
        if score >= 40:
            return "MEDIUM"
        if score > 0:
            return "LOW"
        return "UNKNOWN"

    @staticmethod
    def _derive_urgency(timeframe: Optional[str]) -> str:
        if not timeframe or timeframe == "UNKNOWN":
            return "UNKNOWN"
        mapping = {
            "IMMEDIATE": "HIGH",
            "WITHIN_1_MONTH": "HIGH",
            "WITHIN_3_MONTHS": "MEDIUM",
            "OVER_3_MONTHS": "LOW",
            "RESEARCHING": "LOW",
        }
        return mapping.get(timeframe, "UNKNOWN")
