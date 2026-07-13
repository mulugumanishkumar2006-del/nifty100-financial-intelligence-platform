import re


def clean_whitespace(text):
    if text is None:
        return None
    return str(text).strip()


def normalize_column_names(column):
    column = clean_whitespace(column)
    column = column.lower()
    column = re.sub(r"[^\w\s]", "", column)
    column = column.replace(" ", "_")
    return column


def normalize_ticker(ticker):
    ticker = clean_whitespace(ticker)
    ticker = ticker.upper()
    ticker = ticker.replace(".NS", "")
    ticker = ticker.replace(".BO", "")
    return ticker


def normalize_company_name(name):
    name = clean_whitespace(name)
    return name.title()


def normalize_year(year):
    year = str(year).strip()

    if year.startswith("FY"):
        year = year.replace("FY", "").strip()

        if len(year) == 2:
            return int("20" + year)

        return int(year)

    if "-" in year:
        return int(year.split("-")[0])

    return int(year)


if __name__ == "__main__":
    print(normalize_year("FY24"))
    print(normalize_ticker(" reliance.ns "))
    print(normalize_company_name(" reliance industries ltd "))
    print(normalize_column_names("Company Name"))
    print(clean_whitespace("  Hello World  "))