"""AI provider adapter.

AI output is untrusted until schema-validated.
See docs/AI_SPECIFICATION.md for the extraction contract.
"""

from typing import Any


class AIProvider:
    """Thin adapter around the configured LLM provider."""

    async def extract(self, message: str, context: dict[str, Any] | None = None) -> dict[str, Any]:
        """
        Call the model with the extraction prompt and return raw structured output.
        Caller MUST validate against the Pydantic extraction schema.
        """
        raise NotImplementedError("AI extraction adapter not yet implemented")

    async def generate_response(
        self, lead_facts: dict[str, Any], conversation_history: list[dict[str, Any]]
    ) -> str:
        """Generate a grounded customer response."""
        raise NotImplementedError("AI response generation not yet implemented")
