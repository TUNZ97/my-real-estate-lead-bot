"""n8n webhook / event client.

n8n orchestrates; this client emits events or calls workflow webhooks.
"""

from typing import Any

import httpx

from app.config import settings


class N8NClient:
    def __init__(self, base_url: str | None = None):
        self.base_url = (base_url or settings.N8N_BASE_URL).rstrip("/")

    async def trigger_workflow(self, webhook_path: str, payload: dict[str, Any]) -> dict[str, Any]:
        """POST to an n8n webhook."""
        url = f"{self.base_url}/{webhook_path.lstrip('/')}"
        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.post(url, json=payload)
            response.raise_for_status()
            return response.json() if response.content else {}
