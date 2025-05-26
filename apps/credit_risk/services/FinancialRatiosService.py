# project_root/credit_risk/services/logic_three_service.py

import pandas as pd
# Import instances of previously defined services to fetch data
# from credit_risk.services.FinancialVariablesService import financial_variables_service_instance
from .FinancialVariablesService import financial_variables_service_instance

class FinancialRatiosCalculator:
    """
    Base class for calculating financial ratios. Provides common utilities for
    handling extracted financial data and calculating ratios across years.
    """
    def __init__(self, extracted_data: dict, target_year: str = None):
        """
        Initializes the calculator with extracted data and target year.

        Args:
            extracted_data (dict): A dictionary containing financial variables,
                                   typically fetched by FinancialVariablesService.
            target_year (str, optional): The year for which to calculate ratios.
                                         Can be an integer year (as string) or 'all'.
                                         Defaults to None (which implies 'all').
        """
        self.extracted_data = extracted_data
        self.target_year = target_year
        self.ratios = {}  # Initialize an empty dictionary to store calculated ratios

    def _calculate_ratio(self, ratio_func, data: dict, year_input=None):
        """
        Helper function to calculate a single ratio for a given year or all years.

        Args:
            ratio_func (callable): A function that takes data (dict) and a single year (int)
                                   and returns the calculated ratio for that year.
            data (dict): The extracted financial variables.
            year_input (str, optional): The year for which to calculate ratios.
                                        Can be an integer year (as string) or 'all'.
                                        Defaults to None.

        Returns:
            dict or float or None: A dictionary of year-to-ratio mappings if 'all' years
                                   are requested, or a single float/None if a specific
                                   year is requested. Returns None if calculation fails.
        """
        if year_input is None or str(year_input).lower() == 'all':
            # Collect all unique years present in the extracted data
            years = set()
            for var_name in data:
                if isinstance(data.get(var_name), dict):
                    years.update(data[var_name].keys())
            
            result = {}
            for y in sorted(list(years)): # Sort years for consistent output
                try:
                    # Ensure year 'y' is an integer for ratio_func
                    calculated_val = ratio_func(data, int(y))
                    result[y] = calculated_val if pd.notna(calculated_val) else None # Handle NaN
                except Exception as e:
                    print(f"Error calculating ratio for year {y}: {e}")
                    result[y] = None
            return result
        else:
            try:
                # Convert the target_year to an integer for calculation
                year_int = int(year_input)
                calculated_val = ratio_func(data, year_int)
                return calculated_val if pd.notna(calculated_val) else None # Handle NaN
            except ValueError:
                print(f"Error: target_year '{year_input}' cannot be converted to an integer.")
                return None
            except Exception as e:
                print(f"Error calculating ratio for year {year_input}: {e}")
                return None

    def calculate_ratios(self):
        """
        Calculates all financial ratios. This is the main entry point for ratio calculation.
        Subclasses must implement this method.
        """
        raise NotImplementedError("Subclasses must implement this method")

    def get_ratios(self) -> dict:
        """
        Returns the calculated ratios.
        """
        return self.ratios


