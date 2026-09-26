"""Requirement extraction — rule-based MVP + optional AI.

Rule-based extractor works offline and handles common Nigerian real-estate phrases.
AI adapter can be swapped in later without changing callers.
"""

from __future__ import annotations

import re
from typing import Optional

from app.schemas.extraction import CustomerExtract, ExtractionResult


class ExtractionService:
    """Extract structured requirements from a customer message."""

    INTENT_PATTERNS = [
        (r"\b(buy|buying|purchase|purchasing)\b", "BUY"),
        (r"\b(rent|renting|lease|leasing)\b", "RENT"),
        (r"\b(sell|selling)\b", "SELL"),
    ]

    PROPERTY_PATTERNS = [
        (r"\b(apartment|flat|flats)\b", "APARTMENT"),
        (r"\b(house|bungalow)\b", "HOUSE"),
        (r"\b(duplex)\b", "DUPLEX"),
        (r"\b(land|plot)\b", "LAND"),
        (r"\b(office)\b", "OFFICE"),
        (r"\b(commercial|shop|warehouse)\b", "COMMERCIAL"),
    ]

    TIMEFRAME_PATTERNS = [
        (r"\b(immediately|asap|right away|urgent)\b", "IMMEDIATE"),
        (r"\b(within\s*1\s*month|this month|next month)\b", "WITHIN_1_MONTH"),
        (r"\b(within\s*3\s*months?|in\s*3\s*months?)\b", "WITHIN_3_MONTHS"),
        (r"\b(over\s*3\s*months?|later|next year)\b", "OVER_3_MONTHS"),
        (r"\b(just\s*looking|researching|browsing)\b", "RESEARCHING"),
    ]

    LOCATION_HINTS = [
        "lekki", "ikeja", "victoria island", "vi", "ikoyi", "ajah", "yaba",
        "surulere", "maryland", "gbagada", "magodo", "banana island",
        "ibadan", "abuja", "port harcourt", "ph", "enugu", "lagos",
    ]

    HANDOFF_PATTERNS = [
        r"\b(speak\s+to\s+(an?\s+)?agent|talk\s+to\s+(a\s+)?human|connect\s+me|real\s+person|human\s+agent)\b",
        r"\b(complaint|angry|frustrated|not\s+happy)\b",
    ]

    def extract(self, message: str) -> ExtractionResult:
        text = message.strip()
        lower = text.lower()

        intent = self._match_first(lower, self.INTENT_PATTERNS) or "PROPERTY_ENQUIRY"
        property_type = self._match_first(lower, self.PROPERTY_PATTERNS)
        bedrooms = self._extract_bedrooms(lower)
        location = self._extract_location(lower)
        budget_min, budget_max = self._extract_budget(lower)
        timeframe = self._match_first(lower, self.TIMEFRAME_PATTERNS)
        requires_human, handoff_reason = self._check_handoff(lower)

        missing: list[str] = []
        if not intent or intent == "UNKNOWN":
            missing.append("intent")
        if not location:
            missing.append("location")
        if budget_min is None and budget_max is None:
            missing.append("budget")
        if not property_type and bedrooms is None:
            missing.append("property_type_or_bedrooms")
        if not timeframe:
            missing.append("timeframe")

        confidence = self._estimate_confidence(
            intent, property_type, bedrooms, location, budget_min, budget_max, timeframe
        )

        suggested = self._suggest_next_question(missing)
        response = self._build_response(
            intent=intent,
            property_type=property_type,
            bedrooms=bedrooms,
            location=location,
            budget_min=budget_min,
            budget_max=budget_max,
            timeframe=timeframe,
            missing=missing,
            requires_human=requires_human,
            suggested=suggested,
        )

        return ExtractionResult(
            intent=intent,
            property_type=property_type,
            bedrooms=bedrooms,
            location=location,
            budget_min=budget_min,
            budget_max=budget_max,
            currency="NGN",
            timeframe=timeframe,
            customer=CustomerExtract(),
            missing_information=missing,
            confidence=confidence,
            requires_human=requires_human,
            handoff_reason=handoff_reason,
            suggested_next_question=suggested,
            response=response,
        )

    @staticmethod
    def _match_first(text: str, patterns: list[tuple[str, str]]) -> Optional[str]:
        for pattern, value in patterns:
            if re.search(pattern, text, re.IGNORECASE):
                return value
        return None

    @staticmethod
    def _extract_bedrooms(text: str) -> Optional[int]:
        m = re.search(r"(\d+)\s*[- ]?\s*(bed|bedroom|br|b/r)", text, re.IGNORECASE)
        if m:
            return int(m.group(1))
        m = re.search(r"\b(one|two|three|four|five)\s*(bed|bedroom)", text, re.IGNORECASE)
        if m:
            words = {"one": 1, "two": 2, "three": 3, "four": 4, "five": 5}
            return words.get(m.group(1).lower())
        return None

    def _extract_location(self, text: str) -> Optional[str]:
        for hint in self.LOCATION_HINTS:
            if hint in text:
                # Return title-cased common form
                return hint.title() if hint != "vi" else "Victoria Island"
        # "around X" / "in X"
        m = re.search(r"(?:around|in|at|near)\s+([a-zA-Z][a-zA-Z\s]{1,30}?)(?:\.|$|,|\s+with|\s+my|\s+budget)", text)
        if m:
            loc = m.group(1).strip().title()
            if len(loc) > 2:
                return loc
        return None

    @staticmethod
    def _extract_budget(text: str) -> tuple[Optional[float], Optional[float]]:
        """Parse Nigerian budget expressions: N80m, 80m, below 20m, around 50m, between 50m and 70m."""
        # between X and Y
        m = re.search(
            r"between\s+(?:n|₦)?\s*([\d,.]+)\s*(m|million)?\s+and\s+(?:n|₦)?\s*([\d,.]+)\s*(m|million)?",
            text,
            re.IGNORECASE,
        )
        if m:
            lo = ExtractionService._to_naira(m.group(1), m.group(2))
            hi = ExtractionService._to_naira(m.group(3), m.group(4))
            return lo, hi

        # below / under / max / up to
        m = re.search(
            r"(?:below|under|max|up\s+to|less\s+than)\s+(?:n|₦)?\s*([\d,.]+)\s*(m|million)?",
            text,
            re.IGNORECASE,
        )
        if m:
            val = ExtractionService._to_naira(m.group(1), m.group(2))
            return None, val

        # around / about / approximately
        m = re.search(
            r"(?:around|about|approx(?:imately)?)\s+(?:n|₦)?\s*([\d,.]+)\s*(m|million)?",
            text,
            re.IGNORECASE,
        )
        if m:
            val = ExtractionService._to_naira(m.group(1), m.group(2))
            if val:
                return val * 0.9, val * 1.1

        # plain N80m / ₦80 million / 80m
        m = re.search(
            r"(?:n|₦)\s*([\d,.]+)\s*(m|million)?|\b([\d,.]+)\s*(m|million)\b",
            text,
            re.IGNORECASE,
        )
        if m:
            num = m.group(1) or m.group(3)
            unit = m.group(2) or m.group(4)
            val = ExtractionService._to_naira(num, unit)
            return val, val

        return None, None

    @staticmethod
    def _to_naira(num_str: str, unit: Optional[str]) -> Optional[float]:
        try:
            num = float(num_str.replace(",", ""))
        except (ValueError, TypeError):
            return None
        if unit and unit.lower() in ("m", "million"):
            return num * 1_000_000
        # Heuristic: numbers like 80 in real-estate context often mean 80m
        if 1 <= num <= 500:
            return num * 1_000_000
        return num

    def _check_handoff(self, text: str) -> tuple[bool, Optional[str]]:
        for pattern in self.HANDOFF_PATTERNS:
            if re.search(pattern, text, re.IGNORECASE):
                return True, "Customer requested human assistance"
        return False, None

    @staticmethod
    def _estimate_confidence(
        intent, property_type, bedrooms, location, budget_min, budget_max, timeframe
    ) -> float:
        score = 0.3
        if intent and intent != "UNKNOWN":
            score += 0.15
        if property_type:
            score += 0.1
        if bedrooms is not None:
            score += 0.1
        if location:
            score += 0.15
        if budget_min is not None or budget_max is not None:
            score += 0.15
        if timeframe:
            score += 0.05
        return min(round(score, 2), 1.0)

    @staticmethod
    def _suggest_next_question(missing: list[str]) -> Optional[str]:
        priority = ["location", "budget", "intent", "property_type_or_bedrooms", "timeframe"]
        for key in priority:
            if key in missing:
                questions = {
                    "location": "Which area or location are you interested in?",
                    "budget": "What is your budget range (in Naira)?",
                    "intent": "Are you looking to buy, rent, or sell?",
                    "property_type_or_bedrooms": "What type of property (apartment, house, land…) and how many bedrooms?",
                    "timeframe": "When are you hoping to move or complete the purchase?",
                }
                return questions.get(key)
        return None

    @staticmethod
    def _build_response(
        *,
        intent,
        property_type,
        bedrooms,
        location,
        budget_min,
        budget_max,
        timeframe,
        missing,
        requires_human,
        suggested,
    ) -> str:
        if requires_human:
            return (
                "Of course — I’m connecting you with a PrimeHomes sales representative "
                "who will assist you shortly."
            )

        parts: list[str] = []
        known: list[str] = []

        if intent == "BUY":
            known.append("looking to buy")
        elif intent == "RENT":
            known.append("looking to rent")
        elif intent == "SELL":
            known.append("looking to sell")

        if bedrooms and property_type:
            known.append(f"a {bedrooms}-bedroom {property_type.lower()}")
        elif property_type:
            known.append(f"a {property_type.lower()}")
        elif bedrooms:
            known.append(f"a {bedrooms}-bedroom property")

        if location:
            known.append(f"in {location}")

        if budget_min and budget_max and budget_min != budget_max:
            known.append(
                f"with a budget of about ₦{budget_min/1_000_000:.0f}m–₦{budget_max/1_000_000:.0f}m"
            )
        elif budget_max and not budget_min:
            known.append(f"with a budget below ₦{budget_max/1_000_000:.0f}m")
        elif budget_min:
            known.append(f"with a budget around ₦{budget_min/1_000_000:.0f}m")

        if known:
            parts.append("Thanks! I understand you’re " + " ".join(known) + ".")
        else:
            parts.append("Thanks for reaching out to PrimeHomes Realty.")

        if suggested:
            parts.append(suggested)
        else:
            parts.append(
                "A sales representative will review your requirements and follow up shortly. "
                "Is there anything else you’d like to add?"
            )

        return " ".join(parts)
