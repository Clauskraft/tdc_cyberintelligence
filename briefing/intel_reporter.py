"""
Generator for structured intelligence documents.

This module takes the output from analyzers and produces structured
documents (e.g. JSON or Markdown) that can be fed into a RAG model or
stored for later analysis.  The documents contain metadata such as
timestamp, source and confidence score.
"""

import json
from datetime import datetime
from typing import Iterable, Mapping, Any


class IntelReporter:
    """Produce structured intel documents."""

    def __init__(self, name: str = "intel_report"):
        self.name = name

    def generate(self, data: Iterable[Mapping[str, Any]]) -> str:
        """Return a JSON string representing the intel document.

        Parameters
        ----------
        data: Iterable[Mapping[str, Any]]
            Enriched indicator dictionaries.

        Returns
        -------
        str
            A JSON document containing a list of items and metadata.
        """
        doc = {
            "name": self.name,
            "generated_at": datetime.utcnow().isoformat() + "Z",
            "items": list(data),
        }
        return json.dumps(doc, indent=2)
