# bank_api/constants.py
"""
Constants for the bank API
"""

# CSV related constants
CSV_FILENAME = "fsabanks.csv"

# Year constants
YEARS = ['2019', '2020', '2021', '2022', '2023']

# Financial ratio categories
EFFICIENCY_RATIOS = "efficiency_ratios"
LIQUIDITY_RATIOS = "liquidity_ratios"
ASSET_QUALITY_RATIOS = "asset_quality_ratios"
CAPITAL_RATIOS = "capital_ratios"

# Ratio scoring thresholds
BENCHMARK_SCORING = {
    "significantly_better": {
        "threshold": 1.20,  # Above 120%
        "score": 5
    },
    "better": {
        "threshold": 1.11,  # Between 111% and 120%
        "score": 4
    },
    "on_par": {
        "threshold": 0.90,  # Between 90% and 110%
        "score": 3
    },
    "worse": {
        "threshold": 0.80,  # Between 80% and 89%
        "score": 2
    },
    "significantly_worse": {
        "threshold": 0,  # Less than 80%
        "score": 1
    }
}

# Bank rating thresholds
RATING_THRESHOLDS = {
    80: "Strong Buy",
    70: "Buy/Watch Closely",
    60: "Hold",
    50: "Sell/Watch for Warning Signs",
    0: "Strong Sell"
}

# Financial data field mappings
FINANCIAL_FIELDS = {
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

# Ratios where lower values are better
INVERSE_RATIOS = [
    "npl_to_gross_advances",
    "npl_to_equity",
    "advances_to_deposits",
    "deposits_to_equity",
    "liabilities_to_total_assets",
    "gross_advances_to_deposits",
    "gross_advances_to_borrowing_deposits"
]



