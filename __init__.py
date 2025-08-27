"""
Top‑level package for the TDC Erhverv cyber‑intelligence system.

This package exposes convenience functions to load source plugins,
collect indicators of compromise and analyse them.  The system is
organised into three layers (Data Collection, Threat Analysis and
Reporting) as described in the accompanying architecture report.

NOTE: This is a skeleton implementation intended to illustrate the
overall structure.  Actual integrations with feeds such as MISP,
OTX or Shodan should be implemented in the corresponding modules
under the ``sources`` package.
"""

from importlib import import_module
from pathlib import Path
from typing import List, Type

from .sources.base_source import BaseSource
from .collectors.ioc_collector import IOCCollector
from .analyzers.base_analyzer import BaseAnalyzer


def load_plugins() -> List[Type[BaseSource]]:
    """Dynamically load all source plugins in the ``sources`` package.

    This function inspects the ``sources`` directory for modules that
    define subclasses of :class:`~tdc_cyberintelligence.sources.base_source.BaseSource`.
    New feed integrations can be added simply by dropping a module into
    ``tdc_cyberintelligence/sources`` that defines a class inheriting
    ``BaseSource`` and declaring a ``name`` attribute.

    Returns
    -------
    List[Type[BaseSource]]
        A list of source classes that have been discovered.
    """
    sources_path = Path(__file__).resolve().parent / "sources"
    plugins: List[Type[BaseSource]] = []
    for module_file in sources_path.iterdir():
        if module_file.name.startswith("__") or not module_file.suffix == ".py":
            continue
        module_name = f"{__name__}.sources.{module_file.stem}"
        module = import_module(module_name)
        for attr in dir(module):
            obj = getattr(module, attr)
            if isinstance(obj, type) and issubclass(obj, BaseSource) and obj is not BaseSource:
                plugins.append(obj)
    return plugins


__all__ = ["load_plugins", "IOCCollector", "BaseAnalyzer"]
