"""n8n webhook / event client.

n8n orchestrates; this client emits events or calls workflow webhooks.
Failures are non-blocking so the customer always gets a response.
"""

from typing import Any

import httpx

from app.config import settings


class N8NClient:
    def __init__(self, base_url: str | None = None):
        self.base_url = (base_url or settings.N8N_BASE_URL).rstrip("/")

    async def trigger_workflow(self, webhook_path: str, payload: dict[str, Any]) -> dict[str, Any]:
        """POST to an n8n webhook. Raises on network/HTTP errors."""
        path = webhook_path.lstrip("/")
        url = f"{self.base_url}/{path}"
        async with httpx.AsyncClient(timeout=5.0) as client:
            response = await client.post(url, json=payload)
            response.raise_for_status()
            if response.content:
                try:
                    return response.json()
                except Exception:
                    return {}
            return {}
