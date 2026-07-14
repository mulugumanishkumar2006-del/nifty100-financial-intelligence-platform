"""
Validation Report Generator
"""

import pandas as pd

from src.config.settings import OUTPUT_DIR


def generate_validation_report(failures):

    rows = []

    for failure in failures:

        failed_df = failure["rows"]

        if failed_df is None:
            continue

        for index, _ in failed_df.iterrows():

            rows.append({
                "Rule": failure["rule"],
                "Severity": failure["severity"],
                "Dataset": failure["dataset"],
                "Row": index,
                "Message": failure["message"]
            })

    report = pd.DataFrame(rows)

    output_file = OUTPUT_DIR / "validation_failures.csv"

    report.to_csv(output_file, index=False)

    print(f"\nValidation report saved to:\n{output_file}")