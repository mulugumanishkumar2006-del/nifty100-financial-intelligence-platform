"""
Dataset Inspector
-----------------
This utility scans all Excel datasets in the data/raw directory and
generates a summary report containing:

- File name
- Sheet names
- Number of rows
- Number of columns
- Column names
- Missing value count
- Duplicate row count

Output:
output/dataset_report.txt
"""

from pathlib import Path
import pandas as pd

# ---------------------------------------------------------------------
# Paths
# ---------------------------------------------------------------------

PROJECT_ROOT = Path(__file__).resolve().parents[2]

DATA_DIR = PROJECT_ROOT / "data" / "raw"
OUTPUT_DIR = PROJECT_ROOT / "output"

OUTPUT_DIR.mkdir(exist_ok=True)

REPORT_FILE = OUTPUT_DIR / "dataset_report.txt"

# ---------------------------------------------------------------------
# Dataset Inspector
# ---------------------------------------------------------------------


def inspect_excel_file(file_path: Path) -> str:
    """
    Inspect a single Excel file.
    Returns a formatted report string.
    """

    report = []

    report.append("=" * 80)
    report.append(f"FILE : {file_path.name}")
    report.append("=" * 80)

    try:
        excel = pd.ExcelFile(file_path)

        report.append(f"Number of Sheets : {len(excel.sheet_names)}")
        report.append(f"Sheet Names      : {', '.join(excel.sheet_names)}")
        report.append("")

        for sheet in excel.sheet_names:

            df = pd.read_excel(file_path, sheet_name=sheet)

            report.append("-" * 80)
            report.append(f"Sheet : {sheet}")
            report.append("-" * 80)

            report.append(f"Rows              : {df.shape[0]}")
            report.append(f"Columns           : {df.shape[1]}")
            report.append(f"Duplicate Rows    : {df.duplicated().sum()}")
            report.append(f"Missing Values    : {df.isnull().sum().sum()}")

            report.append("")
            report.append("Column Names:")

            for column in df.columns:
                report.append(f"  - {column}")

            report.append("")
            report.append("Missing Values Per Column:")

            missing = df.isnull().sum()

            for col, value in missing.items():
                report.append(f"  {col:<35} {value}")

            report.append("")

    except Exception as e:
        report.append(f"ERROR : {e}")

    report.append("\n")

    return "\n".join(report)


# ---------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------


def main():

    reports = []

    excel_files = sorted(DATA_DIR.glob("*.xlsx"))

    if not excel_files:
        print("No Excel files found.")
        return

    print(f"Found {len(excel_files)} Excel files.\n")

    for file in excel_files:

        print(f"Inspecting {file.name}...")

        reports.append(inspect_excel_file(file))

    REPORT_FILE.write_text(
        "\n".join(reports),
        encoding="utf-8"
    )

    print("\nInspection Completed.")
    print(f"Report saved to:\n{REPORT_FILE}")


if __name__ == "__main__":
    main()