"""
Base classes for analysis modules.

Analyzers take collected data and produce further insights such as
correlations, risk scores, compliance mapping or anomaly detections.
"""

from abc import ABC, abstractmethod
from typing import Iterable, Mapping, Any


class BaseAnalyzer(ABC):
    """Abstract analyzer class."""

    @abstractmethod
    def analyze(self, data: Iterable[Mapping[str, Any]]) -> Iterable[Mapping[str, Any]]:
        """Analyze the given data and yield annotated results.

        Parameters
        ----------
        data: Iterable[Mapping[str, Any]]
            Raw indicators or events to analyze.

        Returns
        -------
        Iterable[Mapping[str, Any]]
            A stream of enriched or filtered items.
        """
        raise NotImplementedError
