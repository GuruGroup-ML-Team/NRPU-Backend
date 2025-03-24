# bank_api/services.py
import os
import pandas as pd
from django.conf import settings
from apps.bank_api.constants import (
    BANK_CSV_FILENAME, BANK_YEARS, BANK_EFFICIENCY_RATIOS, BANK_LIQUIDITY_RATIOS,
    BANK_ASSET_QUALITY_RATIOS, BANK_CAPITAL_RATIOS, BANK_BENCHMARK_SCORING,
    BANK_RATING_THRESHOLDS, BANK_FINANCIAL_FIELDS, BANK_INVERSE_RATIOS
)


class BankDataService:
    """Service for handling bank financial data operations"""

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
            os.path.join(base_dir, BANK_CSV_FILENAME),  # Project root
            os.path.join(base_dir, 'bank_api', BANK_CSV_FILENAME),
            os.path.join(base_dir, 'data', BANK_CSV_FILENAME),
        ]

        # Return the first path that exists
        for path in possible_paths:
            if os.path.exists(path):
                return path

        # Default path if none exist
        return os.path.join(base_dir, BANK_CSV_FILENAME)

    @staticmethod
    def get_bank_data():
        """
        Load and process bank data from CSV

        Returns:
            dict: Processed bank data in nested dictionary format
        """
        try:
            # Get the path to the CSV file
            csv_file_path = BankDataService.get_csv_path()
            print(f"Attempting to load CSV from: {csv_file_path}")

            # Read the CSV file using pandas
            df = pd.read_csv(csv_file_path)

            # Convert data to appropriate types (numerical values)
            for year in BANK_YEARS:
                df[year] = pd.to_numeric(df[year].str.replace(',', ''), errors='coerce')

            # Initialize the nested dictionary structure
            data = {"Banks": {}}

            # Process each row in the dataframe
            for _, row in df.iterrows():
                org_name = row['Org Name']
                item_name = row['Item Name']

                # Create the organization if it doesn't exist yet
                if org_name not in data["Banks"]:
                    data["Banks"][org_name] = {}

                # Add the item data
                if item_name not in data["Banks"][org_name]:
                    data["Banks"][org_name][item_name] = {}

                # Add the yearly values
                for year in BANK_YEARS:
                    data["Banks"][org_name][item_name][year] = row[year]

            return data

        except Exception as e:
            print(f"Error loading CSV data: {e}")
            # Return empty data structure if file can't be loaded
            return {"Banks": {}}

    @staticmethod
    def get_listed_banks():
        """
        Returns a list of banks listed in the stock exchange

        Returns:
            list: List of bank names excluding 'All Banks'
        """
        try:
            csv_file_path = BankDataService.get_csv_path()
            df = pd.read_csv(csv_file_path)

            # Get unique bank names, excluding 'All Banks'
            banks = df[df['Org Name'] != 'All Banks']['Org Name'].unique().tolist()
            return banks

        except Exception as e:
            print(f"Error getting listed banks: {e}")
            return []

    @staticmethod
    def get_sectors():
        """
        Returns a list of all sectors from the CSV file

        Returns:
            list: List of unique sector names
        """
        try:
            csv_file_path = BankDataService.get_csv_path()
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
            csv_file_path = BankDataService.get_csv_path()
            df = pd.read_csv(csv_file_path)

            # Filter by sector and get unique sub-sectors
            sub_sectors = df[df['Sector'] == sector]['Sub Sector'].unique().tolist()
            return sub_sectors

        except Exception as e:
            print(f"Error getting sub-sectors: {e}")
            return []

    @staticmethod
    def get_banks_by_sub_sector(sub_sector):
        """
        Returns a list of banks for a given sub-sector

        Args:
            sub_sector (str): Sub-sector name

        Returns:
            list: List of bank names
        """
        try:
            csv_file_path = BankDataService.get_csv_path()
            df = pd.read_csv(csv_file_path)

            # Filter by sub-sector and get unique bank names
            banks = df[df['Sub Sector'] == sub_sector]['Org Name'].unique().tolist()
            return banks

        except Exception as e:
            print(f"Error getting banks by sub-sector: {e}")
            return []

    @staticmethod
    def get_metrics():
        """
        Returns a list of available metrics (item names) from the CSV file

        Returns:
            list: List of unique metrics
        """
        try:
            csv_file_path = BankDataService.get_csv_path()
            df = pd.read_csv(csv_file_path)

            # Get unique item names
            metrics = df['Item Name'].unique().tolist()
            return metrics

        except Exception as e:
            print(f"Error getting metrics: {e}")
            return []

    @staticmethod
    def get_years():
        """
        Returns a list of available years

        Returns:
            list: List of available years
        """
        return BANK_YEARS.copy()

    @staticmethod
    def calculate_financial_ratios(bank_data, year="2023"):
        """
        Calculate key financial ratios for a bank based on its data

        Args:
            bank_data (dict): The bank's financial data
            year (str): The year to calculate ratios for

        Returns:
            dict: A dictionary of calculated financial ratios
        """
        ratios = {
            BANK_EFFICIENCY_RATIOS: {},
            BANK_LIQUIDITY_RATIOS: {},
            BANK_ASSET_QUALITY_RATIOS: {},
            BANK_CAPITAL_RATIOS: {}
        }

        try:
            # Helper function to safely calculate a ratio
            def calculate_ratio(numerator_key, denominator_key, factor=100):
                if (numerator_key in bank_data and year in bank_data[numerator_key] and
                        denominator_key in bank_data and year in bank_data[denominator_key] and
                        bank_data[denominator_key][year] > 0):
                    numerator = bank_data[numerator_key][year]
                    denominator = bank_data[denominator_key][year]
                    return round((numerator / denominator) * factor, 2)
                return None

            # Efficiency ratios
            # Spread Ratio
            ratios[BANK_EFFICIENCY_RATIOS]["spread_ratio"] = calculate_ratio(
                BANK_FINANCIAL_FIELDS["NET_INTEREST"],
                BANK_FINANCIAL_FIELDS["INTEREST_EARNED"]
            )

            # Net Interest Margin
            ratios[BANK_EFFICIENCY_RATIOS]["net_interest_margin"] = calculate_ratio(
                BANK_FINANCIAL_FIELDS["NET_INTEREST"],
                BANK_FINANCIAL_FIELDS["TOTAL_ASSETS"]
            )

            # Return on Equity (ROE)
            ratios[BANK_EFFICIENCY_RATIOS]["return_on_equity"] = calculate_ratio(
                BANK_FINANCIAL_FIELDS["NET_PROFIT"],
                BANK_FINANCIAL_FIELDS["TOTAL_EQUITY"]
            )

            # Return on Assets (ROA)
            ratios[BANK_EFFICIENCY_RATIOS]["return_on_assets"] = calculate_ratio(
                BANK_FINANCIAL_FIELDS["NET_PROFIT"],
                BANK_FINANCIAL_FIELDS["TOTAL_ASSETS"]
            )

            # Non-Interest Income Ratio
            ratios[BANK_EFFICIENCY_RATIOS]["non_interest_income_ratio"] = calculate_ratio(
                BANK_FINANCIAL_FIELDS["NON_INTEREST_INCOME"],
                BANK_FINANCIAL_FIELDS["TOTAL_ASSETS"]
            )

            # Liquidity ratios
            # Cash to Total Assets
            if (BANK_FINANCIAL_FIELDS["CASH"] in bank_data and year in bank_data[BANK_FINANCIAL_FIELDS["CASH"]] and
                    BANK_FINANCIAL_FIELDS["BALANCES"] in bank_data and year in bank_data[BANK_FINANCIAL_FIELDS["BALANCES"]] and
                    BANK_FINANCIAL_FIELDS["TOTAL_ASSETS"] in bank_data and year in bank_data[
                        BANK_FINANCIAL_FIELDS["TOTAL_ASSETS"]] and
                    bank_data[BANK_FINANCIAL_FIELDS["TOTAL_ASSETS"]][year] > 0):
                cash = bank_data[BANK_FINANCIAL_FIELDS["CASH"]][year]
                balances = bank_data[BANK_FINANCIAL_FIELDS["BALANCES"]][year]
                total_assets = bank_data[BANK_FINANCIAL_FIELDS["TOTAL_ASSETS"]][year]
                cash_ratio = ((cash + balances) / total_assets) * 100
                ratios[BANK_LIQUIDITY_RATIOS]["cash_to_total_assets"] = round(cash_ratio, 2)

            # Investments to Total Assets
            ratios[BANK_LIQUIDITY_RATIOS]["investments_to_total_assets"] = calculate_ratio(
                BANK_FINANCIAL_FIELDS["INVESTMENTS"],
                BANK_FINANCIAL_FIELDS["TOTAL_ASSETS"]
            )

            # Advances to Total Assets
            ratios[BANK_LIQUIDITY_RATIOS]["advances_to_total_assets"] = calculate_ratio(
                BANK_FINANCIAL_FIELDS["NET_ADVANCES"],
                BANK_FINANCIAL_FIELDS["TOTAL_ASSETS"]
            )

            # Deposits to Total Assets
            ratios[BANK_LIQUIDITY_RATIOS]["deposits_to_total_assets"] = calculate_ratio(
                BANK_FINANCIAL_FIELDS["DEPOSITS"],
                BANK_FINANCIAL_FIELDS["TOTAL_ASSETS"]
            )

            # Total Liabilities to Total Assets
            ratios[BANK_LIQUIDITY_RATIOS]["liabilities_to_total_assets"] = calculate_ratio(
                BANK_FINANCIAL_FIELDS["TOTAL_LIABILITIES"],
                BANK_FINANCIAL_FIELDS["TOTAL_ASSETS"]
            )

            # Advances to Deposits
            ratios[BANK_LIQUIDITY_RATIOS]["advances_to_deposits"] = calculate_ratio(
                BANK_FINANCIAL_FIELDS["NET_ADVANCES"],
                BANK_FINANCIAL_FIELDS["DEPOSITS"]
            )

            # Gross Advances to Deposits
            ratios[BANK_LIQUIDITY_RATIOS]["gross_advances_to_deposits"] = calculate_ratio(
                BANK_FINANCIAL_FIELDS["GROSS_ADVANCES"],
                BANK_FINANCIAL_FIELDS["DEPOSITS"]
            )

            # Gross Advances to Borrowing & Deposits
            if (BANK_FINANCIAL_FIELDS["GROSS_ADVANCES"] in bank_data and year in bank_data[
                BANK_FINANCIAL_FIELDS["GROSS_ADVANCES"]] and
                    BANK_FINANCIAL_FIELDS["BORROWINGS"] in bank_data and year in bank_data[
                        BANK_FINANCIAL_FIELDS["BORROWINGS"]] and
                    BANK_FINANCIAL_FIELDS["DEPOSITS"] in bank_data and year in bank_data[BANK_FINANCIAL_FIELDS["DEPOSITS"]] and
                    (bank_data[BANK_FINANCIAL_FIELDS["BORROWINGS"]][year] + bank_data[BANK_FINANCIAL_FIELDS["DEPOSITS"]][
                        year]) > 0):
                gross_advances = bank_data[BANK_FINANCIAL_FIELDS["GROSS_ADVANCES"]][year]
                borrowings = bank_data[BANK_FINANCIAL_FIELDS["BORROWINGS"]][year]
                deposits = bank_data[BANK_FINANCIAL_FIELDS["DEPOSITS"]][year]
                ratio_value = (gross_advances / (borrowings + deposits)) * 100
                ratios[BANK_LIQUIDITY_RATIOS]["gross_advances_to_borrowing_deposits"] = round(ratio_value, 2)

            # Asset quality ratios
            # NPL to Gross Advances
            ratios[BANK_ASSET_QUALITY_RATIOS]["npl_to_gross_advances"] = calculate_ratio(
                BANK_FINANCIAL_FIELDS["NPL"],
                BANK_FINANCIAL_FIELDS["GROSS_ADVANCES"]
            )

            # Provisions against NPLs to Gross Advances
            ratios[BANK_ASSET_QUALITY_RATIOS]["provisions_to_gross_advances"] = calculate_ratio(
                BANK_FINANCIAL_FIELDS["PROVISIONS"],
                BANK_FINANCIAL_FIELDS["GROSS_ADVANCES"]
            )

            # Provision Coverage
            ratios[BANK_ASSET_QUALITY_RATIOS]["provision_coverage"] = calculate_ratio(
                BANK_FINANCIAL_FIELDS["PROVISIONS"],
                BANK_FINANCIAL_FIELDS["NPL"]
            )

            # NPL to Equity
            ratios[BANK_ASSET_QUALITY_RATIOS]["npl_to_equity"] = calculate_ratio(
                BANK_FINANCIAL_FIELDS["NPL"],
                BANK_FINANCIAL_FIELDS["TOTAL_EQUITY"]
            )

            # Capital ratios
            # Capital to Assets Ratio
            ratios[BANK_CAPITAL_RATIOS]["capital_to_assets"] = calculate_ratio(
                BANK_FINANCIAL_FIELDS["TOTAL_EQUITY"],
                BANK_FINANCIAL_FIELDS["TOTAL_ASSETS"]
            )

            # Deposits to Equity
            deposits_equity = calculate_ratio(
                BANK_FINANCIAL_FIELDS["DEPOSITS"],
                BANK_FINANCIAL_FIELDS["TOTAL_EQUITY"],
                factor=1  # No percentage conversion for this ratio
            )
            if deposits_equity is not None:
                ratios[BANK_CAPITAL_RATIOS]["deposits_to_equity"] = deposits_equity

        except Exception as e:
            print(f"Error calculating financial ratios: {e}")

        return ratios

    @staticmethod
    def calculate_ratio_trend(bank_data, ratio_type, numerator_key, denominator_key, factor=100, years=None):
        """
        Calculate trend data for a specific ratio over multiple years

        Args:
            bank_data (dict): The bank's financial data
            ratio_type (str): Type of ratio (e.g., 'ROA', 'Net Interest Margin')
            numerator_key (str): Key for the numerator in bank_data
            denominator_key (str): Key for the denominator in bank_data
            factor (float): Multiplication factor (e.g., 100 for percentage)
            years (list): List of years to include in trend (defaults to all available)

        Returns:
            dict: A dictionary with years as keys and ratio values as values
        """
        if years is None:
            years = BankDataService.get_years()

        trend_data = {}

        for year in years:
            try:
                if (numerator_key in bank_data and year in bank_data[numerator_key] and
                        denominator_key in bank_data and year in bank_data[denominator_key] and
                        bank_data[denominator_key][year] > 0):

                    numerator = bank_data[numerator_key][year]
                    denominator = bank_data[denominator_key][year]
                    ratio = (numerator / denominator) * factor
                    trend_data[year] = round(ratio, 2)
                else:
                    trend_data[year] = None
            except (KeyError, TypeError, ZeroDivisionError):
                trend_data[year] = None

        return trend_data

    @staticmethod
    def calculate_bank_score(bank_data, weights, year="2023"):
        """
        Calculate an overall financial health score for a bank

        Args:
            bank_data (dict): The bank's financial data
            weights (dict): Dictionary with category weights
            year (str): The year to calculate score for

        Returns:
            dict: Score details including category scores and overall rating
        """
        # Calculate all ratios first
        ratios = BankDataService.calculate_financial_ratios(bank_data, year)

        # Get industry data (All Banks)
        data = BankDataService.get_bank_data()
        industry_data = data["Banks"].get("All Banks", {})
        industry_ratios = BankDataService.calculate_financial_ratios(industry_data, year)

        # Initialize the scores structure
        ratio_scores = {
            BANK_EFFICIENCY_RATIOS: {},
            BANK_LIQUIDITY_RATIOS: {},
            BANK_ASSET_QUALITY_RATIOS: {},
            BANK_CAPITAL_RATIOS: {}
        }

        # For each category and ratio, compare with industry and assign score
        for category, category_ratios in ratios.items():
            for ratio_name, ratio_value in category_ratios.items():
                # Skip if ratio is None or no industry data
                if ratio_value is None or category not in industry_ratios or ratio_name not in industry_ratios[
                    category]:
                    continue

                industry_value = industry_ratios[category].get(ratio_name)
                if industry_value is None or industry_value == 0:
                    continue

                # Calculate bank-to-industry ratio
                # For ratios where lower is better, we invert the comparison
                if ratio_name in BANK_INVERSE_RATIOS:
                    # For these ratios, lower is better, so we invert
                    comparison_ratio = industry_value / ratio_value if ratio_value > 0 else 0
                else:
                    # For these ratios, higher is better
                    comparison_ratio = ratio_value / industry_value if industry_value > 0 else 0

                # Assign score based on comparison ratio
                score = 1  # Default to worst score
                for level, criteria in BANK_BENCHMARK_SCORING.items():
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
        for threshold, rating_value in sorted(BANK_RATING_THRESHOLDS.items(), reverse=True):
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
                "bank_ratios": ratios,
                "industry_ratios": industry_ratios
            }
        }

    @staticmethod
    def get_bank_comparison_data(banks, metrics, year="2023"):
        """
        Get comparison data for multiple banks on specified metrics

        Args:
            banks (list): List of bank names to compare
            metrics (list): List of metrics to compare
            year (str): Year for comparison

        Returns:
            dict: Comparison data organized by bank and metric
        """
        data = BankDataService.get_bank_data()
        result = {}

        for bank in banks:
            if bank not in data["Banks"]:
                continue

            bank_data = data["Banks"][bank]
            result[bank] = {}

            for metric in metrics:
                if metric in bank_data and year in bank_data[metric]:
                    result[bank][metric] = bank_data[metric][year]
                else:
                    result[bank][metric] = None

        if "All Banks" in data["Banks"]:
            all_banks_data = data["Banks"]["All Banks"]
            result["Industry Average"] = {}

            for metric in metrics:
                if metric in all_banks_data and year in all_banks_data[metric]:
                    result["Industry Average"][metric] = all_banks_data[metric][year]
                else:
                    result["Industry Average"][metric] = None

        return result