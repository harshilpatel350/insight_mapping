"""### FILE: insight_mapping/correlation_analysis.py

Correlation analysis module for Insight Mapping EDA Engine.
Supports both numeric (Pearson) and categorical (Cramér's V) correlations.
"""

from __future__ import annotations

from typing import Dict, List, Tuple

import numpy as np
import pandas as pd

from utils import get_categorical_columns, get_numeric_columns


def numeric_correlation(df: pd.DataFrame) -> pd.DataFrame:
    numeric_cols = get_numeric_columns(df)
    if not numeric_cols:
        return pd.DataFrame()
    return df[numeric_cols].corr()


def cramers_v(confusion_matrix: pd.DataFrame) -> float:
    chi2 = ss_chi2(confusion_matrix)
    n = confusion_matrix.to_numpy().sum()
    if n == 0:
        return 0.0
    phi2 = chi2 / n
    r, k = confusion_matrix.shape
    phi2corr = max(0, phi2 - ((k - 1) * (r - 1)) / (n - 1)) if n > 1 else 0
    rcorr = r - ((r - 1) ** 2) / (n - 1) if n > 1 else 0
    kcorr = k - ((k - 1) ** 2) / (n - 1) if n > 1 else 0
    denom = min((kcorr - 1), (rcorr - 1))
    if denom <= 0:
        return 0.0
    return float(np.sqrt(phi2corr / denom))


def ss_chi2(confusion_matrix: pd.DataFrame) -> float:
    observed = confusion_matrix.to_numpy()
    if observed.size == 0:
        return 0.0
    row_sum = observed.sum(axis=1, keepdims=True)
    col_sum = observed.sum(axis=0, keepdims=True)
    total = observed.sum()
    expected = row_sum @ col_sum / total if total else 0
    with np.errstate(divide="ignore", invalid="ignore"):
        chi2 = ((observed - expected) ** 2 / expected)
        chi2 = np.nan_to_num(chi2).sum()
    return float(chi2)


def categorical_correlation(df: pd.DataFrame) -> pd.DataFrame:
    cat_cols = get_categorical_columns(df)
    if len(cat_cols) < 2:
        return pd.DataFrame()

    matrix = pd.DataFrame(index=cat_cols, columns=cat_cols, dtype=float)
    for col_x in cat_cols:
        for col_y in cat_cols:
            if col_x == col_y:
                matrix.loc[col_x, col_y] = 1.0
            else:
                confusion = pd.crosstab(df[col_x], df[col_y])
                matrix.loc[col_x, col_y] = cramers_v(confusion)
    return matrix
