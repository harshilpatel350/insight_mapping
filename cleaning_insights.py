"""### FILE: insight_mapping/cleaning_insights.py

Data cleaning and missing value analysis for Insight Mapping EDA Engine.
"""

from __future__ import annotations

from pathlib import Path
from typing import Any, Dict, List, Optional

import matplotlib.pyplot as plt
import pandas as pd

try:
    import missingno as msno
except Exception:  # pragma: no cover - optional
    msno = None


def missing_value_summary(df: pd.DataFrame) -> pd.DataFrame:
    """Return missing values summary for each column.
    
    Returns DataFrame with columns: missing_count, missing_percent, dtype
    """
    total_missing = df.isna().sum()
    percent_missing = (total_missing / len(df)) * 100
    summary = pd.DataFrame(
        {
            "missing_count": total_missing,
            "missing_percent": percent_missing.round(2),
            "dtype": df.dtypes.astype(str),
        }
    )
    return summary.sort_values(by="missing_percent", ascending=False)


def duplicate_rows_summary(df: pd.DataFrame) -> Dict[str, Any]:
    """Analyze duplicate rows in the DataFrame."""
    dup_count = int(df.duplicated().sum())
    dup_subset_counts: Dict[str, int] = {}
    for col in df.columns:
        dup_subset_counts[col] = int(df.duplicated(subset=[col]).sum())
    
    return {
        "duplicate_rows": dup_count,
        "duplicate_percent": round((dup_count / len(df)) * 100, 2) if len(df) else 0,
        "total_rows": len(df),
        "unique_rows": len(df) - dup_count,
        "duplicates_by_column": dup_subset_counts,
    }


def data_quality_score(df: pd.DataFrame) -> Dict[str, float]:
    """Calculate overall data quality score."""
    completeness = (1 - df.isna().sum().sum() / df.size) * 100
    uniqueness = (len(df) - df.duplicated().sum()) / len(df) * 100 if len(df) else 100
    return {
        "completeness_score": round(completeness, 2),
        "uniqueness_score": round(uniqueness, 2),
        "overall_score": round((completeness + uniqueness) / 2, 2),
    }


def plot_missing_values(df: pd.DataFrame, output_path: Path) -> Optional[Path]:
    """Generate missing values matrix plot using missingno if available."""
    if msno is None:
        return None
    output_path.parent.mkdir(parents=True, exist_ok=True)
    ax = msno.matrix(df, figsize=(12, 8), fontsize=10)
    fig = ax.get_figure()
    fig.savefig(output_path, bbox_inches="tight", dpi=150)
    plt.close(fig)
    return output_path


def plot_missing_bar(df: pd.DataFrame, output_path: Path) -> Optional[Path]:
    """Generate missing values bar chart using missingno."""
    if msno is None:
        return None
    output_path.parent.mkdir(parents=True, exist_ok=True)
    ax = msno.bar(df, figsize=(12, 6), fontsize=10)
    fig = ax.get_figure()
    fig.savefig(output_path, bbox_inches="tight", dpi=150)
    plt.close(fig)
    return output_path


def outlier_detection(df: pd.DataFrame, method: str = "iqr") -> Dict[str, Dict[str, Any]]:
    """Detect outliers in numeric columns using IQR or Z-score method.
    
    Args:
        df: Input DataFrame
        method: 'iqr' for Interquartile Range or 'zscore' for Z-score method
    
    Returns:
        Dictionary with outlier counts and bounds per column
    """
    import numpy as np
    results: Dict[str, Dict[str, Any]] = {}
    
    for col in df.select_dtypes(include=[np.number]).columns:
        series = df[col].dropna()
        if len(series) == 0:
            continue
            
        if method == "iqr":
            q1 = series.quantile(0.25)
            q3 = series.quantile(0.75)
            iqr = q3 - q1
            lower = q1 - 1.5 * iqr
            upper = q3 + 1.5 * iqr
        else:  # zscore
            mean = series.mean()
            std = series.std()
            lower = mean - 3 * std
            upper = mean + 3 * std
        
        outliers = series[(series < lower) | (series > upper)]
        results[col] = {
            "outlier_count": len(outliers),
            "outlier_percent": round(len(outliers) / len(series) * 100, 2),
            "lower_bound": round(float(lower), 4),
            "upper_bound": round(float(upper), 4),
        }
    
    return results
