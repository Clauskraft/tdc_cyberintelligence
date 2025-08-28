"""
Simple job scheduler integration.

This module shows how to use APScheduler to periodically collect
indicators and run analysers.  APScheduler allows you to configure
``interval`` or ``cron`` triggers【560569002111486†L62-L144】.  Replace the placeholders
with actual tasks and data persistence.
"""

from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
from datetime import datetime
from typing import List, Type

from .. import load_plugins
from ..collectors.ioc_collector import IOCCollector
from ..analyzers.correlation_analyzer import CorrelationAnalyzer
from ..analyzers.risk_scoring_analyzer import RiskScoringAnalyzer
from ..briefing.intel_reporter import IntelReporter


def job_collect_and_analyze():
    # Dynamically load source plugins and instantiate them.  In a real
    # environment you would pass credentials via a configuration file.
    sources: List[Type] = load_plugins()
    instances = []
    for src_cls in sources:
        try:
            # Pass dummy credentials; adjust as needed
            instance = None
            if src_cls.name == "misp":
                instance = src_cls(api_url="https://example.com", api_key="")
            elif src_cls.name == "otx":
                instance = src_cls(api_key="")
            elif src_cls.name == "shodan":
                instance = src_cls(api_key="")
            elif src_cls.name == "hibp":
                instance = src_cls(api_key="")
            elif src_cls.name == "cfcs":
                instance = src_cls()
            if instance:
                instances.append(instance)
        except Exception:
            continue
    # Collect indicators
    collector = IOCCollector(instances)
    collected = collector.collect()
    # Run analysers
    analyzers = [CorrelationAnalyzer(), RiskScoringAnalyzer()]
    data = collected
    for analyzer in analyzers:
        data = list(analyzer.analyze(data))
    # Generate intel report and store to file
    reporter = IntelReporter()
    output = reporter.generate(data)
    timestamp = datetime.utcnow().strftime("%Y%m%dT%H%M%SZ")
    output_path = f"reports/intel_report_{timestamp}.json"
    # Ensure directory exists
    import os
    os.makedirs("reports", exist_ok=True)
    with open(output_path, "w") as f:
        f.write(output)
    print(f"Generated report: {output_path}")


def start_scheduler():
    """Start a background scheduler that runs the job daily at 03:00 UTC."""
    scheduler = BackgroundScheduler()
    # Set up a daily trigger at 03:00
    trigger = CronTrigger(hour=3, minute=0)
    scheduler.add_job(job_collect_and_analyze, trigger)
    scheduler.start()
    print("Scheduler started. Press Ctrl+C to exit.")
    try:
        # Keep the scheduler running indefinitely
        import time
        while True:
            time.sleep(1)
    except (KeyboardInterrupt, SystemExit):
        scheduler.shutdown()


if __name__ == "__main__":
    start_scheduler()
