"""
Plugin for retrieving indicators from AlienVault OTX.

OTX is a community‑driven feed that provides IOCs and TTPs【380051382662935†L110-L113】.  Replace
the placeholder code in :meth:`fetch` with calls to the OTX API.
"""

from typing import Iterable, Mapping, Any

from .base_source import BaseSource


class OtxSource(BaseSource):
    """Threat intelligence source for AlienVault OTX."""

    name = "otx"

    def __init__(self, api_key: str):
        self.api_key = api_key

    def fetch(self) -> Iterable[Mapping[str, Any]]:
        """Fetch indicators from the OTX API.

        In a real implementation this method would call the OTX
        ``/pulses/subscribed`` endpoint and parse the IOCs contained in
        the returned pulses.  For now it yields an empty list.
        """
        return []
