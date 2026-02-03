"""### FILE: insight_mapping/visualization.py

Visualization module for Insight Mapping EDA Engine.
Generates static (matplotlib/seaborn) and interactive (plotly) charts.
"""

from __future__ import annotations

from pathlib import Path
from typing import Dict, List, Optional

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

try:
    import plotly.express as px
    import plotly.graph_objects as go
except Exception:  # pragma: no cover - optional
    px = None
    go = None

from utils import get_categorical_columns, get_numeric_columns, limit_categories


# Configure plotting style
sns.set_theme(style="whitegrid", palette="husl")
plt.rcParams["figure.dpi"] = 100
plt.rcParams["savefig.dpi"] = 150


def _save_fig(fig, path: Path) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(path, bbox_inches="tight")
    plt.close(fig)
    return path


def histograms(df: pd.DataFrame, output_dir: Path) -> List[Path]:
    paths: List[Path] = []
    for col in get_numeric_columns(df):
        fig, ax = plt.subplots(figsize=(6, 4))
        sns.histplot(df[col].dropna(), kde=True, ax=ax)
        ax.set_title(f"Histogram: {col}")
        paths.append(_save_fig(fig, output_dir / f"hist_{col}.png"))
    return paths


def boxplots(df: pd.DataFrame, output_dir: Path) -> List[Path]:
    paths: List[Path] = []
    for col in get_numeric_columns(df):
        fig, ax = plt.subplots(figsize=(6, 4))
        sns.boxplot(x=df[col], ax=ax)
        ax.set_title(f"Boxplot: {col}")
        paths.append(_save_fig(fig, output_dir / f"box_{col}.png"))
    return paths


def violin_plots(df: pd.DataFrame, output_dir: Path) -> List[Path]:
    paths: List[Path] = []
    for col in get_numeric_columns(df):
        fig, ax = plt.subplots(figsize=(6, 4))
        sns.violinplot(x=df[col], ax=ax)
        ax.set_title(f"Violin: {col}")
        paths.append(_save_fig(fig, output_dir / f"violin_{col}.png"))
    return paths


def pairplot(df: pd.DataFrame, output_dir: Path) -> Optional[Path]:
    numeric_cols = get_numeric_columns(df)
    if len(numeric_cols) < 2:
        return None
    plot = sns.pairplot(df[numeric_cols].dropna())
    path = output_dir / "pairplot.png"
    plot.savefig(path)
    plt.close("all")
    return path


def bar_charts(df: pd.DataFrame, output_dir: Path) -> List[Path]:
    paths: List[Path] = []
    for col in get_categorical_columns(df):
        series = limit_categories(df[col])
        fig, ax = plt.subplots(figsize=(6, 4))
        series.value_counts(dropna=False).plot(kind="bar", ax=ax)
        ax.set_title(f"Bar Chart: {col}")
        ax.set_xlabel(col)
        ax.set_ylabel("Count")
        paths.append(_save_fig(fig, output_dir / f"bar_{col}.png"))
    return paths


def correlation_heatmap(corr: pd.DataFrame, output_dir: Path, name: str) -> Optional[Path]:
    if corr.empty:
        return None
    fig, ax = plt.subplots(figsize=(8, 6))
    sns.heatmap(corr, annot=True, cmap="coolwarm", ax=ax)
    ax.set_title(f"Correlation Heatmap: {name}")
    return _save_fig(fig, output_dir / f"corr_{name}.png")


def interactive_scatter(df: pd.DataFrame, output_dir: Path) -> Optional[Path]:
    if px is None:
        return None
    numeric_cols = get_numeric_columns(df)
    if len(numeric_cols) < 2:
        return None
    fig = px.scatter(df, x=numeric_cols[0], y=numeric_cols[1], title="Interactive Scatter")
    path = output_dir / "interactive_scatter.html"
    path.parent.mkdir(parents=True, exist_ok=True)
    fig.write_html(str(path), include_plotlyjs="cdn")
    return path
