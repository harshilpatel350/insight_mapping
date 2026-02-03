"""### FILE: insight_mapping/data_loader.py

Data loading module for Insight Mapping EDA Engine.
Supports CSV, Excel, and JSON file formats.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Optional, Tuple

import pandas as pd


def load_data(
    file_path: Path,
    encoding: str = "utf-8",
    sheet_name: Optional[str] = None,
) -> Tuple[pd.DataFrame, str]:
    """Load CSV, Excel, or JSON data into a DataFrame.

    Args:
        file_path: Path to the data file.
        encoding: Character encoding for CSV files.
        sheet_name: Sheet name for Excel files (optional).

    Returns:
        Tuple of (DataFrame, file_type_string)

    Raises:
        FileNotFoundError: If file does not exist.
        ValueError: If file type is not supported.
    """
    if not file_path.exists():
        raise FileNotFoundError(f"File not found: {file_path}")

    suffix = file_path.suffix.lower()

    if suffix in {".csv", ".tsv", ".txt"}:
        sep = "\t" if suffix == ".tsv" else ","
        df = pd.read_csv(file_path, encoding=encoding, sep=sep)
        return df, "csv"

    if suffix in {".xlsx", ".xls"}:
        df = pd.read_excel(file_path, sheet_name=sheet_name or 0)
        return df, "excel"

    if suffix in {".json", ".jsonl"}:
        with file_path.open("r", encoding=encoding) as f:
            if suffix == ".jsonl":
                lines = [json.loads(line) for line in f if line.strip()]
                df = pd.DataFrame(lines)
            else:
                raw = json.load(f)
                df = pd.json_normalize(raw)
        return df, "json"

    if suffix == ".parquet":
        df = pd.read_parquet(file_path)
        return df, "parquet"

    raise ValueError(f"Unsupported file type: {suffix}. Use CSV, Excel, JSON, or Parquet.")
