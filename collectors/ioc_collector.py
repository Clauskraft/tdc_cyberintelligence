"""
Collector for indicators of compromise (IOCs).

This collector aggregates IOCs from any number of configured sources.
Each source must implement a :meth:`fetch` method returning an
iterable of indicators.  Duplicate indicators are removed based on
their ``indicator`` key.  Additional normalization and enrichment
could be performed here.
"""

from typing import Iterable, Mapping, Any, Sequence, Dict

from .base_collector import BaseCollector
from ..sources.base_source import BaseSource


class IOCCollector(BaseCollector):
    """Combine IOCs from multiple sources."""

    def __init__(self, sources: Sequence[BaseSource]):
        super().__init__(sources)

    def collect(self) -> Iterable[Mapping[str, Any]]:
        """Fetch and deduplicate IOCs from each source.

        Returns
        -------
        Iterable[Mapping[str, Any]]
            A list of unique indicator dictionaries.
        """
        seen: Dict[str, Mapping[str, Any]] = {}
        for source in self.sources:
            try:
                for item in source.fetch():
                    indicator = item.get("indicator")
                    if indicator is None:
                        continue
                    # Only keep the first occurrence
                    if indicator not in seen:
                        seen[indicator] = item
            except Exception as exc:
                # In a real implementation you may log the error or send a notification.
                continue
        return list(seen.values())
