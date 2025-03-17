import os
import pandas as pd
from django.conf import settings

# Constants (these would be moved to a constants.py file later)
CSV_FILENAME = "company_data.csv"
YEARS = ["2017", "2018", "2019", "2020", "2021", "2022"]

# Financial fields mapping
FINANCIAL_FIELDS = {
    "REVENUE": "Revenue",
    "NET_PROFIT": "Net Profit",
    "TOTAL_ASSETS": "Total Assets",
    "CURRENT_ASSETS": "Current Assets",
    "CURRENT_LIABILITIES": "Current Liabilities",
    "TOTAL_EQUITY": "Total Equity",
    "TOTAL_DEBT": "Total Debt",
    "EBIT": "EBIT",
    "INTEREST_EXPENSE": "Interest Expense",
    "INVENTORY": "Inventory",
    "COGS": "Cost of Goods Sold",
    "ACCOUNTS_RECEIVABLE": "Accounts Receivable",
    "ACCOUNTS_PAYABLE": "Accounts Payable"
}

# Categorization of ratios
PROFITABILITY_RATIOS = "profitability_ratios"
LIQUIDITY_RATIOS = "liquidity_ratios"
EFFICIENCY_RATIOS = "efficiency_ratios"
SOLVENCY_RATIOS = "solvency_ratios"

# Ratios where lower values are better (inverse)
INVERSE_RATIOS = [
    "debt_to_equity",
    "debt_ratio"
]

# Benchmark scoring thresholds
BENCHMARK_SCORING = {
    "excellent": {"threshold": 1.25, "score": 5},
    "good": {"threshold": 1.00, "score": 4},
    "average": {"threshold": 0.75, "score": 3},
    "below_average": {"threshold": 0.50, "score": 2},
    "poor": {"threshold": 0.00, "score": 1}
}

# Rating thresholds
RATING_THRESHOLDS = {
    80: "Strong Buy",
    70: "Buy",
    60: "Hold",
    50: "Sell",
    0: "Strong Sell"
}


