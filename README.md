### FILE: insight_mapping/README.md

# Insight Mapping – Automated Exploratory Data Analysis Engine

[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)

**Insight Mapping** is a production-ready, modular Python tool that automatically performs comprehensive exploratory data analysis (EDA) on tabular datasets and generates structured HTML and JSON reports with visualizations, descriptive statistics, and correlation insights.

## ✨ Features

- **Multi-format Support**: CSV, TSV, Excel (.xlsx/.xls), JSON, JSONL, and Parquet
- **Modular Architecture**: Clean separation of concerns with dedicated modules
- **CLI Interface**: Easy-to-use command-line interface with options
- **Automated Reports**: HTML and JSON reports with embedded visualizations
- **Comprehensive Statistics**: Descriptive stats, skewness, kurtosis, memory usage
- **Missing Value Analysis**: Tables, plots, and data quality scoring
- **Duplicate Detection**: Row-level and column-level duplicate analysis
- **Outlier Detection**: IQR and Z-score methods
- **Correlation Analysis**: 
  - Numeric: Pearson correlation heatmaps
  - Categorical: Cramér's V association heatmaps
- **Visualizations**:
  - Histograms with KDE
  - Boxplots and Violin plots
  - Pairplots for numeric features
  - Bar charts for categorical features
  - Interactive Plotly scatter plots
- **Optional Integrations**: ydata-profiling and Sweetviz reports
- **Logging**: Rotating file logs with configurable verbosity

## 📁 Project Structure

```
insight_mapping/
├── main.py                  # CLI entry point
├── data_loader.py           # Multi-format data loading
├── cleaning_insights.py     # Missing values, duplicates, outliers
├── descriptive_stats.py     # Statistical summaries
├── correlation_analysis.py  # Numeric & categorical correlations
├── visualization.py         # Static & interactive charts
├── report_generator.py      # HTML/JSON report generation
├── logger_config.py         # Logging configuration
├── utils.py                 # Utility functions
├── README.md
├── requirements.txt
├── demo_data/
│   ├── sample1.csv
│   ├── sample2.xlsx
│   └── sample3.json
└── reports/
    ├── sample_report.html
    └── sample_report.json
```

## 🚀 Installation

1. **Clone or download** the project.

2. **Create a virtual environment** (recommended):
   ```bash
   python -m venv venv
   source venv/bin/activate  # Linux/Mac
   venv\Scripts\activate     # Windows
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

## 📖 Usage

### Basic Usage
```bash
python main.py demo_data/sample1.csv
```

### Specify Output Directory
```bash
python main.py demo_data/sample1.csv --output my_reports
```

### Generate Extended Profiling Reports
```bash
python main.py demo_data/sample1.csv --output reports --profile
```

### Enable Verbose Logging
```bash
python main.py demo_data/sample1.csv -v
```

### Full Example
```bash
python main.py data/sales_data.xlsx -o analysis_reports -p -v
```

## 🎯 CLI Options

| Option | Short | Description |
|--------|-------|-------------|
| `input` | - | Path to dataset (required) |
| `--output` | `-o` | Output directory (default: `reports`) |
| `--profile` | `-p` | Generate ydata-profiling and Sweetviz reports |
| `--verbose` | `-v` | Enable debug logging |

## 📊 Output Reports

### HTML Report (`report.html`)
- Modern, responsive design with navigation
- Embedded visualizations
- Dataset summary, missing values, duplicates
- Correlation heatmaps
- All generated charts

### JSON Report (`report.json`)
- Machine-readable structured data
- Complete statistics and metadata
- Timestamps and engine version
- Paths to generated visualizations

## 🔧 Configuration

### Supported File Formats
- **CSV/TSV/TXT**: Comma or tab-separated values
- **Excel**: .xlsx, .xls (requires openpyxl)
- **JSON/JSONL**: Standard and line-delimited JSON
- **Parquet**: Apache Parquet format (requires pyarrow)

### Optional Dependencies
These are included in requirements.txt but gracefully handled if missing:
- `plotly`: Interactive visualizations
- `ydata-profiling`: Extended profiling reports
- `sweetviz`: Comparative EDA reports
- `dtale`: Interactive data exploration
- `missingno`: Missing value visualizations

## 📝 Example Output

After running on `sample1.csv`:
```
reports/
├── report.html
├── report.json
├── logs/
│   └── insight_mapping.log
└── visuals/
    ├── hist_age.png
    ├── hist_salary.png
    ├── box_age.png
    ├── violin_salary.png
    ├── pairplot.png
    ├── bar_department.png
    ├── corr_numeric.png
    ├── corr_categorical.png
    ├── missing_matrix.png
    └── interactive_scatter.html
```

## 🤝 Contributing

Contributions are welcome! Please feel free to submit issues or pull requests.

---

**Insight Mapping v1.0** – Transform your data into actionable insights.
