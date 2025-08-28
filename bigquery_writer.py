"""
BigQuery writer module for TDC cyber intelligence platform.

This module provides a `BigQueryWriter` class that writes indicators of
compromise (IOCs) into a BigQuery table. It expects the BigQuery client
library to be installed and credentials to be available in the environment.
"""

from typing import Iterable, Mapping, Any
import os

try:
    from google.cloud import bigquery  # type: ignore
except ImportError:
    bigquery = None  # type: ignore

class BigQueryWriter:
    """Write indicator dictionaries into a BigQuery table."""

    def __init__(self, project_id: str, dataset_id: str, table_id: str) -> None:
        if bigquery is None:
            raise ImportError("google-cloud-bigquery is not installed.")
        self.project_id = project_id
        self.dataset_id = dataset_id
        self.table_id = table_id
        # Initialize BigQuery client; uses default credentials from env
        self.client = bigquery.Client(project=self.project_id)

    def write_indicators(self, indicators: Iterable[Mapping[str, Any]]) -> None:
        """Insert a collection of indicator dicts into BigQuery.

        Parameters
        ----------
        indicators : Iterable[Mapping[str, Any]]
            Each mapping should contain at least the keys: indicator, type,
            source, confidence, timestamp.

        Raises
        ------
        RuntimeError
            If any insertion errors occur.
        """
        table_ref = f"{self.project_id}.{self.dataset_id}.{self.table_id}"
        rows_to_insert = []
        for item in indicators:
            # Build row dictionary; missing fields are allowed to be None
            row = {
                "indicator": item.get("indicator"),
                "type": item.get("type"),
                "source": item.get("source"),
                "confidence": item.get("confidence"),
                "timestamp": item.get("timestamp"),
            }
            rows_to_insert.append(row)
        if not rows_to_insert:
            return
        errors = self.client.insert_rows_json(table_ref, rows_to_insert)
        if errors:
            raise RuntimeError(f"BigQuery insertion errors: {errors}")