class CompanyDataService:
    """Service for handling company financial data operations"""

    @staticmethod
    def get_csv_path():
        """
        Helper method to get the absolute path to the CSV file

        Returns:
            str: The path to the CSV file
        """
        base_dir = settings.BASE_DIR

        # Define possible locations for the CSV file
        possible_paths = [
            os.path.join(base_dir, CSV_FILENAME),  # Project root
            os.path.join(base_dir, 'company_api', CSV_FILENAME),
            os.path.join(base_dir, 'data', CSV_FILENAME),
        ]

        # Return the first path that exists
        for path in possible_paths:
            if os.path.exists(path):
                return path

        # Default path if none exist
        return os.path.join(base_dir, CSV_FILENAME)

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
            print(f"Attempting to load CSV from: {csv_file_path}")

            # Read the CSV file using pandas
            df = pd.read_csv(csv_file_path)

            # Convert data to appropriate types (numerical values)
            for year in YEARS:
                # Convert years columns to numeric, handling any formatting
                df[year] = pd.to_numeric(df[year].astype(str).str.replace(',', ''), errors='coerce')

            # Initialize the nested dictionary structure
            data = {"Companies": {}}

            # Process each row in the dataframe
            for _, row in df.iterrows():
                sector = row['Sector']
                sub_sector = row['Sub-Sector']
                org_name = row['Org Name']
                indicator = row['Indicator']
                sub_indicator = row['Sub Indicator'] if 'Sub Indicator' in row else None
                sub_sub_indicator = row['Sub-Sub Indicator'] if 'Sub-Sub Indicator' in row else None

                # Create nested structure if not exists
                if sector not in data:
                    data[sector] = {}

                if sub_sector not in data[sector]:
                    data[sector][sub_sector] = {}

                if org_name not in data[sector][sub_sector]:
                    data[sector][sub_sector][org_name] = {}

                # For flat lookups, also add company directly to Companies dict
                if org_name not in data["Companies"]:
                    data["Companies"][org_name] = {}

                # Handle different levels of indicators
                indicator_key = indicator
                if sub_indicator and not pd.isna(sub_indicator):
                    indicator_key = f"{indicator} - {sub_indicator}"
                if sub_sub_indicator and not pd.isna(sub_sub_indicator):
                    indicator_key = f"{indicator_key} - {sub_sub_indicator}"

                # Add the item data to company nested structure
                if indicator_key not in data[sector][sub_sector][org_name]:
                    data[sector][sub_sector][org_name][indicator_key] = {}

                # Add the item to flat structure too
                if indicator_key not in data["Companies"][org_name]:
                    data["Companies"][org_name][indicator_key] = {}

                # Add the yearly values to both structures
                for year in YEARS:
                    # Add to nested structure
                    data[sector][sub_sector][org_name][indicator_key][year] = row[year]

                    # Add to flat structure
                    data["Companies"][org_name][indicator_key][year] = row[year]

            return data

        except Exception as e:
            print(f"Error loading CSV data: {e}")
            # Return empty data structure if file can't be loaded
            return {"Companies": {}}

    @staticmethod
    def get_listed_companies():
        """
        Returns a list of companies listed in the dataset

        Returns:
            list: List of company names
        """
        try:
            csv_file_path = CompanyDataService.get_csv_path()
            df = pd.read_csv(csv_file_path)

            # Get unique company names
            companies = df['Org Name'].unique().tolist()
            return companies

        except Exception as e:
            print(f"Error getting listed companies: {e}")
            return []

    @staticmethod
    def get_sectors():
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
            print(f"Error getting sectors: {e}")
            return []

    @staticmethod
    def get_sub_sectors(sector):
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
            print(f"Error getting sub-sectors: {e}")
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
    def get_indicators():
        """
        Returns a list of available indicators from the CSV file

        Returns:
            list: List of unique indicators
        """
        try:
            csv_file_path = CompanyDataService.get_csv_path()
            df = pd.read_csv(csv_file_path)

            # Get unique indicators
            indicators = df['Indicator'].unique().tolist()
            return indicators

        except Exception as e:
            print(f"Error getting indicators: {e}")
            return []

    @staticmethod
    def get_years():
        """
        Returns a list of available years

        Returns:
            list: List of available years
        """
        return YEARS.copy()

    @staticmethod
    def calculate_financial_ratios(company_data, year="2022"):
        """
        Calculate key financial ratios for a company based on its data

        Args:
            company_data (dict): The company's financial data
            year (str): The year to calculate ratios for

        Returns:
            dict: A dictionary of calculated financial ratios
        """
        ratios = {
            PROFITABILITY_RATIOS: {},
            LIQUIDITY_RATIOS: {},
            EFFICIENCY_RATIOS: {},
            SOLVENCY_RATIOS: {}
        }

        try:
            # Helper function to safely calculate a ratio
            def calculate_ratio(numerator_key, denominator_key, factor=100):
                if (numerator_key in company_data and year in company_data[numerator_key] and
                        denominator_key in company_data and year in company_data[denominator_key] and
                        company_data[denominator_key][year] > 0):
                    numerator = company_data[numerator_key][year]
                    denominator = company_data[denominator_key][year]
                    return round((numerator / denominator) * factor, 2)
                return None

            # Profitability ratios
            # Return on Equity (ROE)
            ratios[PROFITABILITY_RATIOS]["return_on_equity"] = calculate_ratio(
                FINANCIAL_FIELDS["NET_PROFIT"],
                FINANCIAL_FIELDS["TOTAL_EQUITY"]
            )

            # Return on Assets (ROA)
            ratios[PROFITABILITY_RATIOS]["return_on_assets"] = calculate_ratio(
                FINANCIAL_FIELDS["NET_PROFIT"],
                FINANCIAL_FIELDS["TOTAL_ASSETS"]
            )

            # Return on Capital Employed (ROCE)
            if (FINANCIAL_FIELDS["EBIT"] in company_data and year in company_data[FINANCIAL_FIELDS["EBIT"]] and
                    FINANCIAL_FIELDS["TOTAL_ASSETS"] in company_data and year in company_data[
                        FINANCIAL_FIELDS["TOTAL_ASSETS"]] and
                    FINANCIAL_FIELDS["CURRENT_LIABILITIES"] in company_data and year in company_data[
                        FINANCIAL_FIELDS["CURRENT_LIABILITIES"]]):

                ebit = company_data[FINANCIAL_FIELDS["EBIT"]][year]
                total_assets = company_data[FINANCIAL_FIELDS["TOTAL_ASSETS"]][year]
                current_liabilities = company_data[FINANCIAL_FIELDS["CURRENT_LIABILITIES"]][year]

                capital_employed = total_assets - current_liabilities

                if capital_employed > 0:
                    roce = (ebit / capital_employed) * 100
                    ratios[PROFITABILITY_RATIOS]["return_on_capital_employed"] = round(roce, 2)

            # Net Profit Margin
            ratios[PROFITABILITY_RATIOS]["net_profit_margin"] = calculate_ratio(
                FINANCIAL_FIELDS["NET_PROFIT"],
                FINANCIAL_FIELDS["REVENUE"]
            )

            # Liquidity ratios
            # Current Ratio
            ratios[LIQUIDITY_RATIOS]["current_ratio"] = calculate_ratio(
                FINANCIAL_FIELDS["CURRENT_ASSETS"],
                FINANCIAL_FIELDS["CURRENT_LIABILITIES"],
                factor=1  # Not a percentage
            )

            # Quick Ratio
            if (FINANCIAL_FIELDS["CURRENT_ASSETS"] in company_data and year in company_data[
                FINANCIAL_FIELDS["CURRENT_ASSETS"]] and
                    FINANCIAL_FIELDS["INVENTORY"] in company_data and year in company_data[
                        FINANCIAL_FIELDS["INVENTORY"]] and
                    FINANCIAL_FIELDS["CURRENT_LIABILITIES"] in company_data and year in company_data[
                        FINANCIAL_FIELDS["CURRENT_LIABILITIES"]] and
                    company_data[FINANCIAL_FIELDS["CURRENT_LIABILITIES"]][year] > 0):
                current_assets = company_data[FINANCIAL_FIELDS["CURRENT_ASSETS"]][year]
                inventory = company_data[FINANCIAL_FIELDS["INVENTORY"]][year]
                current_liabilities = company_data[FINANCIAL_FIELDS["CURRENT_LIABILITIES"]][year]

                quick_ratio = (current_assets - inventory) / current_liabilities
                ratios[LIQUIDITY_RATIOS]["quick_ratio"] = round(quick_ratio, 2)

            # Efficiency ratios
            # Asset Turnover Ratio
            ratios[EFFICIENCY_RATIOS]["asset_turnover"] = calculate_ratio(
                FINANCIAL_FIELDS["REVENUE"],
                FINANCIAL_FIELDS["TOTAL_ASSETS"],
                factor=1  # Not a percentage
            )

            # Inventory Turnover Ratio
            ratios[EFFICIENCY_RATIOS]["inventory_turnover"] = calculate_ratio(
                FINANCIAL_FIELDS["COGS"],
                FINANCIAL_FIELDS["INVENTORY"],
                factor=1  # Not a percentage
            )

            # Accounts Receivable Turnover Ratio
            ratios[EFFICIENCY_RATIOS]["accounts_receivable_turnover"] = calculate_ratio(
                FINANCIAL_FIELDS["REVENUE"],  # Using revenue as a proxy for credit sales
                FINANCIAL_FIELDS["ACCOUNTS_RECEIVABLE"],
                factor=1  # Not a percentage
            )

            # Accounts Payable Turnover Ratio
            ratios[EFFICIENCY_RATIOS]["accounts_payable_turnover"] = calculate_ratio(
                FINANCIAL_FIELDS["COGS"],  # Using COGS as a proxy for purchases
                FINANCIAL_FIELDS["ACCOUNTS_PAYABLE"],
                factor=1  # Not a percentage
            )

            # Solvency ratios
            # Debt-to-Equity Ratio
            ratios[SOLVENCY_RATIOS]["debt_to_equity"] = calculate_ratio(
                FINANCIAL_FIELDS["TOTAL_DEBT"],
                FINANCIAL_FIELDS["TOTAL_EQUITY"],
                factor=1  # Not a percentage
            )

            # Debt Ratio
            ratios[SOLVENCY_RATIOS]["debt_ratio"] = calculate_ratio(
                FINANCIAL_FIELDS["TOTAL_DEBT"],
                FINANCIAL_FIELDS["TOTAL_ASSETS"]
            )

            # Interest Coverage Ratio
            ratios[SOLVENCY_RATIOS]["interest_coverage"] = calculate_ratio(
                FINANCIAL_FIELDS["EBIT"],
                FINANCIAL_FIELDS["INTEREST_EXPENSE"],
                factor=1  # Not a percentage
            )

            # Equity Ratio
            ratios[SOLVENCY_RATIOS]["equity_ratio"] = calculate_ratio(
                FINANCIAL_FIELDS["TOTAL_EQUITY"],
                FINANCIAL_FIELDS["TOTAL_ASSETS"]
            )

        except Exception as e:
            print(f"Error calculating financial ratios: {e}")

        return ratios

    @staticmethod
    def calculate_ratio_trend(company_data, ratio_type, numerator_key, denominator_key, factor=100, years=None):
        """
        Calculate trend data for a specific ratio over multiple years

        Args:
            company_data (dict): The company's financial data
            ratio_type (str): Type of ratio (e.g., 'ROA', 'Net Profit Margin')
            numerator_key (str): Key for the numerator in company_data
            denominator_key (str): Key for the denominator in company_data
            factor (float): Multiplication factor (e.g., 100 for percentage)
            years (list): List of years to include in trend (defaults to all available)

        Returns:
            dict: A dictionary with years as keys and ratio values as values
        """
        if years is None:
            years = CompanyDataService.get_years()

        trend_data = {}

        for year in years:
            try:
                if (numerator_key in company_data and year in company_data[numerator_key] and
                        denominator_key in company_data and year in company_data[denominator_key] and
                        company_data[denominator_key][year] > 0):

                    numerator = company_data[numerator_key][year]
                    denominator = company_data[denominator_key][year]
                    ratio = (numerator / denominator) * factor
                    trend_data[year] = round(ratio, 2)
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
        ratios = CompanyDataService.calculate_financial_ratios(company_data, year)

        # Get industry data - using sector average if available
        # This would require additional logic to determine the company's sector
        # For now, we'll just use a dummy industry average
        data = CompanyDataService.get_company_data()

        # Assuming we have a way to determine industry averages
        # This might be a weighted average of all companies in the same sector/sub-sector
        # For simplicity, we'll use a placeholder approach
        industry_data = {}
        industry_ratios = {}

        # Try to find the company's sector and get sector averages
        for sector, sub_sectors in data.items():
            if sector == "Companies":
                continue

            for sub_sector, companies in sub_sectors.items():
                if company_data in companies.values():
                    # Found the company's sector, now calculate sector averages
                    # This would be expanded based on actual data structure
                    pass

        # Initialize the scores structure
        ratio_scores = {
            PROFITABILITY_RATIOS: {},
            LIQUIDITY_RATIOS: {},
            EFFICIENCY_RATIOS: {},
            SOLVENCY_RATIOS: {}
        }

        # For each category and ratio, compare with industry and assign score
        for category, category_ratios in ratios.items():
            for ratio_name, ratio_value in category_ratios.items():
                # Skip if ratio is None
                if ratio_value is None:
                    continue

                # If we have industry data, compare with it
                industry_value = None
                if category in industry_ratios and ratio_name in industry_ratios[category]:
                    industry_value = industry_ratios[category].get(ratio_name)

                # If no industry value, use benchmark approach
                if industry_value is None or industry_value == 0:
                    # Assign score based on standard benchmarks for the ratio
                    # This would be expanded with industry-specific benchmarks

                    # For now, use a simplified scoring system
                    # Assigning default scores based on ratio type
                    if category == PROFITABILITY_RATIOS:
                        if ratio_name == "return_on_equity":
                            if ratio_value >= 15:
                                score = 5
                            elif ratio_value >= 10:
                                score = 4
                            elif ratio_value >= 5:
                                score = 3
                            elif ratio_value >= 0:
                                score = 2
                            else:
                                score = 1

                        elif ratio_name == "return_on_assets":
                            if ratio_value >= 10:
                                score = 5
                            elif ratio_value >= 6:
                                score = 4
                            elif ratio_value >= 3:
                                score = 3
                            elif ratio_value >= 0:
                                score = 2
                            else:
                                score = 1

                        elif ratio_name == "return_on_capital_employed":
                            if ratio_value >= 20:
                                score = 5
                            elif ratio_value >= 15:
                                score = 4
                            elif ratio_value >= 10:
                                score = 3
                            elif ratio_value >= 5:
                                score = 2
                            else:
                                score = 1

                        elif ratio_name == "net_profit_margin":
                            if ratio_value >= 20:
                                score = 5
                            elif ratio_value >= 15:
                                score = 4
                            elif ratio_value >= 10:
                                score = 3
                            elif ratio_value >= 5:
                                score = 2
                            else:
                                score = 1
                        else:
                            score = 3  # Default average score

                    elif category == LIQUIDITY_RATIOS:
                        if ratio_name == "current_ratio":
                            if ratio_value >= 2:
                                score = 5
                            elif ratio_value >= 1.5:
                                score = 4
                            elif ratio_value >= 1:
                                score = 3
                            elif ratio_value >= 0.8:
                                score = 2
                            else:
                                score = 1

                        elif ratio_name == "quick_ratio":
                            if ratio_value >= 1.5:
                                score = 5
                            elif ratio_value >= 1:
                                score = 4
                            elif ratio_value >= 0.8:
                                score = 3
                            elif ratio_value >= 0.5:
                                score = 2
                            else:
                                score = 1
                        else:
                            score = 3  # Default average score

                    elif category == EFFICIENCY_RATIOS:
                        # Higher is generally better for efficiency ratios
                        if ratio_value > 1:
                            score = 4
                        elif ratio_value > 0.75:
                            score = 3
                        elif ratio_value > 0.5:
                            score = 2
                        else:
                            score = 1

                    elif category == SOLVENCY_RATIOS:
                        if ratio_name == "debt_to_equity":
                            # Lower is better
                            if ratio_value < 0.5:
                                score = 5
                            elif ratio_value < 1:
                                score = 4
                            elif ratio_value < 1.5:
                                score = 3
                            elif ratio_value < 2:
                                score = 2
                            else:
                                score = 1

                        elif ratio_name == "interest_coverage":
                            # Higher is better
                            if ratio_value > 5:
                                score = 5
                            elif ratio_value > 3:
                                score = 4
                            elif ratio_value > 2:
                                score = 3
                            elif ratio_value > 1:
                                score = 2
                            else:
                                score = 1

                        elif ratio_name in ["debt_ratio"]:
                            # Lower is better
                            if ratio_value < 0.3:
                                score = 5
                            elif ratio_value < 0.4:
                                score = 4
                            elif ratio_value < 0.5:
                                score = 3
                            elif ratio_value < 0.6:
                                score = 2
                            else:
                                score = 1

                        elif ratio_name == "equity_ratio":
                            # Higher is better
                            if ratio_value > 0.6:
                                score = 5
                            elif ratio_value > 0.5:
                                score = 4
                            elif ratio_value > 0.4:
                                score = 3
                            elif ratio_value > 0.3:
                                score = 2
                            else:
                                score = 1
                        else:
                            score = 3  # Default average score
                    else:
                        score = 3  # Default average score
                else:
                    # Calculate company-to-industry ratio
                    # For ratios where lower is better, we invert the comparison
                    if ratio_name in INVERSE_RATIOS:
                        # For these ratios, lower is better, so we invert
                        comparison_ratio = industry_value / ratio_value if ratio_value > 0 else 0
                    else:
                        # For these ratios, higher is better
                        comparison_ratio = ratio_value / industry_value if industry_value > 0 else 0

                    # Assign score based on comparison ratio
                    score = 1  # Default to worst score
                    for level, criteria in BENCHMARK_SCORING.items():
                        if comparison_ratio >= criteria["threshold"]:
                            score = criteria["score"]
                            break

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
        for category, score in category_scores.items():
            category_weight_key = category.replace("_ratios", "")
            weighted_score += score * weights.get(category_weight_key, 0)

        percentage_score = (weighted_score / 5) * 100

        # Determine rating based on percentage score
        rating = "Not Rated"
        for threshold, rating_value in sorted(RATING_THRESHOLDS.items(), reverse=True):
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
                "industry_ratios": industry_ratios
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
            result[company] = {}

            for indicator in indicators:
                if indicator in company_data and year in company_data[indicator]:
                    result[company][indicator] = company_data[indicator][year]
                else:
                    result[company][indicator] = None

        # You could add industry averages here if available
        # For now, we'll skip this since it depends on sector classification

        return result