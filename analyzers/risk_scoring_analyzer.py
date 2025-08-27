"""
Analyzer that assigns a confidence or risk score to indicators.

The risk score reflects the trustworthiness of the source and the
severity of the indicator.  Sources such as MISP or OTX can have
higher default confidence because they provide structured data【380051382662935†L65-L113】.
"""

from typing import Iterable, Mapping, Any

from .base_analyzer import BaseAnalyzer


class RiskScoringAnalyzer(BaseAnalyzer):
    """Assigns a confidence score to each indicator."""

    DEFAULT_SCORES = {
        "misp": 0.9,
        "otx": 0.7,
        "shodan": 0.6,
        "hibp": 0.8,
        "cfcs": 0.7,
    }

    def analyze(self, data: Iterable[Mapping[str, Any]]) -> Iterable[Mapping[str, Any]]:
        for item in data:
            item = dict(item)
            source_name = item.get("source")
            score = self.DEFAULT_SCORES.get(source_name, 0.5)
            item["confidence"] = score
            yield item
