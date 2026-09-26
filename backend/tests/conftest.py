"""Pytest fixtures for backend tests."""

import pytest


@pytest.fixture
def anyio_backend():
    return "asyncio"
