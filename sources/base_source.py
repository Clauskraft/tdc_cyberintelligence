"""
Abstract base class for threat intelligence sources.

Implementations of this class should override the :meth:`fetch` method
to retrieve indicators of compromise (IOCs), vulnerabilities or other
relevant data.  Each subclass must define a class attribute ``name``
with a unique string identifying the source.
"""

from abc import ABC, abstractmethod
from typing import Any, Iterable, Mapping


class BaseSource(ABC):
    """Base class for feed sources.

    Concrete subclasses must implement :meth:`fetch` to return an
    iterable of indicator dictionaries.  Individual feeds can carry
    arbitrary fields, but a minimum set of keys (e.g., ``indicator``,
    ``type``, ``confidence``) is recommended for interoperability.
    """

    #: Human‑readable name of the source.  Subclasses must override this.
    name: str = "undefined"

    @abstractmethod
    def fetch(self) -> Iterable[Mapping[str, Any]]:
        """Return an iterable of indicators from this source.

        Subclasses should perform any required API calls or scraping
        inside this method.  In this skeleton implementation, the
        method simply yields an empty list.

        Returns
        -------
        Iterable[Mapping[str, Any]]
            An iterable of dictionaries describing indicators.
        """
        raise NotImplementedError
