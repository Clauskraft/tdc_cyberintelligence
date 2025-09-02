"""
Spiderfoot source plugin for the cyber intelligence platform.

Spiderfoot is a comprehensive OSINT automation framework that can
perform reconnaissance on IPs, domains, e mails and more by querying
multiple data sources.  This plugin integrates Spiderfoot via its
HTTP API.  It assumes a running instance of Spiderfoot (either
open‟source or Spiderfoot HX) and uses an API token for
authentication.

Configuration is read from the following environment variables by
default:

* ``SPIDERFOOT_URL`` – Base URL of the Spiderfoot API (e.g. ``http://localhost:5001``)
* ``SPIDERFOOT_API_KEY`` – API key to authenticate requests

When deployed on Cloud Run, these values should be provided via
Secret Manager and referenced in ``--set-secrets`` or set directly
as environment variables.  See the deployment guide for details.

This implementation is intentionally minimal: it queries the
``/scan`` endpoint to list existing scans and returns the most recent
scan status as an indicator.  You may extend ``fetch()`` to
automatically launch new scans or pull full results via the
``/scan/<scan_id>/data`` endpoint.
"""

from __future__ import annotations

import os
import requests
from datetime import datetime
from typing import Iterable, Mapping, Any, List

from .base_source import BaseSource


class SpiderfootSource(BaseSource):
    """Fetch OSINT indicators from a Spiderfoot instance."""

    #: Unique name used by the plugin loader and API handler.
    name: str = "spiderfoot"

    def __init__(self, api_url: str | None = None, api_key: str | None = None) -> None:
        self.api_url = api_url or os.environ.get("SPIDERFOOT_URL")
        self.api_key = api_key or os.environ.get("SPIDERFOOT_API_KEY")

    def fetch(self) -> Iterable[Mapping[str, Any]]:
        """Retrieve data from Spiderfoot.

        Returns a list of indicator dictionaries.  If misconfigured or
        on error, an empty list is returned.
        """
        indicators: List[Mapping[str, Any]] = []
        if not self.api_url or not self.api_key:
            return indicators

        try:
            # Fetch list of scans.  Spiderfoot HX uses /api/v1, while
            # open source Spiderfoot typically exposes /scan. Adjust
            # accordingly if your version differs.
            endpoint = self.api_url.rstrip("/") + "/scan"
            headers = {"X-Api-Key": self.api_key}
            resp = requests.get(endpoint, headers=headers, timeout=10)
            resp.raise_for_status()
            scans = resp.json()

            # Use the most recent scan to create an indicator.  For
            # demonstration purposes we only return the summary of the
            # latest scan.  Further logic could include iterating over
            # scans and pulling detailed results.
            if isinstance(scans, list) and scans:
                latest = scans[-1]
                indicators.append({
                    "indicator": latest.get("scan_id", "spiderfoot_scan"),
                    "type": "osint",
                    "source": self.name,
                    "confidence": "low",
                    "timestamp": datetime.utcnow(),
                    "data": latest,
                })
        except Exception:
            return []

        return indicators
