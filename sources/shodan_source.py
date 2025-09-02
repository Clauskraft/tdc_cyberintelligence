"""
Shodan source plugin for the cyber intelligence platform.

This plugin leverages Shodan's REST API to retrieve data about
internet connected devices and services. The class follows the
``BaseSource`` interface expected by the system: a ``name`` attribute
identifies the source and a ``fetch()`` method returns a sequence of
indicator dictionaries.  Indicators may include open ports, service
banners or other metadata exposed by Shodan.  The plugin reads the
API key from the ``SHODAN_API_KEY`` environment variable by default.

For production deployments, it is recommended to store API keys in
Google Secret Manager and mount them as environment variables via
Cloud Run's ``--set-secrets`` flag.  See the deployment guide for
details.

Note: This implementation is intentionally simple and retrieves only
basic API information (``/api-info``) as a proof of concept. To make
practical use of Shodan, you can extend the ``fetch`` method to call
``/shodan/host/{ip}``, ``/shodan/search`` or other endpoints with
custom queries.  Be mindful of Shodan's rate limits and your
subscription plan.
"""

from __future__ import annotations

import os
import requests
from datetime import datetime
from typing import Iterable, Mapping, Any, List

from .base_source import BaseSource


class ShodanSource(BaseSource):
    """Fetch indicators of compromise from the Shodan REST API."""

    #: Unique name used by the plugin loader and API handler.
    name: str = "shodan"

    def __init__(self, api_key: str | None = None) -> None:
        # Read API key from argument or environment variable
        self.api_key = api_key or os.environ.get("SHODAN_API_KEY")

    def fetch(self) -> Iterable[Mapping[str, Any]]:
        """Retrieve data from Shodan.

        Returns a list of indicator dictionaries.  If no API key is
        configured or an error occurs, an empty list is returned.

        Each dictionary should at minimum contain ``indicator``, ``type``,
        ``source``, ``confidence`` and ``timestamp`` keys.  Additional
        metadata may be included under ``data``.
        """
        indicators: List[Mapping[str, Any]] = []
        if not self.api_key:
            # Without a key, we can't hit the API – return no data.
            return indicators

        try:
            # Simple call to the API info endpoint. This endpoint
            # returns account information and query quotas. Replace
            # this with more specific queries (e.g. shodan/search) as
            # needed for your use case.
            url = f"https://api.shodan.io/api-info?key={self.api_key}"
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            data = response.json()

            # Create a single indicator summarising the account info.
            indicators.append({
                "indicator": "shodan_account",
                "type": "stat",
                "source": self.name,
                "confidence": "medium",
                "timestamp": datetime.utcnow(),
                "data": data,
            })
        except Exception:
            # In production, consider logging the error via your
            # notification mechanism (e.g. Slack/Teams). Here we
            # silently ignore failures and return an empty list.
            return []

        return indicators
