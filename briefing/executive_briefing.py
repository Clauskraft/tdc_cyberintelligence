"""
Generator for executive briefings.

Executive briefings summarise the threat landscape and map it to
business impact.  They are intended for senior stakeholders and
therefore emphasise clarity and actionable recommendations.
"""

from datetime import datetime
from typing import Iterable, Mapping, Any


class ExecutiveBriefing:
    """Produce a textual executive briefing."""

    def __init__(self, title: str = "Executive Briefing"):
        self.title = title

    def generate(self, data: Iterable[Mapping[str, Any]]) -> str:
        """Return a plain‑text briefing.

        Parameters
        ----------
        data: Iterable[Mapping[str, Any]]
            Enriched indicator dictionaries.

        Returns
        -------
        str
            A formatted briefing summarising the indicators.
        """
        lines = [self.title, f"Generated: {datetime.utcnow().isoformat()}Z", ""]
        for item in data:
            indicator = item.get("indicator", "<unknown>")
            confidence = item.get("confidence", "?")
            lines.append(f"- Indicator: {indicator} (confidence {confidence})")
        return "\n".join(lines)
