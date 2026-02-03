"""### FILE: insight_mapping/utils.py

Utility functions for Insight Mapping EDA Engine.
"""

from __future__ import annotations

import json
import os
from pathlib import Path
from typing import Any, Dict, Iterable, List, Optional

import numpy as np
import pandas as pd


def safe_mkdir(path: Path) -> None:
    path.mkdir(parents=True, exist_ok=True)


def infer_dataset_name(file_path: Path) -> str:
    return file_path.stem


def is_numeric(series: pd.Series) -> bool:
    return pd.api.types.is_numeric_dtype(series)


def is_categorical(series: pd.Series, max_unique: int = 50) -> bool:
    if pd.api.types.is_bool_dtype(series) or pd.api.types.is_object_dtype(series):
        return True
    unique_count = series.nunique(dropna=True)
    return unique_count <= max_unique and not is_numeric(series)


def to_serializable(value: Any) -> Any:
    if isinstance(value, (np.integer, np.floating)):
        return value.item()
    if isinstance(value, (np.ndarray,)):
        return value.tolist()
    if isinstance(value, (pd.Timestamp,)):
        return value.isoformat()
    if pd.isna(value):
        return None
    return value


def save_json(data: Dict[str, Any], output_path: Path) -> None:
    with output_path.open("w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, default=to_serializable)


def limit_categories(series: pd.Series, max_categories: int = 20) -> pd.Series:
    if series.nunique(dropna=True) <= max_categories:
        return series
    top = series.value_counts(dropna=True).nlargest(max_categories).index
    return series.where(series.isin(top), other="Other")


def get_numeric_columns(df: pd.DataFrame) -> List[str]:
    return [col for col in df.columns if pd.api.types.is_numeric_dtype(df[col])]


def get_categorical_columns(df: pd.DataFrame) -> List[str]:
    return [col for col in df.columns if is_categorical(df[col])]