class CompanyFinancialRatiosCalculator(FinancialRatiosCalculator):
    """
    Calculates financial ratios specifically for companies.
    """
    def __init__(self, extracted_data: dict, target_year: str = None):
        super().__init__(extracted_data, target_year)
        self.ratios = {
            "Profitability Ratios": {},
            "Efficiency Ratios": {},
            "Liquidity Ratios": {},
            "Solvency Ratios": {},
        }

    def calculate_ratios(self):
        """
        Calculates financial ratios for companies based on the extracted data.
        """
        data = self.extracted_data
        year = self.target_year

        # --- Profitability Ratios ---
        def calculate_net_profit_margin(data, year):
            return data.get("NET_PROFIT_MARGIN", {}).get(year)
        self.ratios["Profitability Ratios"]["Net Profit Margin"] = self._calculate_ratio(calculate_net_profit_margin, data, year)

        def calculate_roa(data, year):
            return data.get("RETURN_ON_ASSETS", {}).get(year)
        self.ratios["Profitability Ratios"]["Return On Assets"] = self._calculate_ratio(calculate_roa, data, year)

        def calculate_roe(data, year):
            return data.get("RETURN_ON_EQUITY", {}).get(year)
        self.ratios["Profitability Ratios"]["Return On Equity"] = self._calculate_ratio(calculate_roe, data, year)

        def calculate_gpm(data, year):
            return data.get("GROSS_PROFIT_MARGIN",{}).get(year)
        self.ratios["Profitability Ratios"]["Gross Profit Margin"] = self._calculate_ratio(calculate_gpm, data, year)

        def calculate_oroa(data, year):
            return data.get("OPERATING_RETURN_ON_ASSETS",{}).get(year)
        self.ratios["Profitability Ratios"]["Operating Return On Assets"] = self._calculate_ratio(calculate_oroa, data, year)

        def calculate_roce(data, year):
            return data.get("RETURN_ON_CAPITAL_EMPLOYED",{}).get(year)
        self.ratios["Profitability Ratios"]["Return On Capital Employed"] = self._calculate_ratio(calculate_roce, data, year)

        # --- Liquidity Ratios ---
        def calculate_current_ratio(data, year):
            return data.get("CURRENT_RATIO", {}).get(year)
        self.ratios["Liquidity Ratios"]["Current Ratio"] = self._calculate_ratio(calculate_current_ratio, data, year)

        def calculate_quick_ratio(data, year):
            return data.get("QUICK_RATIO", {}).get(year)
        self.ratios["Liquidity Ratios"]["Quick Ratio"] = self._calculate_ratio(calculate_quick_ratio, data, year)

        def calculate_cash_to_current_liabilities_ratio(data, year):
            return data.get("CASH_TO_CURRENT_LIABILITIES_RATIO", {}).get(year)
        self.ratios["Liquidity Ratios"]["Cash To Current Liabilities Ratio"] = self._calculate_ratio(calculate_cash_to_current_liabilities_ratio, data, year)

        # --- Efficiency Ratios ---
        def calculate_no_of_days_in_inventory(data, year):
            return data.get("NUM_OF_DAYS_IN_INVENTORY", {}).get(year)
        self.ratios["Efficiency Ratios"]["Num Of Days In Inventory"] = self._calculate_ratio(calculate_no_of_days_in_inventory, data, year)

        def calculate_no_of_days_in_receivables(data, year):
            return data.get("NUM_OF_DAYS_IN_RECEIVABLES", {}).get(year)
        self.ratios["Efficiency Ratios"]["Num Of Days In Receivables"] = self._calculate_ratio(calculate_no_of_days_in_receivables, data, year)

        def calculate_no_of_days_in_payable(data, year):
            return data.get("NUM_OF_DAYS_IN_PAYABLE", {}).get(year)
        self.ratios["Efficiency Ratios"]["Num Of Days In Payable"] = self._calculate_ratio(calculate_no_of_days_in_payable, data, year)

        # --- Solvency Ratios ---
        def calculate_debt_equity_ratio(data, year):
            return data.get("DEBT_EQUITY_RATIO", {}).get(year)
        self.ratios["Solvency Ratios"]["Debt Equity Ratio"] = self._calculate_ratio(calculate_debt_equity_ratio, data, year)

        def calculate_debt_assets_ratio(data, year):
            return data.get("DEBT_TO_ASSETS_RATIO", {}).get(year)
        self.ratios["Solvency Ratios"]["Debt Asset Ratio"] = self._calculate_ratio(calculate_debt_assets_ratio, data, year)

        def calculate_debt_capital_ratio(data, year):
            return data.get("DEBT_TO_CAPITAL_RATIO", {}).get(year)
        self.ratios["Solvency Ratios"]["Debt Capital Ratio"] = self._calculate_ratio(calculate_debt_capital_ratio, data, year)

        def calculate_interest_coverage_ratio(data, year):
            return data.get("INTEREST_COVER_RATIO", {}).get(year)
        self.ratios["Solvency Ratios"]["Interest Coverage Ratio"] = self._calculate_ratio(calculate_interest_coverage_ratio, data, year)


