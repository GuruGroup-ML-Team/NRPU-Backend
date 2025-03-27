import os
import pandas as pd
from django.conf import settings
from apps.credit_risk.constants import (
    COMPANY_CSV_FILENAME, COMPANY_YEARS, COMPANY_PROFITABILITY_RATIOS, COMPANY_LIQUIDITY_RATIOS,
    COMPANY_EFFICIENCY_RATIOS, COMPANY_SOLVENCY_RATIOS, COMPANY_CASH_FLOW_RATIOS,
    COMPANY_VALUATION_RATIOS, COMPANY_RATING_THRESHOLDS, COMPANY_FINANCIAL_FIELDS,
    COMPANY_INVERSE_RATIOS, COMPANY_RATIO_CATEGORIES
)


class CompanyDataService:
    """Service for handling company financial data operations"""

    @staticmethod
    def get_csv_path():
        """
        Helper method to get the absolute path to the company CSV file

        Returns:
            str: The path to the CSV file
        """
        base_dir = settings.BASE_DIR

        # Define possible locations for the CSV file
        possible_paths = [
            os.path.join(base_dir, COMPANY_CSV_FILENAME),  # Project root
            os.path.join(base_dir, 'bank_api', COMPANY_CSV_FILENAME),
            os.path.join(base_dir, 'data', COMPANY_CSV_FILENAME),
        ]

        # Return the first path that exists
        for path in possible_paths:
            if os.path.exists(path):
                return path

        # Default path if none exist
        return os.path.join(base_dir, COMPANY_CSV_FILENAME)

    @staticmethod
    def get_company_data():
        """
        Load and process company data from CSV

        Returns:
            dict: Processed company data in nested dictionary format
        """
        try:
            # Get the path to the CSV file
            csv_file_path = CompanyDataService.get_csv_path()
            print(f"Attempting to load company CSV from: {csv_file_path}")

            df = pd.read_csv(csv_file_path)

            for year in COMPANY_YEARS:
                if year in df.columns:
                    if df[year].dtype == 'object':
                        df[year] = pd.to_numeric(df[year].str.replace(',', ''), errors='coerce')
                    else:
                        df[year] = pd.to_numeric(df[year], errors='coerce')
            # Initialize the nested dictionary structure
            data = {"Companies": {}}

            for _, row in df.iterrows():
                sector = row['Sector']
                sub_sector = row['Sub-Sector']
                org_name = row['Org Name']
                indicator = row['Indicator']
                sub_indicator = row.get('Sub Indicator', '')
                sub_sub_indicator = row.get('Sub-Sub Indicator', '')

                # Create the hierarchical structure
                if org_name not in data["Companies"]:
                    data["Companies"][org_name] = {
                        "Sector": sector,
                        "Sub-Sector": sub_sector,
                        "Indicators": {}
                    }

                # Create the indicator path
                indicator_key = indicator
                if sub_indicator and not pd.isna(sub_indicator):
                    indicator_key = f"{indicator} - {sub_indicator}"
                if sub_sub_indicator and not pd.isna(sub_sub_indicator):
                    indicator_key = f"{indicator} - {sub_indicator} - {sub_sub_indicator}"

                # Add the indicator data
                if indicator_key not in data["Companies"][org_name]["Indicators"]:
                    data["Companies"][org_name]["Indicators"][indicator_key] = {}

                # Add the yearly values
                for year in COMPANY_YEARS:
                    if year in df.columns and not pd.isna(row.get(year)):
                        data["Companies"][org_name]["Indicators"][indicator_key][year] = row[year]

            return data

        except Exception as e:
            print(f"Error loading company CSV data: {e}")
            # Return empty data structure if file can't be loaded
            return {"Companies": {}}

    @staticmethod
    def get_listed_companies():
        """
        Returns a list of companies

        Returns:
            list: List of company names excluding aggregate entries
        """
        try:
            csv_file_path = CompanyDataService.get_csv_path()
            df = pd.read_csv(csv_file_path)

            # Get unique company names, excluding aggregates
            # (assumption: companies named 'All Companies', 'Industry Average', etc. are aggregates)
            companies = df[~df['Org Name'].str.contains('All|Average|Total', case=False, na=False)][
                'Org Name'].unique().tolist()
            return companies

        except Exception as e:
            print(f"Error getting listed companies: {e}")
            return []

    @staticmethod
    def get_company_sectors():
        """
        Returns a list of all sectors from the CSV file

        Returns:
            list: List of unique sector names
        """
        try:
            csv_file_path = CompanyDataService.get_csv_path()
            df = pd.read_csv(csv_file_path)

            # Get unique sector names
            sectors = df['Sector'].unique().tolist()
            return sectors

        except Exception as e:
            print(f"Error getting company sectors: {e}")
            return []

    @staticmethod
    def get_company_sub_sectors(sector):
        """
        Returns a list of sub-sectors for a given sector

        Args:
            sector (str): Sector name

        Returns:
            list: List of sub-sectors
        """
        try:
            csv_file_path = CompanyDataService.get_csv_path()
            df = pd.read_csv(csv_file_path)

            # Filter by sector and get unique sub-sectors
            sub_sectors = df[df['Sector'] == sector]['Sub-Sector'].unique().tolist()
            return sub_sectors

        except Exception as e:
            print(f"Error getting company sub-sectors: {e}")
            return []

    @staticmethod
    def get_companies_by_sub_sector(sub_sector):
        """
        Returns a list of companies for a given sub-sector

        Args:
            sub_sector (str): Sub-sector name

        Returns:
            list: List of company names
        """
        try:
            csv_file_path = CompanyDataService.get_csv_path()
            df = pd.read_csv(csv_file_path)

            # Filter by sub-sector and get unique company names
            companies = df[df['Sub-Sector'] == sub_sector]['Org Name'].unique().tolist()
            return companies

        except Exception as e:
            print(f"Error getting companies by sub-sector: {e}")
            return []

    @staticmethod
    def get_company_indicators():
        """
        Returns a list of available indicators from the CSV file

        Returns:
            list: List of unique indicators
        """
        try:
            csv_file_path = CompanyDataService.get_csv_path()
            df = pd.read_csv(csv_file_path)

            # Get unique indicator names
            indicators = df['Indicator'].unique().tolist()
            return indicators

        except Exception as e:
            print(f"Error getting company indicators: {e}")
            return []

    @staticmethod
    def get_company_sub_indicators(indicator):
        """
        Returns a list of sub-indicators for a given indicator

        Args:
            indicator (str): Indicator name

        Returns:
            list: List of sub-indicators
        """
        try:
            csv_file_path = CompanyDataService.get_csv_path()
            df = pd.read_csv(csv_file_path)

            # Filter by indicator and get unique sub-indicators
            sub_indicators = df[df['Indicator'] == indicator]['Sub Indicator'].unique().tolist()
            # Remove empty or None values
            sub_indicators = [si for si in sub_indicators if si and not pd.isna(si)]
            return sub_indicators

        except Exception as e:
            print(f"Error getting company sub-indicators: {e}")
            return []

    @staticmethod
    def get_company_years():
        """
        Returns a list of available years for company data

        Returns:
            list: List of available years
        """
        # Return a filtered list of years that are actually in the data
        try:
            csv_file_path = CompanyDataService.get_csv_path()
            df = pd.read_csv(csv_file_path)
            available_years = [year for year in COMPANY_YEARS if year in df.columns]
            return available_years
        except Exception:
            # Fall back to the constants-defined years
            return COMPANY_YEARS.copy()

    @staticmethod
    def calculate_company_financial_ratios(company_data, year="2022"):
        """
        Calculate key financial ratios for a company based on its data

        Args:
            company_data (dict): The company's financial data
            year (str): The year to calculate ratios for

        Returns:
            dict: A dictionary of calculated financial ratios
        """
        indicators = company_data.get("Indicators", {})

        ratios = {
            COMPANY_PROFITABILITY_RATIOS: {},
            COMPANY_LIQUIDITY_RATIOS: {},
            COMPANY_EFFICIENCY_RATIOS: {},  # Activity ratios in your data
            COMPANY_SOLVENCY_RATIOS: {},
            COMPANY_CASH_FLOW_RATIOS: {},
            COMPANY_VALUATION_RATIOS: {}
        }

        # First, check if pre-calculated ratios exist in the data
        # This is for the case where the dataset already includes calculated ratios
        for ratio_category, category_key in COMPANY_RATIO_CATEGORIES.items():
            if any(key.startswith(category_key) for key in indicators.keys()):
                for ratio_key, ratio_values in indicators.items():
                    if ratio_key.startswith(category_key) and year in ratio_values:
                        # Extract the ratio name from the full key
                        ratio_name = ratio_key.replace(category_key + " - ", "").lower().replace(" ", "_")

                        # Map to the appropriate category
                        if ratio_category == "PROFITABILITY":
                            ratios[COMPANY_PROFITABILITY_RATIOS][ratio_name] = ratio_values[year]
                        elif ratio_category == "LIQUIDITY":
                            ratios[COMPANY_LIQUIDITY_RATIOS][ratio_name] = ratio_values[year]
                        elif ratio_category == "ACTIVITY":
                            ratios[COMPANY_EFFICIENCY_RATIOS][ratio_name] = ratio_values[year]
                        elif ratio_category == "SOLVENCY":
                            ratios[COMPANY_SOLVENCY_RATIOS][ratio_name] = ratio_values[year]
                        elif ratio_category == "CASH_FLOW":
                            ratios[COMPANY_CASH_FLOW_RATIOS][ratio_name] = ratio_values[year]
                        elif ratio_category == "VALUATION":
                            ratios[COMPANY_VALUATION_RATIOS][ratio_name] = ratio_values[year]

        # If we didn't find pre-calculated ratios, calculate them from raw data
        if not any(list(category.values()) for category in ratios.values()):
            try:
                # Helper function to safely get a value from the indicators
                def get_value(field_key):
                    if field_key in COMPANY_FINANCIAL_FIELDS:
                        field_path = COMPANY_FINANCIAL_FIELDS[field_key]
                        if field_path in indicators and year in indicators[field_path]:
                            return indicators[field_path][year]
                    return None

                # Helper function to safely calculate a ratio
                def calculate_ratio(numerator_key, denominator_key, factor=100):
                    numerator = get_value(numerator_key)
                    denominator = get_value(denominator_key)

                    if numerator is not None and denominator is not None and denominator != 0:
                        return round((numerator / denominator) * factor, 2)
                    return None

                # Profitability ratios
                # Return on Equity (ROE)
                ratios[COMPANY_PROFITABILITY_RATIOS]["return_on_equity"] = calculate_ratio(
                    "NET_PROFIT", "TOTAL_EQUITY"
                )

                # Return on Assets (ROA)
                ratios[COMPANY_PROFITABILITY_RATIOS]["return_on_assets"] = calculate_ratio(
                    "NET_PROFIT", "TOTAL_ASSETS"
                )

                # Gross Profit Margin
                ratios[COMPANY_PROFITABILITY_RATIOS]["gross_profit_margin"] = calculate_ratio(
                    "GROSS_PROFIT", "SALES"
                )

                # Net Profit Margin
                ratios[COMPANY_PROFITABILITY_RATIOS]["net_profit_margin"] = calculate_ratio(
                    "NET_PROFIT", "SALES"
                )

                # EBIT Margin
                ratios[COMPANY_PROFITABILITY_RATIOS]["ebit_margin"] = calculate_ratio(
                    "EBIT", "SALES"
                )

                # Liquidity ratios
                # Current Ratio
                ratios[COMPANY_LIQUIDITY_RATIOS]["current_ratio"] = calculate_ratio(
                    "TOTAL_CURRENT_ASSETS", "TOTAL_CURRENT_LIABILITIES", factor=1
                )

                # Quick Ratio (Acid Test)
                quick_ratio = None
                current_assets = get_value("TOTAL_CURRENT_ASSETS")
                inventories = get_value("INVENTORIES")
                current_liabilities = get_value("TOTAL_CURRENT_LIABILITIES")

                if current_assets is not None and inventories is not None and current_liabilities is not None and current_liabilities != 0:
                    quick_ratio = (current_assets - inventories) / current_liabilities
                    ratios[COMPANY_LIQUIDITY_RATIOS]["quick_ratio"] = round(quick_ratio, 2)

                # Cash Ratio
                ratios[COMPANY_LIQUIDITY_RATIOS]["cash_ratio"] = calculate_ratio(
                    "CASH_BANK_BALANCE", "TOTAL_CURRENT_LIABILITIES", factor=1
                )

                # Activity/Efficiency ratios
                # Asset Turnover
                ratios[COMPANY_EFFICIENCY_RATIOS]["asset_turnover"] = calculate_ratio(
                    "SALES", "TOTAL_ASSETS", factor=1
                )

                # Inventory Turnover
                ratios[COMPANY_EFFICIENCY_RATIOS]["inventory_turnover"] = calculate_ratio(
                    "COST_OF_SALES", "INVENTORIES", factor=1
                )

                # Accounts Receivable Turnover
                ratios[COMPANY_EFFICIENCY_RATIOS]["receivables_turnover"] = calculate_ratio(
                    "SALES", "TRADE_RECEIVABLES", factor=1
                )

                # Inventory Days
                inventory_turnover = ratios[COMPANY_EFFICIENCY_RATIOS].get("inventory_turnover")
                if inventory_turnover and inventory_turnover > 0:
                    ratios[COMPANY_EFFICIENCY_RATIOS]["inventory_days"] = round(365 / inventory_turnover, 2)

                # Receivables Days
                receivables_turnover = ratios[COMPANY_EFFICIENCY_RATIOS].get("receivables_turnover")
                if receivables_turnover and receivables_turnover > 0:
                    ratios[COMPANY_EFFICIENCY_RATIOS]["receivables_days"] = round(365 / receivables_turnover, 2)

                # Payables Turnover
                ratios[COMPANY_EFFICIENCY_RATIOS]["payables_turnover"] = calculate_ratio(
                    "PURCHASES", "TRADE_PAYABLES", factor=1
                )

                # Payables Days
                payables_turnover = ratios[COMPANY_EFFICIENCY_RATIOS].get("payables_turnover")
                if payables_turnover and payables_turnover > 0:
                    ratios[COMPANY_EFFICIENCY_RATIOS]["payables_days"] = round(365 / payables_turnover, 2)

                # Solvency ratios
                # Debt-to-Equity Ratio
                total_debt = None
                long_term_debt = get_value("LONG_TERM_BORROWINGS")
                short_term_debt = get_value("SHORT_TERM_BORROWINGS")

                if long_term_debt is not None and short_term_debt is not None:
                    total_debt = long_term_debt + short_term_debt
                elif long_term_debt is not None:
                    total_debt = long_term_debt
                elif short_term_debt is not None:
                    total_debt = short_term_debt

                if total_debt is not None and get_value("TOTAL_EQUITY") is not None and get_value("TOTAL_EQUITY") != 0:
                    debt_to_equity = total_debt / get_value("TOTAL_EQUITY")
                    ratios[COMPANY_SOLVENCY_RATIOS]["debt_to_equity"] = round(debt_to_equity, 2)

                # Debt Ratio
                if total_debt is not None and get_value("TOTAL_ASSETS") is not None and get_value("TOTAL_ASSETS") != 0:
                    debt_ratio = total_debt / get_value("TOTAL_ASSETS")
                    ratios[COMPANY_SOLVENCY_RATIOS]["debt_ratio"] = round(debt_ratio * 100, 2)

                # Interest Coverage Ratio
                ratios[COMPANY_SOLVENCY_RATIOS]["interest_coverage"] = calculate_ratio(
                    "EBIT", "FINANCIAL_EXPENSES", factor=1
                )

                # Equity Ratio
                ratios[COMPANY_SOLVENCY_RATIOS]["equity_ratio"] = calculate_ratio(
                    "TOTAL_EQUITY", "TOTAL_ASSETS"
                )

                # Cash Flow ratios
                # Operating Cash Flow to Sales
                ratios[COMPANY_CASH_FLOW_RATIOS]["ocf_to_sales"] = calculate_ratio(
                    "OPERATING_CASH_FLOW", "SALES"
                )

                # Cash Flow Coverage Ratio
                ratios[COMPANY_CASH_FLOW_RATIOS]["cash_flow_coverage"] = calculate_ratio(
                    "OPERATING_CASH_FLOW", "TOTAL_CURRENT_LIABILITIES", factor=1
                )

                # Cash Flow to Debt Ratio
                if total_debt is not None and get_value("OPERATING_CASH_FLOW") is not None and total_debt != 0:
                    cash_flow_to_debt = get_value("OPERATING_CASH_FLOW") / total_debt
                    ratios[COMPANY_CASH_FLOW_RATIOS]["cash_flow_to_debt"] = round(cash_flow_to_debt, 2)

            except Exception as e:
                print(f"Error calculating company financial ratios: {e}")

        return ratios

    @staticmethod
    def calculate_company_ratio_trend(company_data, ratio_type, numerator_key, denominator_key, factor=100, years=None):
        """
        Calculate trend data for a specific ratio over multiple years

        Args:
            company_data (dict): The company's financial data
            ratio_type (str): Type of ratio (e.g., 'ROA', 'Profit Margin')
            numerator_key (str): Key for the numerator in company_data
            denominator_key (str): Key for the denominator in company_data
            factor (float): Multiplication factor (e.g., 100 for percentage)
            years (list): List of years to include in trend (defaults to all available)

        Returns:
            dict: A dictionary with years as keys and ratio values as values
        """
        if years is None:
            years = CompanyDataService.get_company_years()

        indicators = company_data.get("Indicators", {})
        trend_data = {}

        for year in years:
            try:
                if (numerator_key in COMPANY_FINANCIAL_FIELDS and
                        denominator_key in COMPANY_FINANCIAL_FIELDS):

                    num_field = COMPANY_FINANCIAL_FIELDS[numerator_key]
                    denom_field = COMPANY_FINANCIAL_FIELDS[denominator_key]

                    if (num_field in indicators and year in indicators[num_field] and
                            denom_field in indicators and year in indicators[denom_field] and
                            indicators[denom_field][year] != 0):

                        numerator = indicators[num_field][year]
                        denominator = indicators[denom_field][year]
                        ratio = (numerator / denominator) * factor
                        trend_data[year] = round(ratio, 2)
                    else:
                        trend_data[year] = None
                else:
                    trend_data[year] = None
            except (KeyError, TypeError, ZeroDivisionError):
                trend_data[year] = None

        return trend_data

    @staticmethod
    def calculate_company_score(company_data, weights, year="2022"):
        """
        Calculate an overall financial health score for a company

        Args:
            company_data (dict): The company's financial data
            weights (dict): Dictionary with category weights
            year (str): The year to calculate score for

        Returns:
            dict: Score details including category scores and overall rating
        """
        # Calculate all ratios first
        ratios = CompanyDataService.calculate_company_financial_ratios(company_data, year)

        # Get industry data (assuming there's an Industry Average entry)
        data = CompanyDataService.get_company_data()

        # Find industry average data by sub-sector
        sub_sector = company_data.get("Sub-Sector")
        industry_data = None

        for company_name, company_info in data["Companies"].items():
            if company_name.lower().find("industry average") >= 0 and company_info.get("Sub-Sector") == sub_sector:
                industry_data = company_info
                break

        # If no specific industry average for sub-sector, try sector-wide
        if not industry_data:
            sector = company_data.get("Sector")
            for company_name, company_info in data["Companies"].items():
                if company_name.lower().find("industry average") >= 0 and company_info.get("Sector") == sector:
                    industry_data = company_info
                    break

        # As a last resort, use any industry average
        if not industry_data:
            for company_name, company_info in data["Companies"].items():
                if company_name.lower().find("industry average") >= 0:
                    industry_data = company_info
                    break

        # Calculate industry ratios if we found industry data
        industry_ratios = {}
        if industry_data:
            industry_ratios = CompanyDataService.calculate_company_financial_ratios(industry_data, year)

        # Initialize the scores structure
        ratio_scores = {
            COMPANY_PROFITABILITY_RATIOS: {},
            COMPANY_LIQUIDITY_RATIOS: {},
            COMPANY_EFFICIENCY_RATIOS: {},
            COMPANY_SOLVENCY_RATIOS: {},
            COMPANY_CASH_FLOW_RATIOS: {},
            COMPANY_VALUATION_RATIOS: {}
        }

        # For each category and ratio, compare with industry and assign score
        for category, category_ratios in ratios.items():
            for ratio_name, ratio_value in category_ratios.items():
                # Skip if ratio is None or no industry data
                if ratio_value is None or not industry_ratios or category not in industry_ratios or ratio_name not in \
                        industry_ratios[category]:
                    continue

                industry_value = industry_ratios[category].get(ratio_name)
                if industry_value is None or industry_value == 0:
                    continue

                if ratio_name in COMPANY_INVERSE_RATIOS:
                    comparison_ratio = industry_value / ratio_value if ratio_value > 0 else 0
                else:
                    # For these ratios, higher is better
                    comparison_ratio = ratio_value / industry_value if industry_value > 0 else 0

                score = 1  # Default to worst score
                if comparison_ratio >= 1.2:
                    score = 5  # Excellent
                elif comparison_ratio >= 1.05:
                    score = 4  # Good
                elif comparison_ratio >= 0.95:
                    score = 3  # Average
                elif comparison_ratio >= 0.8:
                    score = 2  # Below Average
                # else score remains 1 (Poor)

                ratio_scores[category][ratio_name] = score

        # Calculate category scores
        category_scores = {}
        for category, scores in ratio_scores.items():
            if scores:
                category_scores[category] = sum(scores.values()) / len(scores)
            else:
                category_scores[category] = 0

        # Calculate weighted score
        weighted_score = 0
        weight_sum = 0

        # Map ratio categories to weight keys
        category_weight_map = {
            COMPANY_PROFITABILITY_RATIOS: "profitability",
            COMPANY_LIQUIDITY_RATIOS: "liquidity",
            COMPANY_EFFICIENCY_RATIOS: "activity",  # Note the change from efficiency to activity
            COMPANY_SOLVENCY_RATIOS: "solvency",
            COMPANY_CASH_FLOW_RATIOS: "cash_flow",
            COMPANY_VALUATION_RATIOS: "valuation"
        }

        for category, score in category_scores.items():
            if category in category_weight_map:
                weight_key = category_weight_map[category]
                weight = weights.get(weight_key, 0)
                weighted_score += score * weight
                weight_sum += weight

        # Adjust percentage calculation to handle case where no weights apply
        if weight_sum > 0:
            percentage_score = (weighted_score / (5 * weight_sum)) * 100
        else:
            percentage_score = 0

        # Determine rating based on percentage score
        rating = "Not Rated"
        for threshold, rating_value in sorted(COMPANY_RATING_THRESHOLDS.items(), reverse=True):
            if percentage_score >= threshold:
                rating = rating_value
                break

        return {
            "ratio_scores": ratio_scores,
            "category_scores": category_scores,
            "weighted_score": round(weighted_score, 2),
            "percentage_score": round(percentage_score, 2),
            "rating": rating,
            "comparison_data": {
                "company_ratios": ratios,
                "industry_ratios": industry_ratios if industry_ratios else None
            }
        }

    @staticmethod
    def get_company_comparison_data(companies, indicators, year="2022"):
        """
        Get comparison data for multiple companies on specified indicators

        Args:
            companies (list): List of company names to compare
            indicators (list): List of indicators to compare
            year (str): Year for comparison

        Returns:
            dict: Comparison data organized by company and indicator
        """
        data = CompanyDataService.get_company_data()
        result = {}

        for company in companies:
            if company not in data["Companies"]:
                continue

            company_data = data["Companies"][company]
            company_indicators = company_data.get("Indicators", {})
            result[company] = {
                "sector": company_data.get("Sector", ""),
                "sub_sector": company_data.get("Sub-Sector", ""),
                "indicators": {}
            }

            for indicator in indicators:
                if indicator in company_indicators and year in company_indicators[indicator]:
                    result[company]["indicators"][indicator] = company_indicators[indicator][year]
                else:
                    result[company]["indicators"][indicator] = None

        # Try to add industry average if available
        for company_name, company_info in data["Companies"].items():
            if "industry average" in company_name.lower():
                industry_indicators = company_info.get("Indicators", {})
                result["Industry Average"] = {
                    "sector": company_info.get("Sector", ""),
                    "sub_sector": company_info.get("Sub-Sector", ""),
                    "indicators": {}
                }

                for indicator in indicators:
                    if indicator in industry_indicators and year in industry_indicators[indicator]:
                        result["Industry Average"]["indicators"][indicator] = industry_indicators[indicator][year]
                    else:
                        result["Industry Average"]["indicators"][indicator] = None

                break  # Just use the first industry average we find

        return result