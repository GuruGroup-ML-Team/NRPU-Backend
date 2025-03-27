# CSV Filenames
BANK_CSV_FILENAME = "Data/fsabanks.csv"
COMPANY_CSV_FILENAME = "Data/company_data.csv"

# Years
BANK_YEARS = ['2019', '2020', '2021', '2022', '2023']
COMPANY_YEARS = ["2017", "2018", "2019", "2020", "2021", "2022"]

# Bank Financial Ratio Categories
BANK_EFFICIENCY_RATIOS = "efficiency_ratios"
BANK_LIQUIDITY_RATIOS = "liquidity_ratios"
BANK_ASSET_QUALITY_RATIOS = "asset_quality_ratios"
BANK_CAPITAL_RATIOS = "capital_ratios"

# Company Financial Ratio Categories
COMPANY_PROFITABILITY_RATIOS = "company_profitability_ratios"
COMPANY_LIQUIDITY_RATIOS = "company_liquidity_ratios"
COMPANY_EFFICIENCY_RATIOS = "company_efficiency_ratios"
COMPANY_SOLVENCY_RATIOS = "company_solvency_ratios"
COMPANY_CASH_FLOW_RATIOS = "company_cash_flow_ratios"
COMPANY_VALUATION_RATIOS = "company_valuation_ratios"

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

