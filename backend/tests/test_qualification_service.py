"""Unit tests for deterministic qualification."""

from app.services.qualification_service import QualificationService


def test_high_score_complete_lead():
    svc = QualificationService()
    result = svc.calculate(
        {
            "intent": "BUY",
            "budget_min": 70000000,
            "budget_max": 80000000,
            "timeframe": "WITHIN_1_MONTH",
            "location_text": "Lekki",
            "property_type": "APARTMENT",
            "bedrooms": 3,
            "email": "customer@example.com",
        }
    )
    assert result.score >= 70
    assert result.qualification_level == "HIGH"
    assert result.urgency == "HIGH"
    assert result.version == "qualification-v1"


def test_low_score_minimal_lead():
    svc = QualificationService()
    result = svc.calculate({"intent": None})
    assert result.score < 40
    assert result.qualification_level in ("LOW", "UNKNOWN")
    assert "intent" in (result.missing_information or [])
