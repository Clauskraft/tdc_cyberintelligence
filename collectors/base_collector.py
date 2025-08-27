"""
Base classes for collectors.

Collectors orchestrate the fetching of data from multiple sources and
normalize the results into a uniform structure.  Subclasses should
define specific collection strategies (e.g., retrieving only IOCs,
monitoring for ransomware leaks, etc.).
"""

from abc import ABC, abstractmethod
from typing import Iterable, Mapping, Any, Sequence

from ..sources.base_source import BaseSource


class BaseCollector(ABC):
    """Abstract base collector.

    A collector is responsible for orchestrating multiple sources.  It
    holds a list of source instances and returns combined results in
    its :meth:`collect` method.
    """

    def __init__(self, sources: Sequence[BaseSource]):
        self.sources = list(sources)

    @abstractmethod
    def collect(self) -> Iterable[Mapping[str, Any]]:
        """Collect data from all configured sources.

        Returns
        -------
        Iterable[Mapping[str, Any]]
            The combined indicators from each source.
        """
        raise NotImplementedError
