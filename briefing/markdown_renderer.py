"""
Renderers for turning analysis results into Markdown.

This simple renderer converts a list of enriched indicators into a
Markdown table.  More sophisticated renderers could include plots
generated with matplotlib or plotly.
"""

from typing import Iterable, Mapping, Any


class MarkdownRenderer:
    """Render analysis results as Markdown."""

    def render_table(self, data: Iterable[Mapping[str, Any]]) -> str:
        """Return a Markdown table summarising the indicators.

        Parameters
        ----------
        data: Iterable[Mapping[str, Any]]
            Enriched indicator dictionaries.

        Returns
        -------
        str
            A string containing a Markdown table.
        """
        headers = ["Indicator", "Type", "Source", "Confidence"]
        lines = ["| " + " | ".join(headers) + " |", "| " + " | ".join(["---"] * len(headers)) + " |"]
        for item in data:
            lines.append(
                f"| {item.get('indicator', '')} | {item.get('type', '')} | {item.get('source', '')} | {item.get('confidence', '')} |"
            )
        return "\n".join(lines)
