"""### FILE: insight_mapping/main.py

Insight Mapping - Automated Exploratory Data Analysis Engine
A production-quality EDA tool for tabular datasets.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path
from typing import Any, Dict, Optional

import pandas as pd

from cleaning_insights import duplicate_rows_summary, missing_value_summary, plot_missing_values
from correlation_analysis import categorical_correlation, numeric_correlation
from data_loader import load_data
from descriptive_stats import describe_dataframe
from logger_config import setup_logging
from report_generator import generate_html_report, generate_json_report
from visualization import (
    bar_charts,
    boxplots,
    correlation_heatmap,
    histograms,
    interactive_scatter,
    pairplot,
    violin_plots,
)

try:
    from ydata_profiling import ProfileReport
except Exception:  # pragma: no cover - optional
    ProfileReport = None

try:
    import sweetviz as sv
except Exception:  # pragma: no cover - optional
    sv = None


def build_report(df: pd.DataFrame, output_dir: Path, logger) -> Dict[str, Any]:
    output_dir.mkdir(parents=True, exist_ok=True)
    visuals_dir = output_dir / "visuals"

    dataset_summary = {
        "rows": int(len(df)),
        "columns": int(df.shape[1]),
        "dtypes": df.dtypes.astype(str).to_dict(),
    }

    missing_summary_df = missing_value_summary(df)
    duplicates = duplicate_rows_summary(df)
    descriptive_stats = describe_dataframe(df)

    numeric_corr = numeric_correlation(df)
    categorical_corr = categorical_correlation(df)

    visuals = {
        "Histograms": [str(p) for p in histograms(df, visuals_dir)],
        "Boxplots": [str(p) for p in boxplots(df, visuals_dir)],
        "Violin Plots": [str(p) for p in violin_plots(df, visuals_dir)],
        "Pairplot": [str(p) for p in [pairplot(df, visuals_dir)] if p],
        "Bar Charts": [str(p) for p in bar_charts(df, visuals_dir)],
        "Numeric Correlation Heatmap": [
            str(p)
            for p in [correlation_heatmap(numeric_corr, visuals_dir, "numeric")]
            if p
        ],
        "Categorical Correlation Heatmap": [
            str(p)
            for p in [correlation_heatmap(categorical_corr, visuals_dir, "categorical")]
            if p
        ],
        "Interactive Scatter": [
            str(p) for p in [interactive_scatter(df, visuals_dir)] if p
        ],
        "Missing Value Matrix": [
            str(p)
            for p in [plot_missing_values(df, visuals_dir / "missing_matrix.png")]
            if p
        ],
    }

    report = {
        "dataset_summary": dataset_summary,
        "missing_values": missing_summary_df.to_dict(),
        "duplicates": duplicates,
        "descriptive_stats": descriptive_stats,
        "correlation": {
            "numeric": numeric_corr.to_dict(),
            "categorical": categorical_corr.to_dict(),
        },
        "visuals": visuals,
    }

    logger.info("Report data built successfully")
    return report


def generate_profile_reports(df: pd.DataFrame, output_dir: Path, logger) -> None:
    """Generate optional extended profiling reports."""
    if ProfileReport is not None:
        try:
            profile = ProfileReport(df, title="Insight Mapping Profiling Report", explorative=True)
            profile.to_file(output_dir / "profiling_report.html")
            logger.info("Generated ydata-profiling report")
        except Exception as e:
            logger.warning("Failed to generate ydata-profiling report: %s", e)

    if sv is not None:
        try:
            report = sv.analyze(df)
            report.show_html(str(output_dir / "sweetviz_report.html"), open_browser=False)
            logger.info("Generated Sweetviz report")
        except Exception as e:
            logger.warning("Failed to generate Sweetviz report: %s", e)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        prog="insight-mapping",
        description="Insight Mapping - Automated Exploratory Data Analysis Engine",
        epilog="Example: python main.py data.csv --output reports --profile",
    )
    parser.add_argument("input", type=str, help="Path to dataset (CSV, Excel, JSON)")
    parser.add_argument(
        "--output",
        "-o",
        type=str,
        default="reports",
        help="Output directory for reports (default: reports)",
    )
    parser.add_argument(
        "--profile",
        "-p",
        action="store_true",
        help="Generate ydata-profiling and Sweetviz reports if available",
    )
    parser.add_argument(
        "--verbose",
        "-v",
        action="store_true",
        help="Enable verbose/debug logging",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    input_path = Path(args.input).expanduser().resolve()
    output_dir = Path(args.output).expanduser().resolve()
    log_dir = output_dir / "logs"

    import logging
    log_level = logging.DEBUG if args.verbose else logging.INFO
    logger = setup_logging(log_dir, log_level)
    logger.info("Starting Insight Mapping EDA Engine")

    try:
        df, file_type = load_data(input_path)
        logger.info("Loaded %s dataset with shape %s", file_type, df.shape)
    except FileNotFoundError as e:
        logger.error("File not found: %s", input_path)
        sys.exit(1)
    except ValueError as e:
        logger.error("Unsupported file format: %s", e)
        sys.exit(1)

    report = build_report(df, output_dir, logger)
    json_path = generate_json_report(report, output_dir / "report.json")
    html_path = generate_html_report(report, output_dir / "report.html")

    logger.info("JSON report saved to %s", json_path)
    logger.info("HTML report saved to %s", html_path)

    if args.profile:
        generate_profile_reports(df, output_dir, logger)

    logger.info("Insight Mapping EDA complete")


if __name__ == "__main__":
    main()
