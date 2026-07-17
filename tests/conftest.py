"""Shared helpers for the offline test suite."""

from collections.abc import Callable
from pathlib import Path

import pytest
from scrapy.http import HtmlResponse

FIXTURES_DIR = Path(__file__).parent / "fixtures"


@pytest.fixture
def response_from() -> Callable[..., HtmlResponse]:
    """Build an HtmlResponse from a saved HTML fixture (no network)."""

    def _make(fixture_name: str, url: str = "https://example.edu/") -> HtmlResponse:
        body = (FIXTURES_DIR / fixture_name).read_bytes()
        return HtmlResponse(url=url, body=body, encoding="utf-8")

    return _make
