
Simple FastAPI application to expose parts of the cyber‑intelligence system.

Endpoints:

* ``GET /health`` – basic health check.
* ``GET /reports/latest`` – return the latest generated intel report as JSON.
* ``POST /collect-and-analyze`` – trigger collection and analysis on demand and return the result.

This API uses the existing collectors and analyzers defined in the package.  To
run the app, install the required dependencies and execute::

    uvicorn tdc_cyberintelligence.api:app --host 0.0.0.0 --port 8080

Cloud Run will automatically supply the environment variable ``PORT``.  The
Dockerfile included in the repository sets the command appropriately.
"""

import json
import os
from datetime import datetime
from pathlib import Path
from typing import List, Type

from fastapi import FastAPI
from fastapi.responses import JSONResponse

from . import load_plugins
from .collectors.ioc_collector import IOCCollector
from .analyzers.correlation_analyzer import CorrelationAnalyzer
from .analyzers.risk_scoring_analyzer import RiskScoringAnalyzer
from .briefing.intel_reporter import IntelReporter


app = FastAPI(title="Cyber Intelligence API")


@app.get("/health")
def health_check():
    return {"status": "ok"}


@app.post("/collect-and-analyze")
def collect_and_analyze():
    """Trigger immediate collection and analysis and return the results."""
    # Load source plugins dynamically
    sources: List[Type] = load_plugins()
    instances = []
    for src_cls in sources:
        try:
            instance = None
            if src_cls.name == "misp":
             instance = src_cls()
            elif src_cls.name == "otx":
                instance = src_cls(api_key=os.environ.get("OTX_KEY", ""))
            elif src_cls.name == "shodan":
                instance = src_cls(api_key=os.environ.get("SHODAN_KEY", ""))
            elif src_cls.name == "hibp":
                instance = src_cls(api_key=os.environ.get("HIBP_KEY", ""))
            elif src_cls.name == "cfcs":
                instance = src_cls()
            if instance:
                instances.append(instance)
        except Exception:
            continue
    # Collect and analyse
    collector = IOCCollector(instances)
    data = collector.collect()
    analyzers = [CorrelationAnalyzer(), RiskScoringAnalyzer()]
    for analyzer in analyzers:
        data = list(analyzer.analyze(data))
    # Write to file and return JSON
    reporter = IntelReporter()
    output = reporter.generate(data)
    reports_dir = Path(os.environ.get("REPORTS_DIR", "reports"))
    reports_dir.mkdir(parents=True, exist_ok=True)
   
        # Write indicators to BigQuery if environment variables are set
    bq_project = os.environ.get("BQ_PROJECT")
    bq_dataset = os.environ.get("BQ_DATASET")
    bq_table = os.environ.get("BQ_TABLE")
    if bq_project and bq_dataset and bq_table:
        try:
            bq_writer = BigQueryWriter(bq_project, bq_dataset, bq_table)
            bq_writer.write_indicators(data)
        except Exception:
            # Ignore BigQuery errors to avoid failing the entire request
            pass
timestamp = datetime.utcnow().strftime("%Y%m%dT%H%M%SZ")
    path = reports_dir / f"intel_report_{timestamp}.json"
    path.write_text(output)
    return JSONResponse(content=json.loads(output))


@app.get("/reports/latest")
def get_latest_report():
    """Return the most recently generated intel report."""
    reports_dir = Path(os.environ.get("REPORTS_DIR", "reports"))
    if not reports_dir.exists():
        return JSONResponse(content={"error": "No reports available"}, status_code=404)
    reports = sorted(reports_dir.glob("intel_report_*.json"), reverse=True)
    if not reports:
        return JSONResponse(content={"error": "No reports available"}, status_code=404)
    latest = reports[0]
    try:
        data = json.loads(latest.read_text())
        return JSONResponse(content=data)
    except Exception:
        return JSONResponse(content={"error": "Failed to read report"}, status_code=500)
