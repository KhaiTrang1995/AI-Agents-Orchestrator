"""Offline mode detection utilities."""

from __future__ import annotations

import time

import httpx


class OfflineDetector:
    """Detect network availability with cached checks."""

    def __init__(
        self,
        check_interval: int = 60,
        connectivity_url: str = "https://api.anthropic.com",
        timeout_seconds: float = 3.0,
    ) -> None:
        self.check_interval = check_interval
        self.connectivity_url = connectivity_url
        self.timeout_seconds = timeout_seconds
        self._is_offline: bool | None = None
        self._last_check_monotonic: float = 0.0

    def is_offline(self, force_refresh: bool = False) -> bool:
        """Return current offline status using cached connectivity checks."""
        now = time.monotonic()
        cache_is_fresh = (now - self._last_check_monotonic) < self.check_interval

        if force_refresh or self._is_offline is None or not cache_is_fresh:
            self._is_offline = not self._check_connectivity()
            self._last_check_monotonic = now

        return self._is_offline

    def _check_connectivity(self) -> bool:
        """Perform a lightweight online check."""
        try:
            response = httpx.head(self.connectivity_url, timeout=self.timeout_seconds)
            return response.status_code < 500
        except Exception:
            return False