# Company Financial Data Field Mappings
COMPANY_FINANCIAL_FIELDS = {
    # Balance Sheet Fields - Assets
    "CAPITAL_WORK_IN_PROGRESS": "A. Non-Current Assets (A1+A3+A4+A5+A6) - 1. Capital work in progress",
    "OPERATING_FIXED_ASSETS_COST": "A. Non-Current Assets (A1+A3+A4+A5+A6) - 2. Operating fixed assets at cost",
    "OPERATING_FIXED_ASSETS_NET": "A. Non-Current Assets (A1+A3+A4+A5+A6) - 3. Operating fixed assets after deducting accumulated depreciation",
    "INTANGIBLE_ASSETS": "A. Non-Current Assets (A1+A3+A4+A5+A6) - 4. Intangible assets",
    "LONG_TERM_INVESTMENTS": "A. Non-Current Assets (A1+A3+A4+A5+A6) - 5. Long term investments",
    "OTHER_NON_CURRENT_ASSETS": "A. Non-Current Assets (A1+A3+A4+A5+A6) - 6. Other non-current assets",

    "CASH_BANK_BALANCE": "B. Current Assets (B1+B2+B3+B4+B5+B6) - 1. Cash & bank balance",
    "INVENTORIES": "B. Current Assets (B1+B2+B3+B4+B5+B6) - 2. Inventories; of which",
    "TRADE_RECEIVABLES": "B. Current Assets (B1+B2+B3+B4+B5+B6) - 3. Trade Debt / accounts receivables",
    "SHORT_TERM_LOANS": "B. Current Assets (B1+B2+B3+B4+B5+B6) - 4. Short term loans and advances",
    "SHORT_TERM_INVESTMENTS": "B. Current Assets (B1+B2+B3+B4+B5+B6) - 5. Short term investments",
    "OTHER_CURRENT_ASSETS": "B. Current Assets (B1+B2+B3+B4+B5+B6) - 6. Other current assets",

    # Balance Sheet Fields - Equity & Liabilities
    "PAID_UP_CAPITAL": "C. Shareholders' Equity (C1+C2+C3) - 1. Issued, Subscribed & Paid up capital",
    "RESERVES": "C. Shareholders' Equity (C1+C2+C3) - 2. Reserves",
    "REVALUATION_SURPLUS": "C. Shareholders' Equity (C1+C2+C3) - 3. Surplus on revaluation of fixed assets",

    "LONG_TERM_BORROWINGS": "D. Non-Current Liabilities (D1+D2+D3+D4+D5) - 1. Long term borrowings",
    "SUBORDINATED_LOANS": "D. Non-Current Liabilities (D1+D2+D3+D4+D5) - 2. Subordinated loans / Sponsor's loans",
    "DEBENTURES_BONDS": "D. Non-Current Liabilities (D1+D2+D3+D4+D5) - 3. Debentures/TFCs (bonds payable)",
    "EMPLOYEE_BENEFITS": "D. Non-Current Liabilities (D1+D2+D3+D4+D5) - 4. Employees benefit obligations",
    "OTHER_NON_CURRENT_LIABILITIES": "D. Non-Current Liabilities (D1+D2+D3+D4+D5) - 5. Other non-current liabilities",

    "TRADE_PAYABLES": "E. Current Liabilities (E1+E2+E3+E4) - 1. Trade Credit & other accounts payables",
    "SHORT_TERM_BORROWINGS": "E. Current Liabilities (E1+E2+E3+E4) - 2. Short term Borrowings",
    "CURRENT_PORTION_LONG_TERM": "E. Current Liabilities (E1+E2+E3+E4) - 3. Current portion of non-current liabilities",
    "OTHER_CURRENT_LIABILITIES": "E. Current Liabilities (E1+E2+E3+E4) - 4. Other current liabilities",

    # Income Statement Fields
    "SALES": "F. Operations: - 1. Sales",
    "COST_OF_SALES": "F. Operations: - 2. Cost of sales",
    "GROSS_PROFIT": "F. Operations: - 3. Gross profit / (loss) (F1-F2)",
    "ADMIN_EXPENSES": "F. Operations: - 4. General, administrative and other expenses",
    "OTHER_INCOME": "F. Operations: - 5. Other income / (loss)",
    "EBIT": "F. Operations: - 6. EBIT (F3-F4+F5)",
    "FINANCIAL_EXPENSES": "F. Operations: - 7. Financial expenses",
    "PROFIT_BEFORE_TAX": "F. Operations: - 8. Profit / (loss) before taxation (F6-F7)",
    "TAX_EXPENSES": "F. Operations: - 9. Tax expenses",
    "NET_PROFIT": "F. Operations: - 10. Profit / (loss) after tax (F8-F9)",
    "CASH_DIVIDENDS": "F. Operations: - 11. Cash dividends",
    "STOCK_DIVIDENDS": "F. Operations: - 12. Bonus shares / stock dividends",

    # Cash Flow Fields
    "OPERATING_CASH_FLOW": "G. Statement of Cash Flows - 1. Net cash flows from operating activities",
    "INVESTING_CASH_FLOW": "G. Statement of Cash Flows - 2. Net cash flows from investing activities",
    "FINANCING_CASH_FLOW": "G. Statement of Cash Flows - 3. Net cash flows from financing activities",

    # Miscellaneous
    "CAPITAL_EMPLOYED": "H. Miscellaneous - 1. Total capital employed (C+D)",
    "PURCHASES": "H. Miscellaneous - 7. Purchases (F2+Current year B2 - Prev. Year B2)",

    # Aggregated Fields
    "TOTAL_NON_CURRENT_ASSETS": "A. Non-Current Assets (A1+A3+A4+A5+A6)",
    "TOTAL_CURRENT_ASSETS": "B. Current Assets (B1+B2+B3+B4+B5+B6)",
    "TOTAL_ASSETS": "Total Assets (A+B) / Equity & Liabilities (C+D+E)",
    "TOTAL_EQUITY": "C. Shareholders' Equity (C1+C2+C3)",
    "TOTAL_NON_CURRENT_LIABILITIES": "D. Non-Current Liabilities (D1+D2+D3+D4+D5)",
    "TOTAL_CURRENT_LIABILITIES": "E. Current Liabilities (E1+E2+E3+E4)",
    "TOTAL_FIXED_LIABILITIES": "D. Non-Current Liabilities (D1+D2+D3+D4+D5) - 5. Total fixed liabilities (D1+D3)"
}

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
COMPANY_RATIO_CATEGORIES = {
    "PROFITABILITY": "I. Key Performance Indicators - Profitability Ratios",
    "LIQUIDITY": "I. Key Performance Indicators - Liquidity Ratios",
    "ACTIVITY": "I. Key Performance Indicators - Activity Ratios",
    "SOLVENCY": "I. Key Performance Indicators - Solvency Ratios",
    "CASH_FLOW": "I. Key Performance Indicators - Cash Flow Ratios",
    "VALUATION": "I. Key Performance Indicators - Valuation Ratios"
}

# Default weights for different company ratio categories
COMPANY_DEFAULT_WEIGHTS = {
    "profitability": 0.50,
    "liquidity": 0.25,
    "activity": 0.15,  # renamed from efficiency to match your data
    "solvency": 0.10
}

# Company Rating Thresholds
COMPANY_RATING_THRESHOLDS = {
    80: "Strong Buy",
    70: "Buy",
    60: "Hold",
    50: "Sell",
    0: "Strong Sell"
}

# Company rating interpretations (used for the final rating output)
COMPANY_RATING_INTERPRETATIONS = {
    "Strong Buy": "Low risk investment with good fundamentals",
    "Buy": "Good investment potential with minor weaknesses",
    "Hold": "Average performance; may lack compelling growth or undervaluation",
    "Sell": "Below-average; potential risks or lack of competitive advantage",
    "Strong Sell": "High risk investment with poor fundamentals"
}

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

# Company Ratios where lower values are better
COMPANY_INVERSE_RATIOS = [
    "debt_to_equity",
    "debt_ratio",
    "financial_leverage",
    "interest_cover_ratio",
    "asset_turnover",
    "inventory_turnover",
    "debtor_turnover_days",
    "creditor_turnover_days"
]
