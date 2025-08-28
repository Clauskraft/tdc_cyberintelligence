"""
Streamlit dashboard for the cyber‑intelligence system.

This module defines a simple Streamlit app that displays indicators
collected and analysed by the system.  Streamlit turns Python scripts
into web apps without front‑end expertise.  To run this app, install
`streamlit` and execute ``streamlit run tdc_cyberintelligence/dashboard/streamlit_app.py``.
"""

import json
from pathlib import Path

import streamlit as st


def load_intel_docs(folder: Path):
    """Load previously generated intel documents from disk.

    Parameters
    ----------
    folder: Path
        Directory containing JSON documents produced by the intel reporter.

    Returns
    -------
    list[dict]
        Parsed JSON documents.
    """
    docs = []
    for json_file in folder.glob("*.json"):
        try:
            docs.append(json.loads(json_file.read_text()))
        except Exception:
            continue
    return docs


def main():
    st.title("TDC Erhverv Cyber‑Intelligence Dashboard")
    st.write("This dashboard displays indicators collected and analysed by the system.")
    # Select directory containing intel documents
    directory = st.sidebar.text_input("Intel documents directory", value="./reports")
    docs = load_intel_docs(Path(directory))
    if not docs:
        st.info("No intel documents found in the specified directory.")
        return
    # List available documents
    doc_names = [doc.get("generated_at", "unknown") for doc in docs]
    selected_idx = st.sidebar.selectbox("Select report", list(range(len(docs))), format_func=lambda i: doc_names[i])
    selected = docs[selected_idx]
    st.header(f"Report generated at {selected.get('generated_at')}")
    items = selected.get("items", [])
    if items:
        st.write("### Indicators")
        st.table([{key: item.get(key, '') for key in ["indicator", "type", "source", "confidence"]} for item in items])
    else:
        st.write("No indicators in this report.")


if __name__ == "__main__":
    main()
