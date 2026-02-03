"""### FILE: insight_mapping/report_generator.py

Report generation for Insight Mapping EDA Engine.
Generates HTML and JSON reports from analysis results.
"""

from __future__ import annotations

import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional

import pandas as pd

from utils import save_json


def generate_json_report(report: Dict[str, Any], output_path: Path) -> Path:
    """Generate JSON report from analysis data."""
    output_path.parent.mkdir(parents=True, exist_ok=True)
    report["generated_at"] = datetime.datetime.now().isoformat()
    report["engine"] = "Insight Mapping v1.0"
    save_json(report, output_path)
    return output_path


def _html_section(title: str, body: str) -> str:
    return f"<section><h2>{title}</h2>{body}</section>"


def _table_from_df(df: pd.DataFrame) -> str:
    return df.to_html(classes="table", border=0)


def generate_html_report(report: Dict[str, Any], output_path: Path) -> Path:
    """Generate comprehensive HTML report with visualizations."""
    output_path.parent.mkdir(parents=True, exist_ok=True)
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    stats_table = pd.DataFrame(report.get("missing_values", {}))
    stats_html = _table_from_df(stats_table) if not stats_table.empty else "<p>No data.</p>"

    visuals = report.get("visuals", {})
    visual_html = ""
    for title, paths in visuals.items():
        if not paths:
            continue
        visual_html += f"<h3>{title}</h3>"
        for path in paths:
            if str(path).endswith(".html"):
                visual_html += f"<iframe src='{path}' style='width:100%;height:500px;'></iframe>"
            else:
                visual_html += f"<img src='{path}' style='max-width:100%;'/>"

    content = f"""
    <html>
    <head>
        <title>Insight Mapping EDA Report</title>
        <style>
            :root {{ --primary: #2563eb; --bg: #f8fafc; --card: #ffffff; }}
            body {{ font-family: 'Segoe UI', Arial, sans-serif; margin: 0; padding: 2rem; background: var(--bg); color: #1e293b; }}
            header {{ text-align: center; margin-bottom: 2rem; }}
            header h1 {{ color: var(--primary); margin-bottom: 0.5rem; }}
            .timestamp {{ color: #64748b; font-size: 0.9rem; }}
            nav {{ text-align: center; margin-bottom: 2rem; padding: 1rem; background: var(--card); border-radius: 8px; box-shadow: 0 1px 3px rgba(0,0,0,0.1); }}
            nav a {{ color: var(--primary); text-decoration: none; padding: 0.5rem; }}
            nav a:hover {{ text-decoration: underline; }}
            .table {{ border-collapse: collapse; width: 100%; }}
            .table th, .table td {{ border: 1px solid #e2e8f0; padding: 10px; text-align: left; }}
            .table th {{ background-color: var(--primary); color: white; }}
            .table tr:nth-child(even) {{ background-color: #f1f5f9; }}
            section {{ background: var(--card); padding: 1.5rem; margin-bottom: 1.5rem; border-radius: 8px; box-shadow: 0 1px 3px rgba(0,0,0,0.1); }}
            section h2 {{ color: var(--primary); border-bottom: 2px solid var(--primary); padding-bottom: 0.5rem; }}
            footer {{ text-align: center; color: #64748b; margin-top: 2rem; padding: 1rem; }}
            img {{ border-radius: 8px; margin: 0.5rem 0; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }}
        </style>
    </head>
    <body>
        <header>
            <h1>Insight Mapping EDA Report</h1>
            <p class="timestamp">Generated: {timestamp}</p>
        </header>
        <nav>
            <a href="#summary">Summary</a> |
            <a href="#missing">Missing Values</a> |
            <a href="#duplicates">Duplicates</a> |
            <a href="#stats">Statistics</a> |
            <a href="#correlation">Correlation</a> |
            <a href="#visuals">Visualizations</a>
        </nav>
        <div id="summary">{_html_section("Dataset Summary", f"<pre>{report.get('dataset_summary')}</pre>")}</div>
        <div id="missing">{_html_section("Missing Values", stats_html)}</div>
        <div id="duplicates">{_html_section("Duplicate Rows", f"<pre>{report.get('duplicates')}</pre>")}</div>
        <div id="stats">{_html_section("Descriptive Statistics", f"<pre>{report.get('descriptive_stats')}</pre>")}</div>
        <div id="correlation">{_html_section("Correlation", f"<pre>{report.get('correlation')}</pre>")}</div>
        <div id="visuals">{_html_section("Visualizations", visual_html)}</div>
        <footer><p>Powered by Insight Mapping v1.0</p></footer>
    </body>
    </html>
    """

    output_path.write_text(content, encoding="utf-8")
    return output_path
