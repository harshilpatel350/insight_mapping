"""### FILE: insight_mapping/descriptive_stats.py

Descriptive statistics module for Insight Mapping EDA Engine.
"""

from __future__ import annotations

from typing import Any, Dict, List

import numpy as np
import pandas as pd


def describe_dataframe(df: pd.DataFrame) -> Dict[str, Any]:
    """Return comprehensive descriptive statistics for all columns."""
    describe_all = df.describe(include="all")
    per_column: Dict[str, Dict[str, Any]] = {}
    
    for col in df.columns:
        series = df[col]
        col_stats: Dict[str, Any] = {
            "dtype": str(series.dtype),
            "unique": int(series.nunique(dropna=True)),
            "missing": int(series.isna().sum()),
            "missing_percent": round(series.isna().mean() * 100, 2),
        }
        
        if pd.api.types.is_numeric_dtype(series):
            col_stats.update({
                "mean": float(series.mean()) if not series.isna().all() else None,
                "median": float(series.median()) if not series.isna().all() else None,
                "std": float(series.std()) if not series.isna().all() else None,
                "min": float(series.min()) if not series.isna().all() else None,
                "max": float(series.max()) if not series.isna().all() else None,
                "skewness": float(series.skew()) if not series.isna().all() else None,
                "kurtosis": float(series.kurtosis()) if not series.isna().all() else None,
                "zeros": int((series == 0).sum()),
                "negatives": int((series < 0).sum()),
            })
        else:
            col_stats.update({
                "most_common": series.mode().iloc[0] if not series.mode().empty else None,
                "most_common_count": int(series.value_counts().iloc[0]) if series.nunique() > 0 else 0,
            })
        
        per_column[col] = col_stats
    
    return {
        "summary": describe_all.to_dict(),
        "columns": per_column,
        "shape": {"rows": df.shape[0], "columns": df.shape[1]},
        "memory_usage_mb": round(df.memory_usage(deep=True).sum() / 1024 / 1024, 4),
    }