class BankFinancialRatiosCalculator(FinancialRatiosCalculator):
    """
    Calculates financial ratios specifically for banks.
    """
    def __init__(self, extracted_data: dict, target_year: str = None):
        super().__init__(extracted_data, target_year)
        self.ratios = {
            "Profitability And Efficiency Ratios": {},
            "Liquidity Ratios": {},
            "Asset Quality Ratios": {},
            "Solvency Ratios": {}
        }

    def calculate_ratios(self):
        """
        Calculates financial ratios for banks based on the extracted data.
        """
        data = self.extracted_data
        year = self.target_year

        # --- Profitability And Efficiency Ratios ---
        def calculate_spread_ratio(data, year):
            return data.get("SPREAD_RATIO", {}).get(year)
        self.ratios["Profitability And Efficiency Ratios"]["Spread Ratio"] = self._calculate_ratio(calculate_spread_ratio, data, year)

        def calculate_net_interest_margin(data, year):
            return data.get("NET_INTEREST_MARGIN", {}).get(year)
        self.ratios["Profitability And Efficiency Ratios"]["Net Interest Margin"] = self._calculate_ratio(calculate_net_interest_margin, data, year)

        def calculate_return_on_equity(data, year):
            return data.get("RETURN_ON_EQUITY", {}).get(year)
        self.ratios["Profitability And Efficiency Ratios"]["Return On Equity"] = self._calculate_ratio(calculate_return_on_equity, data, year)

        def calculate_return_on_assets(data, year):
            return data.get("RETURN_ON_ASSETS", {}).get(year)
        self.ratios["Profitability And Efficiency Ratios"]["Return On Assets"] = self._calculate_ratio(calculate_return_on_assets, data, year)

        def calculate_non_interest_income_ratio(data, year):
            return data.get("NON_INTEREST_INCOME_RATIO", {}).get(year)
        self.ratios["Profitability And Efficiency Ratios"]["Non Interest Income Ratio"] = self._calculate_ratio(calculate_non_interest_income_ratio, data, year)

        # --- Liquidity Ratios ---
        def calculate_cash_to_total_assets_ratio(data, year):
            return data.get("CASH_TO_TOTAL_ASSETS_RATIO", {}).get(year)
        self.ratios["Liquidity Ratios"]["Cash To Total Assets Ratio"] = self._calculate_ratio(calculate_cash_to_total_assets_ratio, data, year)

        def calculate_investment_to_total_assets(data, year):
            return data.get("INVESTMENT_TO_TOTAL_ASSETS", {}).get(year)
        self.ratios["Liquidity Ratios"]["Investment To Total Assets"] = self._calculate_ratio(calculate_investment_to_total_assets, data, year)

        def calculate_advances_to_total_assets(data, year):
            return data.get("ADVANCES_TO_TOTAL_ASSETS", {}).get(year)
        self.ratios["Liquidity Ratios"]["Advances To Total Assets"] = self._calculate_ratio(calculate_advances_to_total_assets, data, year)

        def calculate_deposits_to_total_assets(data, year):
            return data.get("DEPOSIT_TO_TOTAL_ASSETS", {}).get(year)
        self.ratios["Liquidity Ratios"]["Deposits To Total Assets"] = self._calculate_ratio(calculate_deposits_to_total_assets, data, year)

        def calculate_total_liabilities_to_total_assets(data, year):
            return data.get("TOTAL_LIABILITIES_TO_TOTAL_ASSETS", {}).get(year)
        self.ratios["Liquidity Ratios"]["Total Liabilities To Total Assets"] = self._calculate_ratio(calculate_total_liabilities_to_total_assets, data, year)

        def calculate_gross_advances_to_deposit(data, year):
            return data.get("GROSS_ADVANCES_TO_DEPOSITS", {}).get(year)
        self.ratios["Liquidity Ratios"]["Gross Advances To Deposits"] = self._calculate_ratio(calculate_gross_advances_to_deposit, data, year)

        def calculate_gross_advances_to_borrowing_and_deposit(data, year):
            return data.get("GROSS_ADVANCES_TO_BORROWING_AND_DEPOSIT", {}).get(year)
        self.ratios["Liquidity Ratios"]["Gross Advances To Borrowing And Deposits"] = self._calculate_ratio(calculate_gross_advances_to_borrowing_and_deposit, data, year)

        # ASSETS QUALITY RATIOS
        def calculate_non_performing_loans_to_gross_advances(data, year):
            return data.get("NON_PERFORMING_LOANS_TO_GROSS_ADVANCES", {}).get(year)
        self.ratios["Asset Quality Ratios"]["Non-Performing Loans to Gross Advances"] = self._calculate_ratio(calculate_non_performing_loans_to_gross_advances, data, year)

        def calculate_provisions_against_npls_to_gross_advances(data, year):
            return data.get("PROVISION_AGAINST_NPLS_TO_GROSS_ADVANCES", {}).get(year)
        self.ratios["Asset Quality Ratios"]["Provisions Against NPLs to Gross Advances"] = self._calculate_ratio(calculate_provisions_against_npls_to_gross_advances, data, year)

        def calculate_npl_to_total_equity(data, year):
            return data.get("NPL_TO_TOTAL_EQUITY", {}).get(year)
        self.ratios["Asset Quality Ratios"]["NPL to Total Equity"] = self._calculate_ratio(calculate_npl_to_total_equity, data, year)

        # --- Solvency Ratios ---
        def calculate_capital_ratio(data, year):
            return data.get("CAPITAL_RATIO", {}).get(year)
        self.ratios["Solvency Ratios"]["Capital Ratio"] = self._calculate_ratio(calculate_capital_ratio, data, year)

        def calculate_total_deposit_to_equity_ratio(data, year):
            return data.get("TOTAL_DEPOSIT_TO_EQUITY_RATIO", {}).get(year)
        self.ratios["Solvency Ratios"]["Total deposit to equity Ratio"] = self._calculate_ratio(calculate_total_deposit_to_equity_ratio, data, year)


