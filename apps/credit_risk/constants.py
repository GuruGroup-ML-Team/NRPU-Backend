# CSV Filenames
BANK_CSV_FILENAME = "Data/fsabanks.csv"

# Years
BANK_YEARS = ['2019', '2020', '2021', '2022', '2023']

# Bank Financial Ratio Categories
BANK_EFFICIENCY_RATIOS = "efficiency_ratios"
BANK_LIQUIDITY_RATIOS = "liquidity_ratios"
BANK_ASSET_QUALITY_RATIOS = "asset_quality_ratios"
BANK_CAPITAL_RATIOS = "capital_ratios"

# Categories for company financial ratios


# Bank Financial Data Field Mappings
BANK_FINANCIAL_FIELDS = {
    # Balance Sheet Items
    "CASH": "1. Cash and balances with treasury banks",
    "BALANCES": "2. Balances with other banks",
    "INVESTMENTS": "4. Investments",
    "GROSS_ADVANCES": "5. Gross advances",
    "NPL": "6. Advances-non-performing/classified",
    "PROVISIONS": "7. Provision against advances",
    "NET_ADVANCES": "8. Advances net of provision (C5-C7)",
    "TOTAL_ASSETS": "C. Total assets (C1 to C4 + C8 to C10)",

    # Liability Items
    "BORROWINGS": "2. Borrowings from financial institutions",
    "DEPOSITS": "3. Deposits and other accounts",
    "TOTAL_LIABILITIES": "B. Total liabilities (B1 to B4)",

    # Equity Items
    "TOTAL_EQUITY": "A. Total equity (A1 to A3)",

    # Income Statement Items
    "INTEREST_EARNED": "1. Markup/interest earned",
    "NET_INTEREST": "3. Net markup/interest income",
    "NON_INTEREST_INCOME": "6. Non-markup/interest income",
    "NET_PROFIT": "10. Profit/(loss) after taxation"
}


# Reverse mapping for lookup

# Bank Ratio Scoring Thresholds
BANK_BENCHMARK_SCORING = {
    "significantly_better": {"threshold": 1.20, "score": 5},
    "better": {"threshold": 1.11, "score": 4},
    "on_par": {"threshold": 0.90, "score": 3},
    "worse": {"threshold": 0.80, "score": 2},
    "significantly_worse": {"threshold": 0, "score": 1}
}

BANK_RATING_THRESHOLDS = {
    80: "Strong Buy",
    70: "Buy/Watch Closely",
    60: "Hold",
    50: "Sell/Watch for Warning Signs",
    0: "Strong Sell"
}
# Corrected ratio categories mapping


# Default weights for different company ratio categories



#
# Bank Ratios where lower values are better
BANK_INVERSE_RATIOS = [
    "npl_to_gross_advances",
    "npl_to_equity",
    "advances_to_deposits",
    "deposits_to_equity",
    "liabilities_to_total_assets",
    "gross_advances_to_deposits",
    "gross_advances_to_borrowing_deposits"
]

