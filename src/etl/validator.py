"""
Validator Engine
Sprint 1 - Day 3
"""

from src.etl.loader import load_excel
from src.etl.validation_report import generate_validation_report
from src.etl.dq_rules import (
    dq01_primary_key_uniqueness,
    dq02_company_year_uniqueness,
    dq03_foreign_key_integrity,
    dq04_balance_sheet,
    dq05_positive_sales,
    dq06_valid_urls,
    dq07_net_cash,
    dq08_tax_rate,
    dq09_dividend,
    dq10_eps,
    dq11_company_name,
    dq12_duplicate_company,
    dq13_missing_year,
    dq14_mandatory,
    dq15_ticker,
    dq16_dataset_coverage,
)


class Validator:

    def __init__(self):
        self.failures = []

    def add_failure(self, rule, severity, dataset, message, rows):
        self.failures.append({
            "rule": rule,
            "severity": severity,
            "dataset": dataset,
            "message": message,
            "rows": rows
        })

    def validate_companies(self):

        print("\nValidating companies.xlsx...")

        df = load_excel("companies.xlsx")

        passed, failed = dq01_primary_key_uniqueness(df, "id")

        if passed:
            print("✅ DQ-01 Passed")
        else:
            print("❌ DQ-01 Failed")
            print(failed)

            self.add_failure(
                "DQ-01",
                "CRITICAL",
                "companies.xlsx",
                "Duplicate Primary Key",
                failed
            )

    def validate_profit_and_loss(self):

        print("\nValidating profitandloss.xlsx...")

        df = load_excel("profitandloss.xlsx")

        passed, failed = dq02_company_year_uniqueness(df)

        if passed:
            print("✅ DQ-02 Passed")
        else:
            print("❌ DQ-02 Failed")
            print(failed)

            self.add_failure(
                "DQ-02",
                "CRITICAL",
                "profitandloss.xlsx",
                "Duplicate Company-Year",
                failed
            )

    def validate_balance_sheet(self):

        print("\nValidating balancesheet.xlsx...")

        df = load_excel("balancesheet.xlsx")

        passed, failed = dq04_balance_sheet(df)

        if passed:
            print("✅ DQ-04 Passed")
        else:
            print("❌ DQ-04 Failed")
            print(failed)

            self.add_failure(
                "DQ-04",
                "WARNING",
                "balancesheet.xlsx",
                "Balance Sheet Mismatch",
                failed
            )

    def validate_sales(self):

        print("\nValidating Sales...")

        df = load_excel("profitandloss.xlsx")

        passed, failed = dq05_positive_sales(df)

        if passed:
            print("✅ DQ-05 Passed")
        else:
            print("❌ DQ-05 Failed")
            print(failed)

            self.add_failure(
                "DQ-05",
                "WARNING",
                "profitandloss.xlsx",
                "Negative Sales",
                failed
            )

    def validate_urls(self):

        print("\nValidating Company URLs...")

        df = load_excel("companies.xlsx")

        passed, failed = dq06_valid_urls(df)

        if passed:
            print("✅ DQ-06 Passed")
        else:
            print("❌ DQ-06 Failed")
            print(failed)

            self.add_failure(
                "DQ-06",
                "WARNING",
                "companies.xlsx",
                "Invalid Website URL",
                failed
            )

    def validate_net_cash(self):

        print("\nValidating Cash Flow...")

        df = load_excel("cashflow.xlsx")

        passed, failed = dq07_net_cash(df)

        if passed:
            print("✅ DQ-07 Passed")
        else:
            print("❌ DQ-07 Failed")
            print(failed)

            self.add_failure(
                "DQ-07",
                "WARNING",
                "cashflow.xlsx",
                "Negative Net Cash",
                failed
            )

    def validate_tax_rate(self):

        print("\nValidating Tax Rate...")

        df = load_excel("profitandloss.xlsx")

        passed, failed = dq08_tax_rate(df)

        if passed:
            print("✅ DQ-08 Passed")
        else:
            print("❌ DQ-08 Failed")
            print(failed)

            self.add_failure(
                "DQ-08",
                "WARNING",
                "profitandloss.xlsx",
                "Invalid Tax Percentage",
                failed
            )
    

        def validate_dividend(self):

         print("\nValidating Dividend Payout...")

        df = load_excel("profitandloss.xlsx")

        passed, failed = dq09_dividend(df)

        if passed:
            print("✅ DQ-09 Passed")
        else:
            print("❌ DQ-09 Failed")
            print(failed)

            self.add_failure(
                "DQ-09",
                "WARNING",
                "profitandloss.xlsx",
                "Dividend Payout > 100%",
                failed
            )

    def validate_eps(self):

        print("\nValidating EPS...")

        df = load_excel("profitandloss.xlsx")

        passed, failed = dq10_eps(df)

        if passed:
            print("✅ DQ-10 Passed")
        else:
            print("❌ DQ-10 Failed")
            print(failed)

            self.add_failure(
                "DQ-10",
                "WARNING",
                "profitandloss.xlsx",
                "Missing EPS",
                failed
            )

    def validate_company_name(self):

        print("\nValidating Company Names...")

        df = load_excel("companies.xlsx")

        passed, failed = dq11_company_name(df)

        if passed:
            print("✅ DQ-11 Passed")
        else:
            print("❌ DQ-11 Failed")
            print(failed)

            self.add_failure(
                "DQ-11",
                "WARNING",
                "companies.xlsx",
                "Missing Company Name",
                failed
            )

    def validate_duplicate_company(self):

        print("\nValidating Duplicate Company Names...")

        df = load_excel("companies.xlsx")

        passed, failed = dq12_duplicate_company(df)

        if passed:
            print("✅ DQ-12 Passed")
        else:
            print("❌ DQ-12 Failed")
            print(failed)

            self.add_failure(
                "DQ-12",
                "WARNING",
                "companies.xlsx",
                "Duplicate Company Name",
                failed
            )

    def validate_missing_year(self):

        print("\nValidating Missing Year...")

        df = load_excel("profitandloss.xlsx")

        passed, failed = dq13_missing_year(df)

        if passed:
            print("✅ DQ-13 Passed")
        else:
            print("❌ DQ-13 Failed")
            print(failed)

            self.add_failure(
                "DQ-13",
                "WARNING",
                "profitandloss.xlsx",
                "Missing Year",
                failed
            )

    def validate_mandatory_fields(self):

        print("\nValidating Mandatory Fields...")

        df = load_excel("companies.xlsx")

        passed, failed = dq14_mandatory(df)

        if passed:
            print("✅ DQ-14 Passed")
        else:
            print("❌ DQ-14 Failed")
            print(failed)

            self.add_failure(
                "DQ-14",
                "WARNING",
                "companies.xlsx",
                "Mandatory Field Missing",
                failed
            )

    def validate_ticker(self):

        print("\nValidating Company ID Format...")

        df = load_excel("companies.xlsx")

        passed, failed = dq15_ticker(df)

        if passed:
            print("✅ DQ-15 Passed")
        else:
            print("❌ DQ-15 Failed")
            print(failed)

            self.add_failure(
                "DQ-15",
                "WARNING",
                "companies.xlsx",
                "Invalid Company ID Format",
                failed
            )

    def validate_dataset_coverage(self):

        print("\nValidating Dataset Coverage...")

        df = load_excel("companies.xlsx")

        passed, failed = dq16_dataset_coverage(df)

        if passed:
            print("✅ DQ-16 Passed")
        else:
            print("❌ DQ-16 Failed")
            print(failed)

            self.add_failure(
                "DQ-16",
                "WARNING",
                "companies.xlsx",
                "Dataset Coverage Below Threshold",
                failed
            )

    def run(self):

        print("=" * 60)
        print("DATA QUALITY VALIDATION")
        print("=" * 60)

        self.validate_companies()
        self.validate_profit_and_loss()
        self.validate_balance_sheet()
        self.validate_sales()
        self.validate_urls()
        self.validate_net_cash()
        self.validate_tax_rate()
        self.validate_dividend()
        self.validate_eps()
        self.validate_company_name()
        self.validate_duplicate_company()
        self.validate_missing_year()
        self.validate_mandatory_fields()
        self.validate_ticker()
        self.validate_dataset_coverage()

        print("\n" + "=" * 60)
        print("VALIDATION SUMMARY")
        print("=" * 60)

        print(f"Rules Executed : 16")
        print(f"Failures Found : {len(self.failures)}")

        critical = sum(
            1 for f in self.failures
            if f["severity"] == "CRITICAL"
        )

        warning = sum(
            1 for f in self.failures
            if f["severity"] == "WARNING"
        )

        print(f"Critical : {critical}")
        print(f"Warnings : {warning}")

        generate_validation_report(self.failures)


if __name__ == "__main__":

    validator = Validator()

    validator.run()