class FinancialRatiosService:
    """
    Service layer for calculating financial ratios for both companies and banks.
    It orchestrates data fetching from FinancialVariablesService and then applies
    the appropriate ratio calculation logic.
    """
    def calculate_financial_ratios_for_specific_entity(self, entity_type: str, sector: str = None, sub_sector: str = None, org_name: str = None, target_year: str = None) -> dict:
        """
        Calculates financial ratios for a specific organization based on extracted data.

        Args:
            entity_type (str): The type of entity ("company" or "bank").
            sector (str): The sector of the organization.
            sub_sector (str): The sub-sector of the organization.
            org_name (str): The name of the organization.
            target_year (str, optional): The year for which to calculate ratios.
                                         If 'all', calculates for all available years. Defaults to None.

        Returns:
            dict: A dictionary containing the calculated ratios, categorized by type.
                  Returns an empty dictionary if no data is fetched or ratios cannot be calculated.
        """
        # Fetch specific variables for the organization using the FinancialVariablesService
        extracted_data = financial_variables_service_instance.get_specific_variables_for_specific_org(
            entity_type=entity_type,
            sector=sector,
            sub_sector=sub_sector,
            org_name=org_name,
            target_year=target_year # Pass target_year to filter variables
        )

        if not extracted_data: # Check if the dictionary is empty or None
            print(f"No specific financial variables found for {org_name} in {sector} {sub_sector} for year {target_year}.")
            return {}

        calculator = None
        if entity_type.lower() == "company":
            calculator = CompanyFinancialRatiosCalculator(extracted_data, target_year)
        elif entity_type.lower() == "bank":
            calculator = BankFinancialRatiosCalculator(extracted_data, target_year)
        else:
            print(f"Error: Invalid entity type: {entity_type}. Must be 'company' or 'bank'.")
            return {}

        calculator.calculate_ratios()
        return calculator.get_ratios()

    def calculate_financial_ratios_for_specific_sector(self, entity_type: str, sector: str, target_year: str = None) -> dict:
        """
        Calculates the average financial ratios for all organizations within a given sector
        (including all sub-sectors).

        Args:
            entity_type (str): The type of entity ("company" or "bank").
            sector (str): The sector for which to calculate average ratios.
            target_year (str, optional): The year for which to calculate ratios.
                                         If 'all', calculates for all available years. Defaults to None.

        Returns:
            dict: A dictionary containing the calculated average ratios, categorized by type.
                  Returns an empty dictionary if no data is fetched or ratios cannot be calculated.
        """
        # Fetch aggregated variables for the sector using the FinancialVariablesService
        sector_data = financial_variables_service_instance.get_specific_variables_by_sector(
            entity_type=entity_type,
            sector=sector,
            target_year=target_year # Pass target_year to filter variables
        )

        if not sector_data: # Check if the dictionary is empty or None
            print(f"No sector data found for {sector} for year {target_year}.")
            return {}

        calculator = None
        if entity_type.lower() == "company":
            calculator = CompanyFinancialRatiosCalculator(sector_data, target_year)
        elif entity_type.lower() == "bank":
            calculator = BankFinancialRatiosCalculator(sector_data, target_year)
        else:
            print(f"Error: Invalid entity type: {entity_type}. Must be 'company' or 'bank'.")
            return {}

        calculator.calculate_ratios()
        return calculator.get_ratios()

# Instantiate the service for use in views
financial_ratios_service_instance = FinancialRatiosService()
