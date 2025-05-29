# # project_root/credit_risk/services/logic_three_service.py

# import pandas as pd
# # Import instances of previously defined services to fetch data
# # from credit_risk.services.FinancialVariablesService import financial_variables_service_instance
# from .FinancialVariablesService import financial_variables_service_instance

# class FinancialRatiosCalculator:
#     """
#     Base class for calculating financial ratios. Provides common utilities for
#     handling extracted financial data and calculating ratios across years.
#     """
#     def __init__(self, extracted_data: dict, target_year: str = None):
#         """
#         Initializes the calculator with extracted data and target year.

#         Args:
#             extracted_data (dict): A dictionary containing financial variables,
#                                    typically fetched by FinancialVariablesService.
#             target_year (str, optional): The year for which to calculate ratios.
#                                          Can be an integer year (as string) or 'all'.
#                                          Defaults to None (which implies 'all').
#         """
#         self.extracted_data = extracted_data
#         self.target_year = target_year
#         self.ratios = {}  # Initialize an empty dictionary to store calculated ratios

#     def _calculate_ratio(self, ratio_func, data: dict, year_input=None):
#         """
#         Helper function to calculate a single ratio for a given year or all years.

#         Args:
#             ratio_func (callable): A function that takes data (dict) and a single year (int)
#                                    and returns the calculated ratio for that year.
#             data (dict): The extracted financial variables.
#             year_input (str, optional): The year for which to calculate ratios.
#                                         Can be an integer year (as string) or 'all'.
#                                         Defaults to None.

#         Returns:
#             dict or float or None: A dictionary of year-to-ratio mappings if 'all' years
#                                    are requested, or a single float/None if a specific
#                                    year is requested. Returns None if calculation fails.
#         """
#         if year_input is None or str(year_input).lower() == 'all':
#             # Collect all unique years present in the extracted data
#             years = set()
#             for var_name in data:
#                 if isinstance(data.get(var_name), dict):
#                     years.update(data[var_name].keys())
            
#             result = {}
#             for y in sorted(list(years)): # Sort years for consistent output
#                 try:
#                     # Ensure year 'y' is an integer for ratio_func
#                     calculated_val = ratio_func(data, int(y))
#                     result[y] = calculated_val if pd.notna(calculated_val) else None # Handle NaN
#                 except Exception as e:
#                     print(f"Error calculating ratio for year {y}: {e}")
#                     result[y] = None
#             return result
#         else:
#             try:
#                 # Convert the target_year to an integer for calculation
#                 year_int = int(year_input)
#                 calculated_val = ratio_func(data, year_int)
#                 return calculated_val if pd.notna(calculated_val) else None # Handle NaN
#             except ValueError:
#                 print(f"Error: target_year '{year_input}' cannot be converted to an integer.")
#                 return None
#             except Exception as e:
#                 print(f"Error calculating ratio for year {year_input}: {e}")
#                 return None

#     def calculate_ratios(self):
#         """
#         Calculates all financial ratios. This is the main entry point for ratio calculation.
#         Subclasses must implement this method.
#         """
#         raise NotImplementedError("Subclasses must implement this method")

#     def get_ratios(self) -> dict:
#         """
#         Returns the calculated ratios.
#         """
#         return self.ratios


# class CompanyFinancialRatiosCalculator(FinancialRatiosCalculator):
#     """
#     Calculates financial ratios specifically for companies.
#     """
#     def __init__(self, extracted_data: dict, target_year: str = None):
#         super().__init__(extracted_data, target_year)
#         self.ratios = {
#             "Profitability Ratios": {},
#             "Efficiency Ratios": {},
#             "Liquidity Ratios": {},
#             "Solvency Ratios": {},
#         }

#     def calculate_ratios(self):
#         """
#         Calculates financial ratios for companies based on the extracted data.
#         """
#         data = self.extracted_data
#         year = self.target_year

#         # --- Profitability Ratios ---
#         def calculate_net_profit_margin(data, year):
#             return data.get("NET_PROFIT_MARGIN", {}).get(year)
#         self.ratios["Profitability Ratios"]["Net Profit Margin"] = self._calculate_ratio(calculate_net_profit_margin, data, year)

#         def calculate_roa(data, year):
#             return data.get("RETURN_ON_ASSETS", {}).get(year)
#         self.ratios["Profitability Ratios"]["Return On Assets"] = self._calculate_ratio(calculate_roa, data, year)

#         def calculate_roe(data, year):
#             return data.get("RETURN_ON_EQUITY", {}).get(year)
#         self.ratios["Profitability Ratios"]["Return On Equity"] = self._calculate_ratio(calculate_roe, data, year)

#         def calculate_gpm(data, year):
#             return data.get("GROSS_PROFIT_MARGIN",{}).get(year)
#         self.ratios["Profitability Ratios"]["Gross Profit Margin"] = self._calculate_ratio(calculate_gpm, data, year)

#         def calculate_oroa(data, year):
#             return data.get("OPERATING_RETURN_ON_ASSETS",{}).get(year)
#         self.ratios["Profitability Ratios"]["Operating Return On Assets"] = self._calculate_ratio(calculate_oroa, data, year)

#         def calculate_roce(data, year):
#             return data.get("RETURN_ON_CAPITAL_EMPLOYED",{}).get(year)
#         self.ratios["Profitability Ratios"]["Return On Capital Employed"] = self._calculate_ratio(calculate_roce, data, year)

#         # --- Liquidity Ratios ---
#         def calculate_current_ratio(data, year):
#             return data.get("CURRENT_RATIO", {}).get(year)
#         self.ratios["Liquidity Ratios"]["Current Ratio"] = self._calculate_ratio(calculate_current_ratio, data, year)

#         def calculate_quick_ratio(data, year):
#             return data.get("QUICK_RATIO", {}).get(year)
#         self.ratios["Liquidity Ratios"]["Quick Ratio"] = self._calculate_ratio(calculate_quick_ratio, data, year)

#         def calculate_cash_to_current_liabilities_ratio(data, year):
#             return data.get("CASH_TO_CURRENT_LIABILITIES_RATIO", {}).get(year)
#         self.ratios["Liquidity Ratios"]["Cash To Current Liabilities Ratio"] = self._calculate_ratio(calculate_cash_to_current_liabilities_ratio, data, year)

#         # --- Efficiency Ratios ---
#         def calculate_no_of_days_in_inventory(data, year):
#             return data.get("NUM_OF_DAYS_IN_INVENTORY", {}).get(year)
#         self.ratios["Efficiency Ratios"]["Num Of Days In Inventory"] = self._calculate_ratio(calculate_no_of_days_in_inventory, data, year)

#         def calculate_no_of_days_in_receivables(data, year):
#             return data.get("NUM_OF_DAYS_IN_RECEIVABLES", {}).get(year)
#         self.ratios["Efficiency Ratios"]["Num Of Days In Receivables"] = self._calculate_ratio(calculate_no_of_days_in_receivables, data, year)

#         def calculate_no_of_days_in_payable(data, year):
#             return data.get("NUM_OF_DAYS_IN_PAYABLE", {}).get(year)
#         self.ratios["Efficiency Ratios"]["Num Of Days In Payable"] = self._calculate_ratio(calculate_no_of_days_in_payable, data, year)

#         # --- Solvency Ratios ---
#         def calculate_debt_equity_ratio(data, year):
#             return data.get("DEBT_EQUITY_RATIO", {}).get(year)
#         self.ratios["Solvency Ratios"]["Debt Equity Ratio"] = self._calculate_ratio(calculate_debt_equity_ratio, data, year)

#         def calculate_debt_assets_ratio(data, year):
#             return data.get("DEBT_TO_ASSETS_RATIO", {}).get(year)
#         self.ratios["Solvency Ratios"]["Debt Asset Ratio"] = self._calculate_ratio(calculate_debt_assets_ratio, data, year)

#         def calculate_debt_capital_ratio(data, year):
#             return data.get("DEBT_TO_CAPITAL_RATIO", {}).get(year)
#         self.ratios["Solvency Ratios"]["Debt Capital Ratio"] = self._calculate_ratio(calculate_debt_capital_ratio, data, year)

#         def calculate_interest_coverage_ratio(data, year):
#             return data.get("INTEREST_COVER_RATIO", {}).get(year)
#         self.ratios["Solvency Ratios"]["Interest Coverage Ratio"] = self._calculate_ratio(calculate_interest_coverage_ratio, data, year)


# class BankFinancialRatiosCalculator(FinancialRatiosCalculator):
#     """
#     Calculates financial ratios specifically for banks.
#     """
#     def __init__(self, extracted_data: dict, target_year: str = None):
#         super().__init__(extracted_data, target_year)
#         self.ratios = {
#             "Profitability And Efficiency Ratios": {},
#             "Liquidity Ratios": {},
#             "Asset Quality Ratios": {},
#             "Solvency Ratios": {}
#         }

#     def calculate_ratios(self):
#         """
#         Calculates financial ratios for banks based on the extracted data.
#         """
#         data = self.extracted_data
#         year = self.target_year

#         # --- Profitability And Efficiency Ratios ---
#         def calculate_spread_ratio(data, year):
#             return data.get("SPREAD_RATIO", {}).get(year)
#         self.ratios["Profitability And Efficiency Ratios"]["Spread Ratio"] = self._calculate_ratio(calculate_spread_ratio, data, year)

#         def calculate_net_interest_margin(data, year):
#             return data.get("NET_INTEREST_MARGIN", {}).get(year)
#         self.ratios["Profitability And Efficiency Ratios"]["Net Interest Margin"] = self._calculate_ratio(calculate_net_interest_margin, data, year)

#         def calculate_return_on_equity(data, year):
#             return data.get("RETURN_ON_EQUITY", {}).get(year)
#         self.ratios["Profitability And Efficiency Ratios"]["Return On Equity"] = self._calculate_ratio(calculate_return_on_equity, data, year)

#         def calculate_return_on_assets(data, year):
#             return data.get("RETURN_ON_ASSETS", {}).get(year)
#         self.ratios["Profitability And Efficiency Ratios"]["Return On Assets"] = self._calculate_ratio(calculate_return_on_assets, data, year)

#         def calculate_non_interest_income_ratio(data, year):
#             return data.get("NON_INTEREST_INCOME_RATIO", {}).get(year)
#         self.ratios["Profitability And Efficiency Ratios"]["Non Interest Income Ratio"] = self._calculate_ratio(calculate_non_interest_income_ratio, data, year)

#         # --- Liquidity Ratios ---
#         def calculate_cash_to_total_assets_ratio(data, year):
#             return data.get("CASH_TO_TOTAL_ASSETS_RATIO", {}).get(year)
#         self.ratios["Liquidity Ratios"]["Cash To Total Assets Ratio"] = self._calculate_ratio(calculate_cash_to_total_assets_ratio, data, year)

#         def calculate_investment_to_total_assets(data, year):
#             return data.get("INVESTMENT_TO_TOTAL_ASSETS", {}).get(year)
#         self.ratios["Liquidity Ratios"]["Investment To Total Assets"] = self._calculate_ratio(calculate_investment_to_total_assets, data, year)

#         def calculate_advances_to_total_assets(data, year):
#             return data.get("ADVANCES_TO_TOTAL_ASSETS", {}).get(year)
#         self.ratios["Liquidity Ratios"]["Advances To Total Assets"] = self._calculate_ratio(calculate_advances_to_total_assets, data, year)

#         def calculate_deposits_to_total_assets(data, year):
#             return data.get("DEPOSIT_TO_TOTAL_ASSETS", {}).get(year)
#         self.ratios["Liquidity Ratios"]["Deposits To Total Assets"] = self._calculate_ratio(calculate_deposits_to_total_assets, data, year)

#         def calculate_total_liabilities_to_total_assets(data, year):
#             return data.get("TOTAL_LIABILITIES_TO_TOTAL_ASSETS", {}).get(year)
#         self.ratios["Liquidity Ratios"]["Total Liabilities To Total Assets"] = self._calculate_ratio(calculate_total_liabilities_to_total_assets, data, year)

#         def calculate_gross_advances_to_deposit(data, year):
#             return data.get("GROSS_ADVANCES_TO_DEPOSITS", {}).get(year)
#         self.ratios["Liquidity Ratios"]["Gross Advances To Deposits"] = self._calculate_ratio(calculate_gross_advances_to_deposit, data, year)

#         def calculate_gross_advances_to_borrowing_and_deposit(data, year):
#             return data.get("GROSS_ADVANCES_TO_BORROWING_AND_DEPOSIT", {}).get(year)
#         self.ratios["Liquidity Ratios"]["Gross Advances To Borrowing And Deposits"] = self._calculate_ratio(calculate_gross_advances_to_borrowing_and_deposit, data, year)

#         # ASSETS QUALITY RATIOS
#         def calculate_non_performing_loans_to_gross_advances(data, year):
#             return data.get("NON_PERFORMING_LOANS_TO_GROSS_ADVANCES", {}).get(year)
#         self.ratios["Asset Quality Ratios"]["Non-Performing Loans to Gross Advances"] = self._calculate_ratio(calculate_non_performing_loans_to_gross_advances, data, year)

#         def calculate_provisions_against_npls_to_gross_advances(data, year):
#             return data.get("PROVISION_AGAINST_NPLS_TO_GROSS_ADVANCES", {}).get(year)
#         self.ratios["Asset Quality Ratios"]["Provisions Against NPLs to Gross Advances"] = self._calculate_ratio(calculate_provisions_against_npls_to_gross_advances, data, year)

#         def calculate_npl_to_total_equity(data, year):
#             return data.get("NPL_TO_TOTAL_EQUITY", {}).get(year)
#         self.ratios["Asset Quality Ratios"]["NPL to Total Equity"] = self._calculate_ratio(calculate_npl_to_total_equity, data, year)

#         # --- Solvency Ratios ---
#         def calculate_capital_ratio(data, year):
#             return data.get("CAPITAL_RATIO", {}).get(year)
#         self.ratios["Solvency Ratios"]["Capital Ratio"] = self._calculate_ratio(calculate_capital_ratio, data, year)

#         def calculate_total_deposit_to_equity_ratio(data, year):
#             return data.get("TOTAL_DEPOSIT_TO_EQUITY_RATIO", {}).get(year)
#         self.ratios["Solvency Ratios"]["Total deposit to equity Ratio"] = self._calculate_ratio(calculate_total_deposit_to_equity_ratio, data, year)


# class FinancialRatiosService:
#     """
#     Service layer for calculating financial ratios for both companies and banks.
#     It orchestrates data fetching from FinancialVariablesService and then applies
#     the appropriate ratio calculation logic.
#     """
#     def calculate_financial_ratios_for_specific_entity(self, entity_type: str, sector: str = None, sub_sector: str = None, org_name: str = None, target_year: str = None) -> dict:
#         """
#         Calculates financial ratios for a specific organization based on extracted data.

#         Args:
#             entity_type (str): The type of entity ("company" or "bank").
#             sector (str): The sector of the organization.
#             sub_sector (str): The sub-sector of the organization.
#             org_name (str): The name of the organization.
#             target_year (str, optional): The year for which to calculate ratios.
#                                          If 'all', calculates for all available years. Defaults to None.

#         Returns:
#             dict: A dictionary containing the calculated ratios, categorized by type.
#                   Returns an empty dictionary if no data is fetched or ratios cannot be calculated.
#         """
#         # Fetch specific variables for the organization using the FinancialVariablesService
#         extracted_data = financial_variables_service_instance.get_specific_variables_for_specific_org(
#             entity_type=entity_type,
#             sector=sector,
#             sub_sector=sub_sector,
#             org_name=org_name,
#             target_year=target_year # Pass target_year to filter variables
#         )

#         if not extracted_data: # Check if the dictionary is empty or None
#             print(f"No specific financial variables found for {org_name} in {sector} {sub_sector} for year {target_year}.")
#             return {}

#         calculator = None
#         if entity_type.lower() == "company":
#             calculator = CompanyFinancialRatiosCalculator(extracted_data, target_year)
#         elif entity_type.lower() == "bank":
#             calculator = BankFinancialRatiosCalculator(extracted_data, target_year)
#         else:
#             print(f"Error: Invalid entity type: {entity_type}. Must be 'company' or 'bank'.")
#             return {}

#         calculator.calculate_ratios()
#         return calculator.get_ratios()

#     def calculate_financial_ratios_for_specific_sector(self, entity_type: str, sector: str, target_year: str = None) -> dict:
#         """
#         Calculates the average financial ratios for all organizations within a given sector
#         (including all sub-sectors).

#         Args:
#             entity_type (str): The type of entity ("company" or "bank").
#             sector (str): The sector for which to calculate average ratios.
#             target_year (str, optional): The year for which to calculate ratios.
#                                          If 'all', calculates for all available years. Defaults to None.

#         Returns:
#             dict: A dictionary containing the calculated average ratios, categorized by type.
#                   Returns an empty dictionary if no data is fetched or ratios cannot be calculated.
#         """
#         # Fetch aggregated variables for the sector using the FinancialVariablesService
#         sector_data = financial_variables_service_instance.get_specific_variables_by_sector(
#             entity_type=entity_type,
#             sector=sector,
#             target_year=target_year # Pass target_year to filter variables
#         )

#         if not sector_data: # Check if the dictionary is empty or None
#             print(f"No sector data found for {sector} for year {target_year}.")
#             return {}

#         calculator = None
#         if entity_type.lower() == "company":
#             calculator = CompanyFinancialRatiosCalculator(sector_data, target_year)
#         elif entity_type.lower() == "bank":
#             calculator = BankFinancialRatiosCalculator(sector_data, target_year)
#         else:
#             print(f"Error: Invalid entity type: {entity_type}. Must be 'company' or 'bank'.")
#             return {}

#         calculator.calculate_ratios()
#         return calculator.get_ratios()

# # Instantiate the service for use in views
# financial_ratios_service_instance = FinancialRatiosService()







# project_root/credit_risk/services/logic_three_service.py

# import pandas as pd
# # Import instances of previously defined services to fetch data
# # from credit_risk.services.FinancialVariablesService import financial_variables_service_instance
# from .FinancialVariablesService import financial_variables_service_instance

# class FinancialRatiosCalculator:
#     """
#     Base class for calculating financial ratios. Provides common utilities for
#     handling extracted financial data and calculating ratios across years.
#     """
#     def __init__(self, extracted_data: dict, target_year: str = None):
#         """
#         Initializes the calculator with extracted data and target year.

#         Args:
#             extracted_data (dict): A dictionary containing financial variables,
#                                    typically fetched by FinancialVariablesService.
#             target_year (str, optional): The year for which to calculate ratios.
#                                          Can be an integer year (as string) or 'all'.
#                                          Defaults to None (which implies 'all').
#         """
#         self.extracted_data = extracted_data
#         self.target_year = target_year
#         self.ratios = {}  # Initialize an empty dictionary to store calculated ratios

#     def _calculate_ratio(self, ratio_func, data: dict, year_input=None):
#         """
#         Helper function to calculate a single ratio for a given year or all years.

#         Args:
#             ratio_func (callable): A function that takes data (dict) and a single year (int)
#                                    and returns the calculated ratio for that year.
#             data (dict): The extracted financial variables.
#             year_input (str, optional): The year for which to calculate ratios.
#                                          Can be an integer year (as string) or 'all'.
#                                          Defaults to None.

#         Returns:
#             dict or float or None: A dictionary of year-to-ratio mappings if 'all' years
#                                    are requested, or a single float/None if a specific
#                                    year is requested. Returns None if calculation fails.
#         """
#         if year_input is None or str(year_input).lower() == 'all':
#             # Collect all unique years present in the extracted data
#             years = set()
#             for var_name in data:
#                 if isinstance(data.get(var_name), dict):
#                     years.update(data[var_name].keys())
            
#             result = {}
#             for y in sorted(list(years)): # Sort years for consistent output
#                 try:
#                     # Ensure year 'y' is an integer for ratio_func
#                     calculated_val = ratio_func(data, int(y))
#                     result[y] = calculated_val if pd.notna(calculated_val) else None # Handle NaN
#                 except Exception as e:
#                     print(f"Error calculating ratio for year {y}: {e}")
#                     result[y] = None
#             return result
#         else:
#             try:
#                 # Convert the target_year to an integer for calculation
#                 year_int = int(year_input)
#                 calculated_val = ratio_func(data, year_int)
#                 return calculated_val if pd.notna(calculated_val) else None # Handle NaN
#             except ValueError:
#                 print(f"Error: target_year '{year_input}' cannot be converted to an integer.")
#                 return None
#             except Exception as e:
#                 print(f"Error calculating ratio for year {year_input}: {e}")
#                 return None

#     def calculate_ratios(self):
#         """
#         Calculates all financial ratios. This is the main entry point for ratio calculation.
#         Subclasses must implement this method.
#         """
#         raise NotImplementedError("Subclasses must implement this method")

#     def get_ratios(self) -> dict:
#         """
#         Returns the calculated ratios.
#         """
#         return self.ratios


# class CompanyFinancialRatiosCalculator(FinancialRatiosCalculator):
#     """
#     Calculates financial ratios specifically for companies.
#     """
#     def __init__(self, extracted_data: dict, target_year: str = None):
#         super().__init__(extracted_data, target_year)
#         self.ratios = {
#             "Profitability Ratios": {},
#             "Efficiency Ratios": {},
#             "Liquidity Ratios": {},
#             "Solvency Ratios": {},
#         }

#     def calculate_ratios(self):
#         """
#         Calculates financial ratios for companies based on the extracted data.
#         """
#         data = self.extracted_data
#         year = self.target_year

#         # --- Profitability Ratios ---
#         def calculate_net_profit_margin(data, year):
#             return data.get("NET_PROFIT_MARGIN", {}).get(year)
#         self.ratios["Profitability Ratios"]["Net Profit Margin"] = self._calculate_ratio(calculate_net_profit_margin, data, year)

#         def calculate_roa(data, year):
#             return data.get("RETURN_ON_ASSETS", {}).get(year)
#         self.ratios["Profitability Ratios"]["Return On Assets"] = self._calculate_ratio(calculate_roa, data, year)

#         def calculate_roe(data, year):
#             return data.get("RETURN_ON_EQUITY", {}).get(year)
#         self.ratios["Profitability Ratios"]["Return On Equity"] = self._calculate_ratio(calculate_roe, data, year)

#         def calculate_gpm(data, year):
#             return data.get("GROSS_PROFIT_MARGIN",{}).get(year)
#         self.ratios["Profitability Ratios"]["Gross Profit Margin"] = self._calculate_ratio(calculate_gpm, data, year)

#         def calculate_oroa(data, year):
#             return data.get("OPERATING_RETURN_ON_ASSETS",{}).get(year)
#         self.ratios["Profitability Ratios"]["Operating Return On Assets"] = self._calculate_ratio(calculate_oroa, data, year)

#         def calculate_roce(data, year):
#             return data.get("RETURN_ON_CAPITAL_EMPLOYED",{}).get(year)
#         self.ratios["Profitability Ratios"]["Return On Capital Employed"] = self._calculate_ratio(calculate_roce, data, year)

#         # --- Liquidity Ratios ---
#         def calculate_current_ratio(data, year):
#             return data.get("CURRENT_RATIO", {}).get(year)
#         self.ratios["Liquidity Ratios"]["Current Ratio"] = self._calculate_ratio(calculate_current_ratio, data, year)

#         def calculate_quick_ratio(data, year):
#             return data.get("QUICK_RATIO", {}).get(year)
#         self.ratios["Liquidity Ratios"]["Quick Ratio"] = self._calculate_ratio(calculate_quick_ratio, data, year)

#         def calculate_cash_to_current_liabilities_ratio(data, year):
#             return data.get("CASH_TO_CURRENT_LIABILITIES_RATIO", {}).get(year)
#         self.ratios["Liquidity Ratios"]["Cash To Current Liabilities Ratio"] = self._calculate_ratio(calculate_cash_to_current_liabilities_ratio, data, year)

#         # --- Efficiency Ratios ---
#         def calculate_no_of_days_in_inventory(data, year):
#             return data.get("NUM_OF_DAYS_IN_INVENTORY", {}).get(year)
#         self.ratios["Efficiency Ratios"]["Num Of Days In Inventory"] = self._calculate_ratio(calculate_no_of_days_in_inventory, data, year)

#         def calculate_no_of_days_in_receivables(data, year):
#             return data.get("NUM_OF_DAYS_IN_RECEIVABLES", {}).get(year)
#         self.ratios["Efficiency Ratios"]["Num Of Days In Receivables"] = self._calculate_ratio(calculate_no_of_days_in_receivables, data, year)

#         def calculate_no_of_days_in_payable(data, year):
#             return data.get("NUM_OF_DAYS_IN_PAYABLE", {}).get(year)
#         self.ratios["Efficiency Ratios"]["Num Of Days In Payable"] = self._calculate_ratio(calculate_no_of_days_in_payable, data, year)

#         # --- Solvency Ratios ---
#         def calculate_debt_equity_ratio(data, year):
#             return data.get("DEBT_EQUITY_RATIO", {}).get(year)
#         self.ratios["Solvency Ratios"]["Debt Equity Ratio"] = self._calculate_ratio(calculate_debt_equity_ratio, data, year)

#         def calculate_debt_assets_ratio(data, year):
#             return data.get("DEBT_TO_ASSETS_RATIO", {}).get(year)
#         self.ratios["Solvency Ratios"]["Debt Asset Ratio"] = self._calculate_ratio(calculate_debt_assets_ratio, data, year)

#         def calculate_debt_capital_ratio(data, year):
#             return data.get("DEBT_TO_CAPITAL_RATIO", {}).get(year)
#         self.ratios["Solvency Ratios"]["Debt Capital Ratio"] = self._calculate_ratio(calculate_debt_capital_ratio, data, year)

#         def calculate_interest_coverage_ratio(data, year):
#             return data.get("INTEREST_COVER_RATIO", {}).get(year)
#         self.ratios["Solvency Ratios"]["Interest Coverage Ratio"] = self._calculate_ratio(calculate_interest_coverage_ratio, data, year)


# class BankFinancialRatiosCalculator(FinancialRatiosCalculator):
#     """
#     Calculates financial ratios specifically for banks.
#     """
#     def __init__(self, extracted_data: dict, target_year: str = None):
#         super().__init__(extracted_data, target_year)
#         self.ratios = {
#             "Profitability And Efficiency Ratios": {},
#             "Liquidity Ratios": {},
#             "Asset Quality Ratios": {},
#             "Solvency Ratios": {}
#         }

#     def calculate_ratios(self):
#         """
#         Calculates financial ratios for banks based on the extracted data.
#         """
#         data = self.extracted_data
#         year = self.target_year

#         # --- Profitability And Efficiency Ratios ---
#         def calculate_spread_ratio(data, year):
#             return data.get("SPREAD_RATIO", {}).get(year)
#         self.ratios["Profitability And Efficiency Ratios"]["Spread Ratio"] = self._calculate_ratio(calculate_spread_ratio, data, year)

#         def calculate_net_interest_margin(data, year):
#             return data.get("NET_INTEREST_MARGIN", {}).get(year)
#         self.ratios["Profitability And Efficiency Ratios"]["Net Interest Margin"] = self._calculate_ratio(calculate_net_interest_margin, data, year)

#         def calculate_return_on_equity(data, year):
#             return data.get("RETURN_ON_EQUITY", {}).get(year)
#         self.ratios["Profitability And Efficiency Ratios"]["Return On Equity"] = self._calculate_ratio(calculate_return_on_equity, data, year)

#         def calculate_return_on_assets(data, year):
#             return data.get("RETURN_ON_ASSETS", {}).get(year)
#         self.ratios["Profitability And Efficiency Ratios"]["Return On Assets"] = self._calculate_ratio(calculate_return_on_assets, data, year)

#         def calculate_non_interest_income_ratio(data, year):
#             return data.get("NON_INTEREST_INCOME_RATIO", {}).get(year)
#         self.ratios["Profitability And Efficiency Ratios"]["Non Interest Income Ratio"] = self._calculate_ratio(calculate_non_interest_income_ratio, data, year)

#         # --- Liquidity Ratios ---
#         def calculate_cash_to_total_assets_ratio(data, year):
#             return data.get("CASH_TO_TOTAL_ASSETS_RATIO", {}).get(year)
#         self.ratios["Liquidity Ratios"]["Cash To Total Assets Ratio"] = self._calculate_ratio(calculate_cash_to_total_assets_ratio, data, year)

#         def calculate_investment_to_total_assets(data, year):
#             return data.get("INVESTMENT_TO_TOTAL_ASSETS", {}).get(year)
#         self.ratios["Liquidity Ratios"]["Investment To Total Assets"] = self._calculate_ratio(calculate_investment_to_total_assets, data, year)

#         def calculate_advances_to_total_assets(data, year):
#             return data.get("ADVANCES_TO_TOTAL_ASSETS", {}).get(year)
#         self.ratios["Liquidity Ratios"]["Advances To Total Assets"] = self._calculate_ratio(calculate_advances_to_total_assets, data, year)

#         def calculate_deposits_to_total_assets(data, year):
#             return data.get("DEPOSIT_TO_TOTAL_ASSETS", {}).get(year)
#         self.ratios["Liquidity Ratios"]["Deposits To Total Assets"] = self._calculate_ratio(calculate_deposits_to_total_assets, data, year)

#         def calculate_total_liabilities_to_total_assets(data, year):
#             return data.get("TOTAL_LIABILITIES_TO_TOTAL_ASSETS", {}).get(year)
#         self.ratios["Liquidity Ratios"]["Total Liabilities To Total Assets"] = self._calculate_ratio(calculate_total_liabilities_to_total_assets, data, year)

#         def calculate_gross_advances_to_deposit(data, year):
#             return data.get("GROSS_ADVANCES_TO_DEPOSITS", {}).get(year)
#         self.ratios["Liquidity Ratios"]["Gross Advances To Deposits"] = self._calculate_ratio(calculate_gross_advances_to_deposit, data, year)

#         def calculate_gross_advances_to_borrowing_and_deposit(data, year):
#             return data.get("GROSS_ADVANCES_TO_BORROWING_AND_DEPOSIT", {}).get(year)
#         self.ratios["Liquidity Ratios"]["Gross Advances To Borrowing And Deposits"] = self._calculate_ratio(calculate_gross_advances_to_borrowing_and_deposit, data, year)

#         # ASSETS QUALITY RATIOS
#         def calculate_non_performing_loans_to_gross_advances(data, year):
#             return data.get("NON_PERFORMING_LOANS_TO_GROSS_ADVANCES", {}).get(year)
#         self.ratios["Asset Quality Ratios"]["Non-Performing Loans to Gross Advances"] = self._calculate_ratio(calculate_non_performing_loans_to_gross_advances, data, year)

#         def calculate_provisions_against_npls_to_gross_advances(data, year):
#             return data.get("PROVISION_AGAINST_NPLS_TO_GROSS_ADVANCES", {}).get(year)
#         self.ratios["Asset Quality Ratios"]["Provisions Against NPLs to Gross Advances"] = self._calculate_ratio(calculate_provisions_against_npls_to_gross_advances, data, year)

#         def calculate_npl_to_total_equity(data, year):
#             return data.get("NPL_TO_TOTAL_EQUITY", {}).get(year)
#         self.ratios["Asset Quality Ratios"]["NPL to Total Equity"] = self._calculate_ratio(calculate_npl_to_total_equity, data, year)

#         # --- Solvency Ratios ---
#         def calculate_capital_ratio(data, year):
#             return data.get("CAPITAL_RATIO", {}).get(year)
#         self.ratios["Solvency Ratios"]["Capital Ratio"] = self._calculate_ratio(calculate_capital_ratio, data, year)

#         def calculate_total_deposit_to_equity_ratio(data, year):
#             return data.get("TOTAL_DEPOSIT_TO_EQUITY_RATIO", {}).get(year)
#         self.ratios["Solvency Ratios"]["Total deposit to equity Ratio"] = self._calculate_ratio(calculate_total_deposit_to_equity_ratio, data, year)


# class FinancialRatiosService:
#     """
#     Service layer for calculating financial ratios for both companies and banks.
#     It orchestrates data fetching from FinancialVariablesService and then applies
#     the appropriate ratio calculation logic.
#     """
#     def _get_rank(self, org_name: str, org_value: float, all_orgs_values: list[tuple[str, float]], higher_is_better: bool = True) -> int:
#         """
#         Calculates the rank of an organization's value within a list of all organizations' values.

#         Args:
#             org_name (str): The name of the organization to rank.
#             org_value (float): The value of the specific organization.
#             all_orgs_values (list[tuple[str, float]]): List of (organization_name, value) tuples for the sector.
#             higher_is_better (bool): True if higher values mean better rank (e.g., Revenue),
#                                      False if lower values mean better rank (e.g., NPLs).

#         Returns:
#             int: The rank (1-based), or None if the organization's value is None, not found, or no valid data.
#         """
#         if org_value is None or pd.isna(org_value):
#             return None

#         # Create a Series for ranking from valid organization data
#         valid_orgs_data = {name: val for name, val in all_orgs_values if val is not None and pd.notna(val)}
#         if not valid_orgs_data:
#             return None # No valid data to rank against

#         temp_series = pd.Series(valid_orgs_data)

#         # Rank the series. 'dense' method gives consecutive ranks without gaps.
#         # `ascending=False` for higher_is_better (e.g., Revenue: 1st is highest)
#         # `ascending=True` for lower_is_better (e.g., NPLs: 1st is lowest)
#         ranked_series = temp_series.rank(method='dense', ascending=not higher_is_better)

#         # Get the rank of the specific organization
#         rank = ranked_series.get(org_name)

#         if pd.notna(rank):
#             return int(rank)
#         return None


#     def calculate_financial_ratios_for_specific_entity(self, entity_type: str, sector: str = None, sub_sector: str = None, org_name: str = None, target_year: str = None) -> dict:
#         """
#         Calculates financial ratios for a specific organization based on extracted data.

#         Args:
#             entity_type (str): The type of entity ("company" or "bank").
#             sector (str): The sector of the organization.
#             sub_sector (str): The sub-sector of the organization.
#             org_name (str): The name of the organization.
#             target_year (str, optional): The year for which to calculate ratios.
#                                          If 'all', calculates for all available years. Defaults to None.

#         Returns:
#             dict: A dictionary containing the calculated ratios, categorized by type,
#                   plus Revenue and Assets details with ranking.
#                   Returns an empty dictionary if no data is fetched or ratios cannot be calculated.
#         """
#         # Fetch specific variables for the organization using the FinancialVariablesService
#         extracted_data = financial_variables_service_instance.get_specific_variables_for_specific_org(
#             entity_type=entity_type,
#             sector=sector,
#             sub_sector=sub_sector,
#             org_name=org_name,
#             target_year=target_year # Pass target_year to filter variables
#         )

#         if not extracted_data: # Check if the dictionary is empty or None
#             print(f"No specific financial variables found for {org_name} in {sector} {sub_sector} for year {target_year}.")
#             return {}

#         # Convert target_year to integer for fetching specific variables for ranking
#         target_year_int = None
#         if target_year is not None and str(target_year).lower() != 'all':
#             try:
#                 target_year_int = int(target_year)
#             except ValueError:
#                 print(f"Error: target_year '{target_year}' cannot be converted to an integer. Cannot perform ranking.")
#                 # Still proceed with ratios, but ranking info will be missing
        
#         # Initialize results with existing ratio calculation
#         final_results = {}
#         calculator = None

#         # --- START OF CHANGES ---
#         # Determine internal variable keys for fetching data (these match your variables_map keys)
#         revenue_var_key = "REVENUE"
#         assets_var_key = "ASSETS" # CHANGED: Now using "ASSETS" as the internal key for both companies and banks

#         # Set the display labels based on entity type for the final output string
#         revenue_label = "Revenue" # Default
#         assets_label = "Assets"   # Default

#         if entity_type.lower() == "company":
#             calculator = CompanyFinancialRatiosCalculator(extracted_data, target_year)
#             revenue_label = "Sales" # Specific display label for companies
#             assets_label = "Total Assets (A+B) / Equity & Liabilities (C+D+E)" # Specific display label for companies
#         elif entity_type.lower() == "bank":
#             calculator = BankFinancialRatiosCalculator(extracted_data, target_year)
#             revenue_label = "Profit & loss account" # Specific display label for banks
#             assets_label = "Total assets (C1 to C4 + C8 to C10)" # Specific display label for banks
#         else:
#             print(f"Error: Invalid entity type: {entity_type}. Must be 'company' or 'bank'.")
#             return {}

#         calculator.calculate_ratios()
#         final_results.update(calculator.get_ratios()) # Add existing ratios

#         # --- Add Revenue and Assets with Ranking (only if target_year is a specific year) ---
#         if target_year_int is not None:
#             # Fetch all organizations' revenue for ranking using the internal 'revenue_var_key'
#             all_orgs_revenue_data = financial_variables_service_instance.get_all_organizations_variable_for_year_by_sector(
#                 entity_type=entity_type,
#                 sector=sector,
#                 variable_key=revenue_var_key, # Use the internal key, which maps to "1. Sales" or "D. Profit & loss account"
#                 target_year=target_year_int
#             )
            
#             # Fetch all organizations' assets for ranking using the internal 'assets_var_key'
#             all_orgs_assets_data = financial_variables_service_instance.get_all_organizations_variable_for_year_by_sector(
#                 entity_type=entity_type,
#                 sector=sector,
#                 variable_key=assets_var_key, # Use the internal key, which maps to the full asset strings
#                 target_year=target_year_int
#             )

#             # Get the specific organization's values for the target year
#             org_revenue_value = extracted_data.get(revenue_var_key, {}).get(target_year_int)
#             org_assets_value = extracted_data.get(assets_var_key, {}).get(target_year_int)
            
#             # Determine ranks
#             revenue_rank = self._get_rank(org_name, org_revenue_value, all_orgs_revenue_data, higher_is_better=True)
#             assets_rank = self._get_rank(org_name, org_assets_value, all_orgs_assets_data, higher_is_better=True) 

#             # Format the output strings
#             sector_display_name = f"{sector} Sector" if sector else "Industry"
            
#             # Revenue formatting
#             revenue_display = "N/A"
#             if org_revenue_value is not None and pd.notna(org_revenue_value):
#                 revenue_display = f"Rs. {org_revenue_value:,.3f} Million"
#                 if revenue_rank is not None:
#                     revenue_display += f" (ranked {revenue_rank} in {sector_display_name})"
#             # Use the dynamic 'revenue_label' here
#             final_results["RevenueDetails"] = f"{revenue_label} in {target_year_int} {revenue_display}"

#             # Assets formatting
#             assets_display = "N/A"
#             if org_assets_value is not None and pd.notna(org_assets_value):
#                 # For both new Company and Bank 'ASSETS' variables, it's a monetary value, not percentage.
#                 assets_display = f"Rs. {org_assets_value:,.3f} Million"

#                 if assets_rank is not None:
#                     assets_display += f" (ranked {assets_rank} in {sector_display_name})"
#             # Use the dynamic 'assets_label' here
#             final_results["AssetsDetails"] = f"{assets_label} as of {target_year_int} {assets_display}"
#         # --- END OF CHANGES ---

#         return final_results

#     def calculate_financial_ratios_for_specific_sector(self, entity_type: str, sector: str, target_year: str = None) -> dict:
#         """
#         Calculates the average financial ratios for all organizations within a given sector
#         (including all sub-sectors).

#         Args:
#             entity_type (str): The type of entity ("company" or "bank").
#             sector (str): The sector for which to calculate average ratios.
#             target_year (str, optional): The year for which to calculate ratios.
#                                          If 'all', calculates for all available years. Defaults to None.

#         Returns:
#             dict: A dictionary containing the calculated average ratios, categorized by type.
#                   Returns an empty dictionary if no data is fetched or ratios cannot be calculated.
#         """
#         # Fetch aggregated variables for the sector using the FinancialVariablesService
#         sector_data = financial_variables_service_instance.get_specific_variables_by_sector(
#             entity_type=entity_type,
#             sector=sector,
#             target_year=target_year # Pass target_year to filter variables
#         )

#         if not sector_data: # Check if the dictionary is empty or None
#             print(f"No sector data found for {sector} for year {target_year}.")
#             return {}

#         calculator = None
#         if entity_type.lower() == "company":
#             calculator = CompanyFinancialRatiosCalculator(sector_data, target_year)
#         elif entity_type.lower() == "bank":
#             calculator = BankFinancialRatiosCalculator(sector_data, target_year)
#         else:
#             print(f"Error: Invalid entity type: {entity_type}. Must be 'company' or 'bank'.")
#             return {}

#         calculator.calculate_ratios()
#         return calculator.get_ratios()

# # Instantiate the service for use in views
# financial_ratios_service_instance = FinancialRatiosService()



# import pandas as pd
# # Import instances of previously defined services to fetch data
# # from credit_risk.services.FinancialVariablesService import financial_variables_service_instance
# from .FinancialVariablesService import financial_variables_service_instance

# class FinancialRatiosCalculator:
#     """
#     Base class for calculating financial ratios. Provides common utilities for
#     handling extracted financial data and calculating ratios across years.
#     """
#     def __init__(self, extracted_data: dict, target_year: str = None):
#         """
#         Initializes the calculator with extracted data and target year.

#         Args:
#             extracted_data (dict): A dictionary containing financial variables,
#                                    typically fetched by FinancialVariablesService.
#             target_year (str, optional): The year for which to calculate ratios.
#                                          Can be an integer year (as string) or 'all'.
#                                          Defaults to None (which implies 'all').
#         """
#         self.extracted_data = extracted_data
#         self.target_year = target_year
#         self.ratios = {}  # Initialize an empty dictionary to store calculated ratios

#     def _calculate_ratio(self, ratio_func, data: dict, year_input=None):
#         """
#         Helper function to calculate a single ratio for a given year or all years.

#         Args:
#             ratio_func (callable): A function that takes data (dict) and a single year (int)
#                                    and returns the calculated ratio for that year.
#             data (dict): The extracted financial variables.
#             year_input (str, optional): The year for which to calculate ratios.
#                                          Can be an integer year (as string) or 'all'.
#                                          Defaults to None.

#         Returns:
#             dict or float or None: A dictionary of year-to-ratio mappings if 'all' years
#                                    are requested, or a single float/None if a specific
#                                    year is requested. Returns None if calculation fails.
#         """
#         if year_input is None or str(year_input).lower() == 'all':
#             # Collect all unique years present in the extracted data
#             years = set()
#             for var_name in data:
#                 if isinstance(data.get(var_name), dict):
#                     years.update(data[var_name].keys())
            
#             result = {}
#             for y in sorted(list(years)): # Sort years for consistent output
#                 try:
#                     # Ensure year 'y' is an integer for ratio_func
#                     calculated_val = ratio_func(data, int(y))
#                     result[y] = calculated_val if pd.notna(calculated_val) else None # Handle NaN
#                 except Exception as e:
#                     # print(f"Error calculating ratio for year {y}: {e}") # Suppress for cleaner output unless debugging
#                     result[y] = None
#             return result
#         else:
#             try:
#                 # Convert the target_year to an integer for calculation
#                 year_int = int(year_input)
#                 calculated_val = ratio_func(data, year_int)
#                 return calculated_val if pd.notna(calculated_val) else None # Handle NaN
#             except ValueError:
#                 print(f"Error: target_year '{year_input}' cannot be converted to an integer.")
#                 return None
#             except Exception as e:
#                 # print(f"Error calculating ratio for year {year_input}: {e}") # Suppress for cleaner output unless debugging
#                 return None

#     def calculate_ratios(self):
#         """
#         Calculates all financial ratios. This is the main entry point for ratio calculation.
#         Subclasses must implement this method.
#         """
#         raise NotImplementedError("Subclasses must implement this method")

#     def get_ratios(self) -> dict:
#         """
#         Returns the calculated ratios.
#         """
#         return self.ratios


# class CompanyFinancialRatiosCalculator(FinancialRatiosCalculator):
#     """
#     Calculates financial ratios specifically for companies.
#     """
#     def __init__(self, extracted_data: dict, target_year: str = None):
#         super().__init__(extracted_data, target_year)
#         self.ratios = {
#             "Profitability Ratios": {},
#             "Efficiency Ratios": {},
#             "Liquidity Ratios": {},
#             "Solvency Ratios": {},
#         }

#     def calculate_ratios(self):
#         """
#         Calculates financial ratios for companies based on the extracted data.
#         """
#         data = self.extracted_data
#         year = self.target_year

#         # --- Profitability Ratios ---
#         def calculate_net_profit_margin(data, year):
#             return data.get("NET_PROFIT_MARGIN", {}).get(year)
#         self.ratios["Profitability Ratios"]["Net Profit Margin"] = self._calculate_ratio(calculate_net_profit_margin, data, year)

#         def calculate_roa(data, year):
#             return data.get("RETURN_ON_ASSETS", {}).get(year)
#         self.ratios["Profitability Ratios"]["Return On Assets"] = self._calculate_ratio(calculate_roa, data, year)

#         def calculate_roe(data, year):
#             return data.get("RETURN_ON_EQUITY", {}).get(year)
#         self.ratios["Profitability Ratios"]["Return On Equity"] = self._calculate_ratio(calculate_roe, data, year)

#         def calculate_gpm(data, year):
#             return data.get("GROSS_PROFIT_MARGIN",{}).get(year)
#         self.ratios["Profitability Ratios"]["Gross Profit Margin"] = self._calculate_ratio(calculate_gpm, data, year)

#         def calculate_oroa(data, year):
#             return data.get("OPERATING_RETURN_ON_ASSETS",{}).get(year)
#         self.ratios["Profitability Ratios"]["Operating Return On Assets"] = self._calculate_ratio(calculate_oroa, data, year)

#         def calculate_roce(data, year):
#             return data.get("RETURN_ON_CAPITAL_EMPLOYED",{}).get(year)
#         self.ratios["Profitability Ratios"]["Return On Capital Employed"] = self._calculate_ratio(calculate_roce, data, year)

#         # --- Liquidity Ratios ---
#         def calculate_current_ratio(data, year):
#             return data.get("CURRENT_RATIO", {}).get(year)
#         self.ratios["Liquidity Ratios"]["Current Ratio"] = self._calculate_ratio(calculate_current_ratio, data, year)

#         def calculate_quick_ratio(data, year):
#             return data.get("QUICK_RATIO", {}).get(year)
#         self.ratios["Liquidity Ratios"]["Quick Ratio"] = self._calculate_ratio(calculate_quick_ratio, data, year)

#         def calculate_cash_to_current_liabilities_ratio(data, year):
#             return data.get("CASH_TO_CURRENT_LIABILITIES_RATIO", {}).get(year)
#         self.ratios["Liquidity Ratios"]["Cash To Current Liabilities Ratio"] = self._calculate_ratio(calculate_cash_to_current_liabilities_ratio, data, year)

#         # --- Efficiency Ratios ---
#         def calculate_no_of_days_in_inventory(data, year):
#             return data.get("NUM_OF_DAYS_IN_INVENTORY", {}).get(year)
#         self.ratios["Efficiency Ratios"]["Num Of Days In Inventory"] = self._calculate_ratio(calculate_no_of_days_in_inventory, data, year)

#         def calculate_no_of_days_in_receivables(data, year):
#             return data.get("NUM_OF_DAYS_IN_RECEIVABLES", {}).get(year)
#         self.ratios["Efficiency Ratios"]["Num Of Days In Receivables"] = self._calculate_ratio(calculate_no_of_days_in_receivables, data, year)

#         def calculate_no_of_days_in_payable(data, year):
#             return data.get("NUM_OF_DAYS_IN_PAYABLE", {}).get(year)
#         self.ratios["Efficiency Ratios"]["Num Of Days In Payable"] = self._calculate_ratio(calculate_no_of_days_in_payable, data, year)

#         # --- Solvency Ratios ---
#         def calculate_debt_equity_ratio(data, year):
#             return data.get("DEBT_EQUITY_RATIO", {}).get(year)
#         self.ratios["Solvency Ratios"]["Debt Equity Ratio"] = self._calculate_ratio(calculate_debt_equity_ratio, data, year)

#         def calculate_debt_assets_ratio(data, year):
#             return data.get("DEBT_TO_ASSETS_RATIO", {}).get(year)
#         self.ratios["Solvency Ratios"]["Debt Asset Ratio"] = self._calculate_ratio(calculate_debt_assets_ratio, data, year)

#         def calculate_debt_capital_ratio(data, year):
#             return data.get("DEBT_TO_CAPITAL_RATIO", {}).get(year)
#         self.ratios["Solvency Ratios"]["Debt Capital Ratio"] = self._calculate_ratio(calculate_debt_capital_ratio, data, year)

#         def calculate_interest_coverage_ratio(data, year):
#             return data.get("INTEREST_COVER_RATIO", {}).get(year)
#         self.ratios["Solvency Ratios"]["Interest Coverage Ratio"] = self._calculate_ratio(calculate_interest_coverage_ratio, data, year)


# class BankFinancialRatiosCalculator(FinancialRatiosCalculator):
#     """
#     Calculates financial ratios specifically for banks.
#     """
#     def __init__(self, extracted_data: dict, target_year: str = None):
#         super().__init__(extracted_data, target_year)
#         self.ratios = {
#             "Profitability And Efficiency Ratios": {},
#             "Liquidity Ratios": {},
#             "Asset Quality Ratios": {},
#             "Solvency Ratios": {}
#         }

#     def calculate_ratios(self):
#         """
#         Calculates financial ratios for banks based on the extracted data.
#         """
#         data = self.extracted_data
#         year = self.target_year

#         # --- Profitability And Efficiency Ratios ---
#         def calculate_spread_ratio(data, year):
#             return data.get("SPREAD_RATIO", {}).get(year)
#         self.ratios["Profitability And Efficiency Ratios"]["Spread Ratio"] = self._calculate_ratio(calculate_spread_ratio, data, year)

#         def calculate_net_interest_margin(data, year):
#             return data.get("NET_INTEREST_MARGIN", {}).get(year)
#         self.ratios["Profitability And Efficiency Ratios"]["Net Interest Margin"] = self._calculate_ratio(calculate_net_interest_margin, data, year)

#         def calculate_return_on_equity(data, year):
#             return data.get("RETURN_ON_EQUITY", {}).get(year)
#         self.ratios["Profitability And Efficiency Ratios"]["Return On Equity"] = self._calculate_ratio(calculate_return_on_equity, data, year)

#         def calculate_return_on_assets(data, year):
#             return data.get("RETURN_ON_ASSETS", {}).get(year)
#         self.ratios["Profitability And Efficiency Ratios"]["Return On Assets"] = self._calculate_ratio(calculate_return_on_assets, data, year)

#         def calculate_non_interest_income_ratio(data, year):
#             return data.get("NON_INTEREST_INCOME_RATIO", {}).get(year)
#         self.ratios["Profitability And Efficiency Ratios"]["Non Interest Income Ratio"] = self._calculate_ratio(calculate_non_interest_income_ratio, data, year)

#         # --- Liquidity Ratios ---
#         def calculate_cash_to_total_assets_ratio(data, year):
#             return data.get("CASH_TO_TOTAL_ASSETS_RATIO", {}).get(year)
#         self.ratios["Liquidity Ratios"]["Cash To Total Assets Ratio"] = self._calculate_ratio(calculate_cash_to_total_assets_ratio, data, year)

#         def calculate_investment_to_total_assets(data, year):
#             return data.get("INVESTMENT_TO_TOTAL_ASSETS", {}).get(year)
#         self.ratios["Liquidity Ratios"]["Investment To Total Assets"] = self._calculate_ratio(calculate_investment_to_total_assets, data, year)

#         def calculate_advances_to_total_assets(data, year):
#             return data.get("ADVANCES_TO_TOTAL_ASSETS", {}).get(year)
#         self.ratios["Liquidity Ratios"]["Advances To Total Assets"] = self._calculate_ratio(calculate_advances_to_total_assets, data, year)

#         def calculate_deposits_to_total_assets(data, year):
#             return data.get("DEPOSIT_TO_TOTAL_ASSETS", {}).get(year)
#         self.ratios["Liquidity Ratios"]["Deposits To Total Assets"] = self._calculate_ratio(calculate_deposits_to_total_assets, data, year)

#         def calculate_total_liabilities_to_total_assets(data, year):
#             return data.get("TOTAL_LIABILITIES_TO_TOTAL_ASSETS", {}).get(year)
#         self.ratios["Liquidity Ratios"]["Total Liabilities To Total Assets"] = self._calculate_ratio(calculate_total_liabilities_to_total_assets, data, year)

#         def calculate_gross_advances_to_deposit(data, year):
#             return data.get("GROSS_ADVANCES_TO_DEPOSITS", {}).get(year)
#         self.ratios["Liquidity Ratios"]["Gross Advances To Deposits"] = self._calculate_ratio(calculate_gross_advances_to_deposit, data, year)

#         def calculate_gross_advances_to_borrowing_and_deposit(data, year):
#             return data.get("GROSS_ADVANCES_TO_BORROWING_AND_DEPOSIT", {}).get(year)
#         self.ratios["Liquidity Ratios"]["Gross Advances To Borrowing And Deposits"] = self._calculate_ratio(calculate_gross_advances_to_borrowing_and_deposit, data, year)

#         # ASSETS QUALITY RATIOS
#         def calculate_non_performing_loans_to_gross_advances(data, year):
#             return data.get("NON_PERFORMING_LOANS_TO_GROSS_ADVANCES", {}).get(year)
#         self.ratios["Asset Quality Ratios"]["Non-Performing Loans to Gross Advances"] = self._calculate_ratio(calculate_non_performing_loans_to_gross_advances, data, year)

#         def calculate_provisions_against_npls_to_gross_advances(data, year):
#             return data.get("PROVISION_AGAINST_NPLS_TO_GROSS_ADVANCES", {}).get(year)
#         self.ratios["Asset Quality Ratios"]["Provisions Against NPLs to Gross Advances"] = self._calculate_ratio(calculate_provisions_against_npls_to_gross_advances, data, year)

#         def calculate_npl_to_total_equity(data, year):
#             return data.get("NPL_TO_TOTAL_EQUITY", {}).get(year)
#         self.ratios["Asset Quality Ratios"]["NPL to Total Equity"] = self._calculate_ratio(calculate_npl_to_total_equity, data, year)

#         # --- Solvency Ratios ---
#         def calculate_capital_ratio(data, year):
#             return data.get("CAPITAL_RATIO", {}).get(year)
#         self.ratios["Solvency Ratios"]["Capital Ratio"] = self._calculate_ratio(calculate_capital_ratio, data, year)

#         def calculate_total_deposit_to_equity_ratio(data, year):
#             return data.get("TOTAL_DEPOSIT_TO_EQUITY_RATIO", {}).get(year)
#         self.ratios["Solvency Ratios"]["Total deposit to equity Ratio"] = self._calculate_ratio(calculate_total_deposit_to_equity_ratio, data, year)


# class FinancialRatiosService:
#     """
#     Service layer for calculating financial ratios for both companies and banks.
#     It orchestrates data fetching from FinancialVariablesService and then applies
#     the appropriate ratio calculation logic.
#     """
#     def _get_rank(self, org_name: str, org_value: float, all_orgs_values: list[tuple[str, float]], higher_is_better: bool = True) -> int:
#         """
#         Calculates the rank of an organization's value within a list of all organizations' values.

#         Args:
#             org_name (str): The name of the organization to rank.
#             org_value (float): The value of the specific organization.
#             all_orgs_values (list[tuple[str, float]]): List of (organization_name, value) tuples for the sector.
#             higher_is_better (bool): True if higher values mean better rank (e.g., Revenue),
#                                      False if lower values mean better rank (e.g., NPLs).

#         Returns:
#             int: The rank (1-based), or None if the organization's value is None, not found, or no valid data.
#         """
#         if org_value is None or pd.isna(org_value):
#             return None

#         # Create a Series for ranking from valid organization data
#         valid_orgs_data = {name: val for name, val in all_orgs_values if val is not None and pd.notna(val)}
#         if not valid_orgs_data:
#             return None # No valid data to rank against

#         temp_series = pd.Series(valid_orgs_data)

#         # Rank the series. 'dense' method gives consecutive ranks without gaps.
#         # `ascending=False` for higher_is_better (e.g., Revenue: 1st is highest)
#         # `ascending=True` for lower_is_better (e.g., NPLs: 1st is lowest)
#         ranked_series = temp_series.rank(method='dense', ascending=not higher_is_better)

#         # Get the rank of the specific organization
#         rank = ranked_series.get(org_name)

#         if pd.notna(rank):
#             return int(rank)
#         return None


#     def calculate_financial_ratios_for_specific_entity(self, entity_type: str, sector: str = None, sub_sector: str = None, org_name: str = None, target_year: str = None) -> dict:
#         """
#         Calculates financial ratios for a specific organization based on extracted data.

#         Args:
#             entity_type (str): The type of entity ("company" or "bank").
#             sector (str): The sector of the organization.
#             sub_sector (str): The sub-sector of the organization.
#             org_name (str): The name of the organization.
#             target_year (str, optional): The year for which to calculate ratios.
#                                          If 'all', calculates for all available years. Defaults to None.

#         Returns:
#             dict: A dictionary containing the calculated ratios, categorized by type,
#                   plus Revenue and Assets details with ranking.
#                   Returns an empty dictionary if no data is fetched or ratios cannot be calculated.
#         """
#         # Fetch specific variables for the organization using the FinancialVariablesService
#         extracted_data = financial_variables_service_instance.get_specific_variables_for_specific_org(
#             entity_type=entity_type,
#             sector=sector,
#             sub_sector=sub_sector,
#             org_name=org_name,
#             target_year=target_year # Pass target_year to filter variables
#         )

#         if not extracted_data: # Check if the dictionary is empty or None
#             print(f"No specific financial variables found for {org_name} in {sector} {sub_sector} for year {target_year}.")
#             return {}

#         # Convert target_year to integer for fetching specific variables for ranking
#         target_year_int = None
#         if target_year is not None and str(target_year).lower() != 'all':
#             try:
#                 target_year_int = int(target_year)
#             except ValueError:
#                 print(f"Error: target_year '{target_year}' cannot be converted to an integer. Cannot perform ranking.")
#                 # Still proceed with ratios, but ranking info will be missing
        
#         # Initialize results with existing ratio calculation
#         final_results = {}
#         calculator = None

#         # --- Determine calculator and specific labels ---
#         revenue_var_key = "REVENUE"
#         assets_var_key = "ASSETS"
        
#         # Initialize for type hinting or default clarity
#         revenue_prefix_for_display = "" 
#         assets_prefix_for_display = ""

#         if entity_type.lower() == "company":
#             calculator = CompanyFinancialRatiosCalculator(extracted_data, target_year)
#             revenue_prefix_for_display = "Sales"
#             assets_prefix_for_display = "Assets"
#         elif entity_type.lower() == "bank":
#             calculator = BankFinancialRatiosCalculator(extracted_data, target_year)
#             revenue_prefix_for_display = "Revenue" # As per your requirement: "Revenue in 2023 N/A"
#             assets_prefix_for_display = "Assets"  # As per your requirement: "Assets as of 2023..."
#         else:
#             print(f"Error: Invalid entity type: {entity_type}. Must be 'company' or 'bank'.")
#             return {}

#         calculator.calculate_ratios()
#         final_results.update(calculator.get_ratios()) # Add existing ratios

#         # --- Add Revenue and Assets with Ranking (only if target_year is a specific year) ---
#         if target_year_int is not None:
#             # Fetch all organizations' revenue for ranking using the internal 'revenue_var_key'
#             all_orgs_revenue_data = financial_variables_service_instance.get_all_organizations_variable_for_year_by_sector(
#                 entity_type=entity_type,
#                 sector=sector,
#                 variable_key=revenue_var_key,
#                 target_year=target_year_int
#             )
            
#             # Fetch all organizations' assets for ranking using the internal 'assets_var_key'
#             all_orgs_assets_data = financial_variables_service_instance.get_all_organizations_variable_for_year_by_sector(
#                 entity_type=entity_type,
#                 sector=sector,
#                 variable_key=assets_var_key,
#                 target_year=target_year_int
#             )

#             # Get the specific organization's values for the target year
#             org_revenue_value = extracted_data.get(revenue_var_key, {}).get(target_year_int)
#             org_assets_value = extracted_data.get(assets_var_key, {}).get(target_year_int)
            
#             # Determine ranks
#             revenue_rank = self._get_rank(org_name, org_revenue_value, all_orgs_revenue_data, higher_is_better=True)
#             assets_rank = self._get_rank(org_name, org_assets_value, all_orgs_assets_data, higher_is_better=True) 

#             sector_display_name = f"{sector} Sector" if sector else "Industry"
            
#             # --- Revenue formatting ---
#             # Special case for banks: Revenue should always be "N/A"
#             if entity_type.lower() == "bank":
#                 final_results["RevenueDetails"] = f"Revenue in {target_year_int} N/A"
#             else: # For companies
#                 revenue_display = "N/A"
#                 if org_revenue_value is not None and pd.notna(org_revenue_value):
#                     revenue_display = f"Rs. {org_revenue_value:,.3f} Million"
#                     if revenue_rank is not None:
#                         revenue_display += f" (ranked {revenue_rank} in {sector_display_name})"
#                 final_results["RevenueDetails"] = f"{revenue_prefix_for_display} in {target_year_int} {revenue_display}"

#             # --- Assets formatting ---
#             assets_display = "N/A"
#             if org_assets_value is not None and pd.notna(org_assets_value):
#                 assets_display = f"Rs. {org_assets_value:,.3f} Million"
#                 if assets_rank is not None:
#                     assets_display += f" (ranked {assets_rank} in {sector_display_name})"
            
#             # The AssetsDetails prefix should be dynamic based on entity type as well,
#             # but the value part (Rs. X Million...) is generally the same.
#             # Your original request implies a simpler prefix for both: "Assets as of 2023"
#             final_results["AssetsDetails"] = f"Assets as of {target_year_int} {assets_display}"


#         return final_results

#     def calculate_financial_ratios_for_specific_sector(self, entity_type: str, sector: str, target_year: str = None) -> dict:
#         """
#         Calculates the average financial ratios for all organizations within a given sector
#         (including all sub-sectors).

#         Args:
#             entity_type (str): The type of entity ("company" or "bank").
#             sector (str): The sector for which to calculate average ratios.
#             target_year (str, optional): The year for which to calculate ratios.
#                                          If 'all', calculates for all available years. Defaults to None.

#         Returns:
#             dict: A dictionary containing the calculated average ratios, categorized by type.
#                   Returns an empty dictionary if no data is fetched or ratios cannot be calculated.
#         """
#         # Fetch aggregated variables for the sector using the FinancialVariablesService
#         sector_data = financial_variables_service_instance.get_specific_variables_by_sector(
#             entity_type=entity_type,
#             sector=sector,
#             target_year=target_year # Pass target_year to filter variables
#         )

#         if not sector_data: # Check if the dictionary is empty or None
#             print(f"No sector data found for {sector} for year {target_year}.")
#             return {}

#         calculator = None
#         if entity_type.lower() == "company":
#             calculator = CompanyFinancialRatiosCalculator(sector_data, target_year)
#         elif entity_type.lower() == "bank":
#             calculator = BankFinancialRatiosCalculator(sector_data, target_year)
#         else:
#             print(f"Error: Invalid entity type: {entity_type}. Must be 'company' or 'bank'.")
#             return {}

#         calculator.calculate_ratios()
#         return calculator.get_ratios()

# # Instantiate the service for use in views
# financial_ratios_service_instance = FinancialRatiosService()





# import pandas as pd
# # Import instances of previously defined services to fetch data
# # from credit_risk.services.FinancialVariablesService import financial_variables_service_instance
# from .FinancialVariablesService import financial_variables_service_instance

# class FinancialRatiosCalculator:
#     """
#     Base class for calculating financial ratios. Provides common utilities for
#     handling extracted financial data and calculating ratios across years.
#     """
#     def __init__(self, extracted_data: dict, target_year: str = None):
#         """
#         Initializes the calculator with extracted data and target year.

#         Args:
#             extracted_data (dict): A dictionary containing financial variables,
#                                    typically fetched by FinancialVariablesService.
#             target_year (str, optional): The year for which to calculate ratios.
#                                          Can be an integer year (as string) or 'all'.
#                                          Defaults to None (which implies 'all').
#         """
#         self.extracted_data = extracted_data
#         self.target_year = target_year
#         self.ratios = {}  # Initialize an empty dictionary to store calculated ratios

#     def _calculate_ratio(self, ratio_func, data: dict, year_input=None):
#         """
#         Helper function to calculate a single ratio for a given year or all years.

#         Args:
#             ratio_func (callable): A function that takes data (dict) and a single year (int)
#                                    and returns the calculated ratio for that year.
#             data (dict): The extracted financial variables.
#             year_input (str, optional): The year for which to calculate ratios.
#                                          Can be an integer year (as string) or 'all'.
#                                          Defaults to None.

#         Returns:
#             dict or float or None: A dictionary of year-to-ratio mappings if 'all' years
#                                    are requested, or a single float/None if a specific
#                                    year is requested. Returns None if calculation fails.
#         """
#         if year_input is None or str(year_input).lower() == 'all':
#             # Collect all unique years present in the extracted data
#             years = set()
#             for var_name in data:
#                 if isinstance(data.get(var_name), dict):
#                     years.update(data[var_name].keys())
            
#             result = {}
#             for y in sorted(list(years)): # Sort years for consistent output
#                 try:
#                     # Ensure year 'y' is an integer for ratio_func
#                     calculated_val = ratio_func(data, int(y))
#                     result[y] = calculated_val if pd.notna(calculated_val) else None # Handle NaN
#                 except Exception as e:
#                     # print(f"Error calculating ratio for year {y}: {e}") # Suppress for cleaner output unless debugging
#                     result[y] = None
#             return result
#         else:
#             try:
#                 # Convert the target_year to an integer for calculation
#                 year_int = int(year_input)
#                 calculated_val = ratio_func(data, year_int)
#                 return calculated_val if pd.notna(calculated_val) else None # Handle NaN
#             except ValueError:
#                 print(f"Error: target_year '{year_input}' cannot be converted to an integer.")
#                 return None
#             except Exception as e:
#                 # print(f"Error calculating ratio for year {year_input}: {e}") # Suppress for cleaner output unless debugging
#                 return None

#     def calculate_ratios(self):
#         """
#         Calculates all financial ratios. This is the main entry point for ratio calculation.
#         Subclasses must implement this method.
#         """
#         raise NotImplementedError("Subclasses must implement this method")

#     def get_ratios(self) -> dict:
#         """
#         Returns the calculated ratios.
#         """
#         return self.ratios


# class CompanyFinancialRatiosCalculator(FinancialRatiosCalculator):
#     """
#     Calculates financial ratios specifically for companies.
#     """
#     def __init__(self, extracted_data: dict, target_year: str = None):
#         super().__init__(extracted_data, target_year)
#         self.ratios = {
#             "Profitability Ratios": {},
#             "Efficiency Ratios": {},
#             "Liquidity Ratios": {},
#             "Solvency Ratios": {},
#         }

#     def calculate_ratios(self):
#         """
#         Calculates financial ratios for companies based on the extracted data.
#         """
#         data = self.extracted_data
#         year = self.target_year

#         # --- Profitability Ratios ---
#         def calculate_net_profit_margin(data, year):
#             return data.get("NET_PROFIT_MARGIN", {}).get(year)
#         self.ratios["Profitability Ratios"]["Net Profit Margin"] = self._calculate_ratio(calculate_net_profit_margin, data, year)

#         def calculate_roa(data, year):
#             return data.get("RETURN_ON_ASSETS", {}).get(year)
#         self.ratios["Profitability Ratios"]["Return On Assets"] = self._calculate_ratio(calculate_roa, data, year)

#         def calculate_roe(data, year):
#             return data.get("RETURN_ON_EQUITY", {}).get(year)
#         self.ratios["Profitability Ratios"]["Return On Equity"] = self._calculate_ratio(calculate_roe, data, year)

#         def calculate_gpm(data, year):
#             return data.get("GROSS_PROFIT_MARGIN",{}).get(year)
#         self.ratios["Profitability Ratios"]["Gross Profit Margin"] = self._calculate_ratio(calculate_gpm, data, year)

#         def calculate_oroa(data, year):
#             return data.get("OPERATING_RETURN_ON_ASSETS",{}).get(year)
#         self.ratios["Profitability Ratios"]["Operating Return On Assets"] = self._calculate_ratio(calculate_oroa, data, year)

#         def calculate_roce(data, year):
#             return data.get("RETURN_ON_CAPITAL_EMPLOYED",{}).get(year)
#         self.ratios["Profitability Ratios"]["Return On Capital Employed"] = self._calculate_ratio(calculate_roce, data, year)

#         # --- Liquidity Ratios ---
#         def calculate_current_ratio(data, year):
#             return data.get("CURRENT_RATIO", {}).get(year)
#         self.ratios["Liquidity Ratios"]["Current Ratio"] = self._calculate_ratio(calculate_current_ratio, data, year)

#         def calculate_quick_ratio(data, year):
#             return data.get("QUICK_RATIO", {}).get(year)
#         self.ratios["Liquidity Ratios"]["Quick Ratio"] = self._calculate_ratio(calculate_quick_ratio, data, year)

#         def calculate_cash_to_current_liabilities_ratio(data, year):
#             return data.get("CASH_TO_CURRENT_LIABILITIES_RATIO", {}).get(year)
#         self.ratios["Liquidity Ratios"]["Cash To Current Liabilities Ratio"] = self._calculate_ratio(calculate_cash_to_current_liabilities_ratio, data, year)

#         # --- Efficiency Ratios ---
#         def calculate_no_of_days_in_inventory(data, year):
#             return data.get("NUM_OF_DAYS_IN_INVENTORY", {}).get(year)
#         self.ratios["Efficiency Ratios"]["Num Of Days In Inventory"] = self._calculate_ratio(calculate_no_of_days_in_inventory, data, year)

#         def calculate_no_of_days_in_receivables(data, year):
#             return data.get("NUM_OF_DAYS_IN_RECEIVABLES", {}).get(year)
#         self.ratios["Efficiency Ratios"]["Num Of Days In Receivables"] = self._calculate_ratio(calculate_no_of_days_in_receivables, data, year)

#         def calculate_no_of_days_in_payable(data, year):
#             return data.get("NUM_OF_DAYS_IN_PAYABLE", {}).get(year)
#         self.ratios["Efficiency Ratios"]["Num Of Days In Payable"] = self._calculate_ratio(calculate_no_of_days_in_payable, data, year)

#         # --- Solvency Ratios ---
#         def calculate_debt_equity_ratio(data, year):
#             return data.get("DEBT_EQUITY_RATIO", {}).get(year)
#         self.ratios["Solvency Ratios"]["Debt Equity Ratio"] = self._calculate_ratio(calculate_debt_equity_ratio, data, year)

#         def calculate_debt_assets_ratio(data, year):
#             return data.get("DEBT_TO_ASSETS_RATIO", {}).get(year)
#         self.ratios["Solvency Ratios"]["Debt Asset Ratio"] = self._calculate_ratio(calculate_debt_assets_ratio, data, year)

#         def calculate_debt_capital_ratio(data, year):
#             return data.get("DEBT_TO_CAPITAL_RATIO", {}).get(year)
#         self.ratios["Solvency Ratios"]["Debt Capital Ratio"] = self._calculate_ratio(calculate_debt_capital_ratio, data, year)

#         def calculate_interest_coverage_ratio(data, year):
#             return data.get("INTEREST_COVER_RATIO", {}).get(year)
#         self.ratios["Solvency Ratios"]["Interest Coverage Ratio"] = self._calculate_ratio(calculate_interest_coverage_ratio, data, year)


# class BankFinancialRatiosCalculator(FinancialRatiosCalculator):
#     """
#     Calculates financial ratios specifically for banks.
#     """
#     def __init__(self, extracted_data: dict, target_year: str = None):
#         super().__init__(extracted_data, target_year)
#         self.ratios = {
#             "Profitability And Efficiency Ratios": {},
#             "Liquidity Ratios": {},
#             "Asset Quality Ratios": {},
#             "Solvency Ratios": {}
#         }

#     def calculate_ratios(self):
#         """
#         Calculates financial ratios for banks based on the extracted data.
#         """
#         data = self.extracted_data
#         year = self.target_year

#         # --- Profitability And Efficiency Ratios ---
#         def calculate_spread_ratio(data, year):
#             return data.get("SPREAD_RATIO", {}).get(year)
#         self.ratios["Profitability And Efficiency Ratios"]["Spread Ratio"] = self._calculate_ratio(calculate_spread_ratio, data, year)

#         def calculate_net_interest_margin(data, year):
#             return data.get("NET_INTEREST_MARGIN", {}).get(year)
#         self.ratios["Profitability And Efficiency Ratios"]["Net Interest Margin"] = self._calculate_ratio(calculate_net_interest_margin, data, year)

#         def calculate_return_on_equity(data, year):
#             return data.get("RETURN_ON_EQUITY", {}).get(year)
#         self.ratios["Profitability And Efficiency Ratios"]["Return On Equity"] = self._calculate_ratio(calculate_return_on_equity, data, year)

#         def calculate_return_on_assets(data, year):
#             return data.get("RETURN_ON_ASSETS", {}).get(year)
#         self.ratios["Profitability And Efficiency Ratios"]["Return On Assets"] = self._calculate_ratio(calculate_return_on_assets, data, year)

#         def calculate_non_interest_income_ratio(data, year):
#             return data.get("NON_INTEREST_INCOME_RATIO", {}).get(year)
#         self.ratios["Profitability And Efficiency Ratios"]["Non Interest Income Ratio"] = self._calculate_ratio(calculate_non_interest_income_ratio, data, year)

#         # --- Liquidity Ratios ---
#         def calculate_cash_to_total_assets_ratio(data, year):
#             return data.get("CASH_TO_TOTAL_ASSETS_RATIO", {}).get(year)
#         self.ratios["Liquidity Ratios"]["Cash To Total Assets Ratio"] = self._calculate_ratio(calculate_cash_to_total_assets_ratio, data, year)

#         def calculate_investment_to_total_assets(data, year):
#             return data.get("INVESTMENT_TO_TOTAL_ASSETS", {}).get(year)
#         self.ratios["Liquidity Ratios"]["Investment To Total Assets"] = self._calculate_ratio(calculate_investment_to_total_assets, data, year)

#         def calculate_advances_to_total_assets(data, year):
#             return data.get("ADVANCES_TO_TOTAL_ASSETS", {}).get(year)
#         self.ratios["Liquidity Ratios"]["Advances To Total Assets"] = self._calculate_ratio(calculate_advances_to_total_assets, data, year)

#         def calculate_deposits_to_total_assets(data, year):
#             return data.get("DEPOSIT_TO_TOTAL_ASSETS", {}).get(year)
#         self.ratios["Liquidity Ratios"]["Deposits To Total Assets"] = self._calculate_ratio(calculate_deposits_to_total_assets, data, year)

#         def calculate_total_liabilities_to_total_assets(data, year):
#             return data.get("TOTAL_LIABILITIES_TO_TOTAL_ASSETS", {}).get(year)
#         self.ratios["Liquidity Ratios"]["Total Liabilities To Total Assets"] = self._calculate_ratio(calculate_total_liabilities_to_total_assets, data, year)

#         def calculate_gross_advances_to_deposit(data, year):
#             return data.get("GROSS_ADVANCES_TO_DEPOSITS", {}).get(year)
#         self.ratios["Liquidity Ratios"]["Gross Advances To Deposits"] = self._calculate_ratio(calculate_gross_advances_to_deposit, data, year)

#         def calculate_gross_advances_to_borrowing_and_deposit(data, year):
#             return data.get("GROSS_ADVANCES_TO_BORROWING_AND_DEPOSIT", {}).get(year)
#         self.ratios["Liquidity Ratios"]["Gross Advances To Borrowing And Deposits"] = self._calculate_ratio(calculate_gross_advances_to_borrowing_and_deposit, data, year)

#         # ASSETS QUALITY RATIOS
#         def calculate_non_performing_loans_to_gross_advances(data, year):
#             return data.get("NON_PERFORMING_LOANS_TO_GROSS_ADVANCES", {}).get(year)
#         self.ratios["Asset Quality Ratios"]["Non-Performing Loans to Gross Advances"] = self._calculate_ratio(calculate_non_performing_loans_to_gross_advances, data, year)

#         def calculate_provisions_against_npls_to_gross_advances(data, year):
#             return data.get("PROVISION_AGAINST_NPLS_TO_GROSS_ADVANCES", {}).get(year)
#         self.ratios["Asset Quality Ratios"]["Provisions Against NPLs to Gross Advances"] = self._calculate_ratio(calculate_provisions_against_npls_to_gross_advances, data, year)

#         def calculate_npl_to_total_equity(data, year):
#             return data.get("NPL_TO_TOTAL_EQUITY", {}).get(year)
#         self.ratios["Asset Quality Ratios"]["NPL to Total Equity"] = self._calculate_ratio(calculate_npl_to_total_equity, data, year)

#         # --- Solvency Ratios ---
#         def calculate_capital_ratio(data, year):
#             return data.get("CAPITAL_RATIO", {}).get(year)
#         self.ratios["Solvency Ratios"]["Capital Ratio"] = self._calculate_ratio(calculate_capital_ratio, data, year)

#         def calculate_total_deposit_to_equity_ratio(data, year):
#             return data.get("TOTAL_DEPOSIT_TO_EQUITY_RATIO", {}).get(year)
#         self.ratios["Solvency Ratios"]["Total deposit to equity Ratio"] = self._calculate_ratio(calculate_total_deposit_to_equity_ratio, data, year)


# class FinancialRatiosService:
#     """
#     Service layer for calculating financial ratios for both companies and banks.
#     It orchestrates data fetching from FinancialVariablesService and then applies
#     the appropriate ratio calculation logic.
#     """
#     def _get_rank(self, org_name: str, org_value: float, all_orgs_values: list[tuple[str, float]], higher_is_better: bool = True) -> tuple[int | None, int | None]:
#         """
#         Calculates the rank of an organization's value within a list of all organizations' values.

#         Args:
#             org_name (str): The name of the organization to rank.
#             org_value (float): The value of the specific organization.
#             all_orgs_values (list[tuple[str, float]]): List of (organization_name, value) tuples for the sector.
#             higher_is_better (bool): True if higher values mean better rank (e.g., Revenue),
#                                      False if lower values mean better rank (e.g., NPLs).

#         Returns:
#             tuple[int | None, int | None]: A tuple containing (rank, total_organizations).
#                                          Returns (None, None) if the organization's value is None,
#                                          not found, or no valid data to rank against.
#         """
#         if org_value is None or pd.isna(org_value):
#             return None, None

#         # Create a Series for ranking from valid organization data
#         valid_orgs_data = {name: val for name, val in all_orgs_values if val is not None and pd.notna(val)}
        
#         # Get the total count of valid organizations *before* ranking
#         total_valid_orgs = len(valid_orgs_data)

#         if not valid_orgs_data:
#             return None, None # No valid data to rank against

#         temp_series = pd.Series(valid_orgs_data)

#         # Rank the series. 'dense' method gives consecutive ranks without gaps.
#         # `ascending=False` for higher_is_better (e.g., Revenue: 1st is highest)
#         # `ascending=True` for lower_is_better (e.g., NPLs: 1st is lowest)
#         ranked_series = temp_series.rank(method='dense', ascending=not higher_is_better)

#         # Get the rank of the specific organization
#         rank = ranked_series.get(org_name)

#         if pd.notna(rank):
#             return int(rank), total_valid_orgs
#         return None, None


#     def calculate_financial_ratios_for_specific_entity(self, entity_type: str, sector: str = None, sub_sector: str = None, org_name: str = None, target_year: str = None) -> dict:
#         """
#         Calculates financial ratios for a specific organization based on extracted data.

#         Args:
#             entity_type (str): The type of entity ("company" or "bank").
#             sector (str): The sector of the organization.
#             sub_sector (str): The sub-sector of the organization.
#             org_name (str): The name of the organization.
#             target_year (str, optional): The year for which to calculate ratios.
#                                          If 'all', calculates for all available years. Defaults to None.

#         Returns:
#             dict: A dictionary containing the calculated ratios, categorized by type,
#                   plus Revenue and Assets details with ranking.
#                   Returns an empty dictionary if no data is fetched or ratios cannot be calculated.
#         """
#         # Fetch specific variables for the organization using the FinancialVariablesService
#         extracted_data = financial_variables_service_instance.get_specific_variables_for_specific_org(
#             entity_type=entity_type,
#             sector=sector,
#             sub_sector=sub_sector,
#             org_name=org_name,
#             target_year=target_year # Pass target_year to filter variables
#         )

#         if not extracted_data: # Check if the dictionary is empty or None
#             print(f"No specific financial variables found for {org_name} in {sector} {sub_sector} for year {target_year}.")
#             return {}

#         # Convert target_year to integer for fetching specific variables for ranking
#         target_year_int = None
#         if target_year is not None and str(target_year).lower() != 'all':
#             try:
#                 target_year_int = int(target_year)
#             except ValueError:
#                 print(f"Error: target_year '{target_year}' cannot be converted to an integer. Cannot perform ranking.")
#                 # Still proceed with ratios, but ranking info will be missing
        
#         # Initialize results with existing ratio calculation
#         final_results = {}
#         calculator = None

#         # --- Determine calculator and specific labels ---
#         revenue_var_key = "REVENUE"
#         assets_var_key = "ASSETS"
        
#         # Initialize for type hinting or default clarity
#         revenue_prefix_for_display = "" 
#         assets_prefix_for_display = ""

#         if entity_type.lower() == "company":
#             calculator = CompanyFinancialRatiosCalculator(extracted_data, target_year)
#             revenue_prefix_for_display = "Sales"
#             assets_prefix_for_display = "Assets"
#         elif entity_type.lower() == "bank":
#             calculator = BankFinancialRatiosCalculator(extracted_data, target_year)
#             revenue_prefix_for_display = "Revenue" # As per your requirement: "Revenue in 2023 N/A"
#             assets_prefix_for_display = "Assets"  # As per your requirement: "Assets as of 2023..."
#         else:
#             print(f"Error: Invalid entity type: {entity_type}. Must be 'company' or 'bank'.")
#             return {}

#         calculator.calculate_ratios()
#         final_results.update(calculator.get_ratios()) # Add existing ratios

#         # --- Add Revenue and Assets with Ranking (only if target_year is a specific year) ---
#         if target_year_int is not None:
#             # Fetch all organizations' revenue for ranking using the internal 'revenue_var_key'
#             all_orgs_revenue_data = financial_variables_service_instance.get_all_organizations_variable_for_year_by_sector(
#                 entity_type=entity_type,
#                 sector=sector,
#                 variable_key=revenue_var_key,
#                 target_year=target_year_int
#             )
            
#             # Fetch all organizations' assets for ranking using the internal 'assets_var_key'
#             all_orgs_assets_data = financial_variables_service_instance.get_all_organizations_variable_for_year_by_sector(
#                 entity_type=entity_type,
#                 sector=sector,
#                 variable_key=assets_var_key,
#                 target_year=target_year_int
#             )

#             # Get the specific organization's values for the target year
#             org_revenue_value = extracted_data.get(revenue_var_key, {}).get(target_year_int)
#             org_assets_value = extracted_data.get(assets_var_key, {}).get(target_year_int)
            
#             # Determine ranks and total count
#             revenue_rank, total_revenue_orgs = self._get_rank(org_name, org_revenue_value, all_orgs_revenue_data, higher_is_better=True)
#             assets_rank, total_assets_orgs = self._get_rank(org_name, org_assets_value, all_orgs_assets_data, higher_is_better=True) 

#             sector_display_name = f"{sector} Sector" if sector else "Industry"
            
#             # --- Revenue formatting ---
#             # Special case for banks: Revenue should always be "N/A"
#             if entity_type.lower() == "bank":
#                 final_results["RevenueDetails"] = f"Revenue in {target_year_int} N/A"
#             else: # For companies
#                 revenue_display = "N/A"
#                 if org_revenue_value is not None and pd.notna(org_revenue_value):
#                     revenue_display = f"Rs. {org_revenue_value:,.3f} Million"
#                     if revenue_rank is not None and total_revenue_orgs is not None:
#                         revenue_display += f" (ranked {revenue_rank} out of {total_revenue_orgs} in {sector_display_name})"
#                     elif revenue_rank is not None: # Fallback if total_revenue_orgs is somehow None but rank isn't
#                         revenue_display += f" (ranked {revenue_rank} in {sector_display_name})"
#                 final_results["RevenueDetails"] = f"{revenue_prefix_for_display} in {target_year_int} {revenue_display}"

#             # --- Assets formatting ---
#             assets_display = "N/A"
#             if org_assets_value is not None and pd.notna(org_assets_value):
#                 assets_display = f"Rs. {org_assets_value:,.3f} Million"
#                 if assets_rank is not None and total_assets_orgs is not None:
#                     assets_display += f" (ranked {assets_rank} out of {total_assets_orgs} in {sector_display_name})"
#                 elif assets_rank is not None: # Fallback if total_assets_orgs is somehow None but rank isn't
#                     assets_display += f" (ranked {assets_rank} in {sector_display_name})"
            
#             final_results["AssetsDetails"] = f"Assets as of {target_year_int} {assets_display}"


#         return final_results

#     def calculate_financial_ratios_for_specific_sector(self, entity_type: str, sector: str, target_year: str = None) -> dict:
#         """
#         Calculates the average financial ratios for all organizations within a given sector
#         (including all sub-sectors).

#         Args:
#             entity_type (str): The type of entity ("company" or "bank").
#             sector (str): The sector for which to calculate average ratios.
#             target_year (str, optional): The year for which to calculate ratios.
#                                          If 'all', calculates for all available years. Defaults to None.

#         Returns:
#             dict: A dictionary containing the calculated average ratios, categorized by type.
#                   Returns an empty dictionary if no data is fetched or ratios cannot be calculated.
#         """
#         # Fetch aggregated variables for the sector using the FinancialVariablesService
#         sector_data = financial_variables_service_instance.get_specific_variables_by_sector(
#             entity_type=entity_type,
#             sector=sector,
#             target_year=target_year # Pass target_year to filter variables
#         )

#         if not sector_data: # Check if the dictionary is empty or None
#             print(f"No sector data found for {sector} for year {target_year}.")
#             return {}

#         calculator = None
#         if entity_type.lower() == "company":
#             calculator = CompanyFinancialRatiosCalculator(sector_data, target_year)
#         elif entity_type.lower() == "bank":
#             calculator = BankFinancialRatiosCalculator(sector_data, target_year)
#         else:
#             print(f"Error: Invalid entity type: {entity_type}. Must be 'company' or 'bank'.")
#             return {}

#         calculator.calculate_ratios()
#         return calculator.get_ratios()

# # Instantiate the service for use in views
# financial_ratios_service_instance = FinancialRatiosService()







# import pandas as pd
# # Import instances of previously defined services to fetch data
# # from credit_risk.services.FinancialVariablesService import financial_variables_service_instance
# from .FinancialVariablesService import financial_variables_service_instance

# class FinancialRatiosCalculator:
#     """
#     Base class for calculating financial ratios. Provides common utilities for
#     handling extracted financial data and calculating ratios across years.
#     """
#     def __init__(self, extracted_data: dict, target_year: str = None):
#         """
#         Initializes the calculator with extracted data and target year.

#         Args:
#             extracted_data (dict): A dictionary containing financial variables,
#                                    typically fetched by FinancialVariablesService.
#             target_year (str, optional): The year for which to calculate ratios.
#                                          Can be an integer year (as string) or 'all'.
#                                          Defaults to None (which implies 'all').
#         """
#         self.extracted_data = extracted_data
#         self.target_year = target_year
#         self.ratios = {}  # Initialize an empty dictionary to store calculated ratios

#     def _calculate_ratio(self, ratio_func, data: dict, year_input=None):
#         """
#         Helper function to calculate a single ratio for a given year or all years.

#         Args:
#             ratio_func (callable): A function that takes data (dict) and a single year (int)
#                                    and returns the calculated ratio for that year.
#             data (dict): The extracted financial variables.
#             year_input (str, optional): The year for which to calculate ratios.
#                                          Can be an integer year (as string) or 'all'.
#                                          Defaults to None.

#         Returns:
#             dict or float or None: A dictionary of year-to-ratio mappings if 'all' years
#                                    are requested, or a single float/None if a specific
#                                    year is requested. Returns None if calculation fails.
#         """
#         if year_input is None or str(year_input).lower() == 'all':
#             # Collect all unique years present in the extracted data
#             years = set()
#             for var_name in data:
#                 if isinstance(data.get(var_name), dict):
#                     years.update(data[var_name].keys())
            
#             result = {}
#             for y in sorted(list(years)): # Sort years for consistent output
#                 try:
#                     # Ensure year 'y' is an integer for ratio_func
#                     calculated_val = ratio_func(data, int(y))
#                     result[y] = calculated_val if pd.notna(calculated_val) else None # Handle NaN
#                 except Exception as e:
#                     # print(f"Error calculating ratio for year {y}: {e}") # Suppress for cleaner output unless debugging
#                     result[y] = None
#             return result
#         else:
#             try:
#                 # Convert the target_year to an integer for calculation
#                 year_int = int(year_input)
#                 calculated_val = ratio_func(data, year_int)
#                 return calculated_val if pd.notna(calculated_val) else None # Handle NaN
#             except ValueError:
#                 print(f"Error: target_year '{year_input}' cannot be converted to an integer.")
#                 return None
#             except Exception as e:
#                 # print(f"Error calculating ratio for year {year_input}: {e}") # Suppress for cleaner output unless debugging
#                 return None

#     def calculate_ratios(self):
#         """
#         Calculates all financial ratios. This is the main entry point for ratio calculation.
#         Subclasses must implement this method.
#         """
#         raise NotImplementedError("Subclasses must implement this method")

#     def get_ratios(self) -> dict:
#         """
#         Returns the calculated ratios.
#         """
#         return self.ratios


# class CompanyFinancialRatiosCalculator(FinancialRatiosCalculator):
#     """
#     Calculates financial ratios specifically for companies.
#     """
#     def __init__(self, extracted_data: dict, target_year: str = None):
#         super().__init__(extracted_data, target_year)
#         self.ratios = {
#             "Profitability Ratios": {},
#             "Efficiency Ratios": {},
#             "Liquidity Ratios": {},
#             "Solvency Ratios": {},
#         }

#     def calculate_ratios(self):
#         """
#         Calculates financial ratios for companies based on the extracted data.
#         """
#         data = self.extracted_data
#         year = self.target_year

#         # --- Profitability Ratios ---
#         def calculate_net_profit_margin(data, year):
#             return data.get("NET_PROFIT_MARGIN", {}).get(year)
#         self.ratios["Profitability Ratios"]["Net Profit Margin"] = self._calculate_ratio(calculate_net_profit_margin, data, year)

#         def calculate_roa(data, year):
#             return data.get("RETURN_ON_ASSETS", {}).get(year)
#         self.ratios["Profitability Ratios"]["Return On Assets"] = self._calculate_ratio(calculate_roa, data, year)

#         def calculate_roe(data, year):
#             return data.get("RETURN_ON_EQUITY", {}).get(year)
#         self.ratios["Profitability Ratios"]["Return On Equity"] = self._calculate_ratio(calculate_roe, data, year)

#         def calculate_gpm(data, year):
#             return data.get("GROSS_PROFIT_MARGIN",{}).get(year)
#         self.ratios["Profitability Ratios"]["Gross Profit Margin"] = self._calculate_ratio(calculate_gpm, data, year)

#         def calculate_oroa(data, year):
#             return data.get("OPERATING_RETURN_ON_ASSETS",{}).get(year)
#         self.ratios["Profitability Ratios"]["Operating Return On Assets"] = self._calculate_ratio(calculate_oroa, data, year)

#         def calculate_roce(data, year):
#             return data.get("RETURN_ON_CAPITAL_EMPLOYED",{}).get(year)
#         self.ratios["Profitability Ratios"]["Return On Capital Employed"] = self._calculate_ratio(calculate_roce, data, year)

#         # --- Liquidity Ratios ---
#         def calculate_current_ratio(data, year):
#             return data.get("CURRENT_RATIO", {}).get(year)
#         self.ratios["Liquidity Ratios"]["Current Ratio"] = self._calculate_ratio(calculate_current_ratio, data, year)

#         def calculate_quick_ratio(data, year):
#             return data.get("QUICK_RATIO", {}).get(year)
#         self.ratios["Liquidity Ratios"]["Quick Ratio"] = self._calculate_ratio(calculate_quick_ratio, data, year)

#         def calculate_cash_to_current_liabilities_ratio(data, year):
#             return data.get("CASH_TO_CURRENT_LIABILITIES_RATIO", {}).get(year)
#         self.ratios["Liquidity Ratios"]["Cash To Current Liabilities Ratio"] = self._calculate_ratio(calculate_cash_to_current_liabilities_ratio, data, year)

#         # --- Efficiency Ratios ---
#         def calculate_no_of_days_in_inventory(data, year):
#             return data.get("NUM_OF_DAYS_IN_INVENTORY", {}).get(year)
#         self.ratios["Efficiency Ratios"]["Num Of Days In Inventory"] = self._calculate_ratio(calculate_no_of_days_in_inventory, data, year)

#         def calculate_no_of_days_in_receivables(data, year):
#             return data.get("NUM_OF_DAYS_IN_RECEIVABLES", {}).get(year)
#         self.ratios["Efficiency Ratios"]["Num Of Days In Receivables"] = self._calculate_ratio(calculate_no_of_days_in_receivables, data, year)

#         def calculate_no_of_days_in_payable(data, year):
#             return data.get("NUM_OF_DAYS_IN_PAYABLE", {}).get(year)
#         self.ratios["Efficiency Ratios"]["Num Of Days In Payable"] = self._calculate_ratio(calculate_no_of_days_in_payable, data, year)

#         # --- Solvency Ratios ---
#         def calculate_debt_equity_ratio(data, year):
#             return data.get("DEBT_EQUITY_RATIO", {}).get(year)
#         self.ratios["Solvency Ratios"]["Debt Equity Ratio"] = self._calculate_ratio(calculate_debt_equity_ratio, data, year)

#         def calculate_debt_assets_ratio(data, year):
#             return data.get("DEBT_TO_ASSETS_RATIO", {}).get(year)
#         self.ratios["Solvency Ratios"]["Debt Asset Ratio"] = self._calculate_ratio(calculate_debt_assets_ratio, data, year)

#         def calculate_debt_capital_ratio(data, year):
#             return data.get("DEBT_TO_CAPITAL_RATIO", {}).get(year)
#         self.ratios["Solvency Ratios"]["Debt Capital Ratio"] = self._calculate_ratio(calculate_debt_capital_ratio, data, year)

#         def calculate_interest_coverage_ratio(data, year):
#             return data.get("INTEREST_COVER_RATIO", {}).get(year)
#         self.ratios["Solvency Ratios"]["Interest Coverage Ratio"] = self._calculate_ratio(calculate_interest_coverage_ratio, data, year)


# class BankFinancialRatiosCalculator(FinancialRatiosCalculator):
#     """
#     Calculates financial ratios specifically for banks.
#     """
#     def __init__(self, extracted_data: dict, target_year: str = None):
#         super().__init__(extracted_data, target_year)
#         self.ratios = {
#             "Profitability And Efficiency Ratios": {},
#             "Liquidity Ratios": {},
#             "Asset Quality Ratios": {},
#             "Solvency Ratios": {}
#         }

#     def calculate_ratios(self):
#         """
#         Calculates financial ratios for banks based on the extracted data.
#         """
#         data = self.extracted_data
#         year = self.target_year

#         # --- Profitability And Efficiency Ratios ---
#         def calculate_spread_ratio(data, year):
#             return data.get("SPREAD_RATIO", {}).get(year)
#         self.ratios["Profitability And Efficiency Ratios"]["Spread Ratio"] = self._calculate_ratio(calculate_spread_ratio, data, year)

#         def calculate_net_interest_margin(data, year):
#             return data.get("NET_INTEREST_MARGIN", {}).get(year)
#         self.ratios["Profitability And Efficiency Ratios"]["Net Interest Margin"] = self._calculate_ratio(calculate_net_interest_margin, data, year)

#         def calculate_return_on_equity(data, year):
#             return data.get("RETURN_ON_EQUITY", {}).get(year)
#         self.ratios["Profitability And Efficiency Ratios"]["Return On Equity"] = self._calculate_ratio(calculate_return_on_equity, data, year)

#         def calculate_return_on_assets(data, year):
#             return data.get("RETURN_ON_ASSETS", {}).get(year)
#         self.ratios["Profitability And Efficiency Ratios"]["Return On Assets"] = self._calculate_ratio(calculate_return_on_assets, data, year)

#         def calculate_non_interest_income_ratio(data, year):
#             return data.get("NON_INTEREST_INCOME_RATIO", {}).get(year)
#         self.ratios["Profitability And Efficiency Ratios"]["Non Interest Income Ratio"] = self._calculate_ratio(calculate_non_interest_income_ratio, data, year)

#         # --- Liquidity Ratios ---
#         def calculate_cash_to_total_assets_ratio(data, year):
#             return data.get("CASH_TO_TOTAL_ASSETS_RATIO", {}).get(year)
#         self.ratios["Liquidity Ratios"]["Cash To Total Assets Ratio"] = self._calculate_ratio(calculate_cash_to_total_assets_ratio, data, year)

#         def calculate_investment_to_total_assets(data, year):
#             return data.get("INVESTMENT_TO_TOTAL_ASSETS", {}).get(year)
#         self.ratios["Liquidity Ratios"]["Investment To Total Assets"] = self._calculate_ratio(calculate_investment_to_total_assets, data, year)

#         def calculate_advances_to_total_assets(data, year):
#             return data.get("ADVANCES_TO_TOTAL_ASSETS", {}).get(year)
#         self.ratios["Liquidity Ratios"]["Advances To Total Assets"] = self._calculate_ratio(calculate_advances_to_total_assets, data, year)

#         def calculate_deposits_to_total_assets(data, year):
#             return data.get("DEPOSIT_TO_TOTAL_ASSETS", {}).get(year)
#         self.ratios["Liquidity Ratios"]["Deposits To Total Assets"] = self._calculate_ratio(calculate_deposits_to_total_assets, data, year)

#         def calculate_total_liabilities_to_total_assets(data, year):
#             return data.get("TOTAL_LIABILITIES_TO_TOTAL_ASSETS", {}).get(year)
#         self.ratios["Liquidity Ratios"]["Total Liabilities To Total Assets"] = self._calculate_ratio(calculate_total_liabilities_to_total_assets, data, year)

#         def calculate_gross_advances_to_deposit(data, year):
#             return data.get("GROSS_ADVANCES_TO_DEPOSITS", {}).get(year)
#         self.ratios["Liquidity Ratios"]["Gross Advances To Deposits"] = self._calculate_ratio(calculate_gross_advances_to_deposit, data, year)

#         def calculate_gross_advances_to_borrowing_and_deposit(data, year):
#             return data.get("GROSS_ADVANCES_TO_BORROWING_AND_DEPOSIT", {}).get(year)
#         self.ratios["Liquidity Ratios"]["Gross Advances To Borrowing And Deposits"] = self._calculate_ratio(calculate_gross_advances_to_borrowing_and_deposit, data, year)

#         # ASSETS QUALITY RATIOS
#         def calculate_non_performing_loans_to_gross_advances(data, year):
#             return data.get("NON_PERFORMING_LOANS_TO_GROSS_ADVANCES", {}).get(year)
#         self.ratios["Asset Quality Ratios"]["Non-Performing Loans to Gross Advances"] = self._calculate_ratio(calculate_non_performing_loans_to_gross_advances, data, year)

#         def calculate_provisions_against_npls_to_gross_advances(data, year):
#             return data.get("PROVISION_AGAINST_NPLS_TO_GROSS_ADVANCES", {}).get(year)
#         self.ratios["Asset Quality Ratios"]["Provisions Against NPLs to Gross Advances"] = self._calculate_ratio(calculate_provisions_against_npls_to_gross_advances, data, year)

#         def calculate_npl_to_total_equity(data, year):
#             return data.get("NPL_TO_TOTAL_EQUITY", {}).get(year)
#         self.ratios["Asset Quality Ratios"]["NPL to Total Equity"] = self._calculate_ratio(calculate_npl_to_total_equity, data, year)

#         # --- Solvency Ratios ---
#         def calculate_capital_ratio(data, year):
#             return data.get("CAPITAL_RATIO", {}).get(year)
#         self.ratios["Solvency Ratios"]["Capital Ratio"] = self._calculate_ratio(calculate_capital_ratio, data, year)

#         def calculate_total_deposit_to_equity_ratio(data, year):
#             return data.get("TOTAL_DEPOSIT_TO_EQUITY_RATIO", {}).get(year)
#         self.ratios["Solvency Ratios"]["Total deposit to equity Ratio"] = self._calculate_ratio(calculate_total_deposit_to_equity_ratio, data, year)


# class FinancialRatiosService:
#     """
#     Service layer for calculating financial ratios for both companies and banks.
#     It orchestrates data fetching from FinancialVariablesService and then applies
#     the appropriate ratio calculation logic.
#     """
#     def _get_rank(self, org_name: str, org_value: float, all_orgs_values: list[tuple[str, float]], higher_is_better: bool = True) -> tuple[int | None, int | None]:
#         """
#         Calculates the rank of an organization's value within a list of all organizations' values.

#         Args:
#             org_name (str): The name of the organization to rank.
#             org_value (float): The value of the specific organization.
#             all_orgs_values (list[tuple[str, float]]): List of (organization_name, value) tuples for the sector.
#             higher_is_better (bool): True if higher values mean better rank (e.g., Revenue),
#                                      False if lower values mean better rank (e.g., NPLs).

#         Returns:
#             tuple[int | None, int | None]: A tuple containing (rank, total_organizations).
#                                          Returns (None, None) if the organization's value is None,
#                                          not found, or no valid data to rank against.
#         """
#         if org_value is None or pd.isna(org_value):
#             return None, None

#         # Create a Series for ranking from valid organization data
#         valid_orgs_data = {name: val for name, val in all_orgs_values if val is not None and pd.notna(val)}
        
#         # Get the total count of valid organizations *before* ranking
#         total_valid_orgs = len(valid_orgs_data)

#         if not valid_orgs_data:
#             return None, None # No valid data to rank against

#         temp_series = pd.Series(valid_orgs_data)

#         # Rank the series. 'dense' method gives consecutive ranks without gaps.
#         # `ascending=False` for higher_is_better (e.g., Revenue: 1st is highest)
#         # `ascending=True` for lower_is_better (e.g., NPLs: 1st is lowest)
#         ranked_series = temp_series.rank(method='dense', ascending=not higher_is_better)

#         # Get the rank of the specific organization
#         rank = ranked_series.get(org_name)

#         if pd.notna(rank):
#             return int(rank), total_valid_orgs
#         return None, None


#     def calculate_financial_ratios_for_specific_entity(self, entity_type: str, sector: str = None, sub_sector: str = None, org_name: str = None, target_year: str = None) -> dict:
#         """
#         Calculates financial ratios for a specific organization based on extracted data.

#         Args:
#             entity_type (str): The type of entity ("company" or "bank").
#             sector (str): The sector of the organization.
#             sub_sector (str): The sub-sector of the organization.
#             org_name (str): The name of the organization.
#             target_year (str, optional): The year for which to calculate ratios.
#                                          If 'all', calculates for all available years. Defaults to None.

#         Returns:
#             dict: A dictionary containing the calculated ratios, categorized by type,
#                   plus Revenue and Assets details with structured ranking.
#                   Returns an empty dictionary if no data is fetched or ratios cannot be calculated.
#         """
#         # Fetch specific variables for the organization using the FinancialVariablesService
#         extracted_data = financial_variables_service_instance.get_specific_variables_for_specific_org(
#             entity_type=entity_type,
#             sector=sector,
#             sub_sector=sub_sector,
#             org_name=org_name,
#             target_year=target_year # Pass target_year to filter variables
#         )

#         if not extracted_data: # Check if the dictionary is empty or None
#             print(f"No specific financial variables found for {org_name} in {sector} {sub_sector} for year {target_year}.")
#             return {}

#         # Convert target_year to integer for fetching specific variables for ranking
#         target_year_int = None
#         if target_year is not None and str(target_year).lower() != 'all':
#             try:
#                 target_year_int = int(target_year)
#             except ValueError:
#                 print(f"Error: target_year '{target_year}' cannot be converted to an integer. Cannot perform ranking.")
#                 # Still proceed with ratios, but ranking info will be missing
        
#         # Initialize results with existing ratio calculation
#         final_results = {}
#         calculator = None

#         # --- Determine calculator and specific labels ---
#         revenue_var_key = "REVENUE"
#         assets_var_key = "ASSETS"
        
#         # Initialize for type hinting or default clarity
#         revenue_display_label = "" 

#         if entity_type.lower() == "company":
#             calculator = CompanyFinancialRatiosCalculator(extracted_data, target_year)
#             revenue_display_label = "Sales"
#         elif entity_type.lower() == "bank":
#             calculator = BankFinancialRatiosCalculator(extracted_data, target_year)
#             revenue_display_label = "Revenue" # As per your requirement: "Revenue in 2023 N/A"
#         else:
#             print(f"Error: Invalid entity type: {entity_type}. Must be 'company' or 'bank'.")
#             return {}

#         calculator.calculate_ratios()
#         final_results.update(calculator.get_ratios()) # Add existing ratios

#         # --- Add Revenue and Assets with Structured Ranking (only if target_year is a specific year) ---
#         if target_year_int is not None:
#             # Fetch all organizations' revenue for ranking using the internal 'revenue_var_key'
#             all_orgs_revenue_data = financial_variables_service_instance.get_all_organizations_variable_for_year_by_sector(
#                 entity_type=entity_type,
#                 sector=sector,
#                 variable_key=revenue_var_key,
#                 target_year=target_year_int
#             )
            
#             # Fetch all organizations' assets for ranking using the internal 'assets_var_key'
#             all_orgs_assets_data = financial_variables_service_instance.get_all_organizations_variable_for_year_by_sector(
#                 entity_type=entity_type,
#                 sector=sector,
#                 variable_key=assets_var_key,
#                 target_year=target_year_int
#             )

#             # Get the specific organization's values for the target year
#             org_revenue_value = extracted_data.get(revenue_var_key, {}).get(target_year_int)
#             org_assets_value = extracted_data.get(assets_var_key, {}).get(target_year_int)
            
#             # Determine ranks and total count
#             revenue_rank, total_revenue_orgs = self._get_rank(org_name, org_revenue_value, all_orgs_revenue_data, higher_is_better=True)
#             assets_rank, total_assets_orgs = self._get_rank(org_name, org_assets_value, all_orgs_assets_data, higher_is_better=True) 

#             sector_display_name = f"{sector} Sector" if sector else "Industry"
            
#             # --- Revenue Details Structure ---
#             revenue_details = {
#                 "label": revenue_display_label,
#                 "year": target_year_int,
#                 "value": org_revenue_value if org_revenue_value is not None else "N/A",
#                 "unit": "Million" if org_revenue_value is not None else None,
#                 "currency": "Rs." if org_revenue_value is not None else None,
#                 "rank": revenue_rank,
#                 "total_in_sector": total_revenue_orgs,
#                 "sector": sector_display_name,
#                 "display_string": "" # This will be the formatted string for quick display
#             }
#             # Special case for banks: Revenue should always be "N/A"
#             if entity_type.lower() == "bank":
#                 revenue_details["value"] = "N/A"
#                 revenue_details["unit"] = None
#                 revenue_details["currency"] = None
#                 revenue_details["rank"] = None
#                 revenue_details["total_in_sector"] = None
#                 revenue_details["display_string"] = f"Revenue in {target_year_int} N/A"
#             else: # For companies, construct display string
#                 if org_revenue_value is not None and pd.notna(org_revenue_value):
#                     revenue_display_val = f"Rs. {org_revenue_value:,.3f} Million"
#                     if revenue_rank is not None and total_revenue_orgs is not None:
#                         revenue_details["display_string"] = f"{revenue_details['label']} in {target_year_int} {revenue_display_val} (ranked {revenue_rank} out of {total_revenue_orgs} in {sector_display_name})"
#                     elif revenue_rank is not None:
#                         revenue_details["display_string"] = f"{revenue_details['label']} in {target_year_int} {revenue_display_val} (ranked {revenue_rank} in {sector_display_name})"
#                     else:
#                         revenue_details["display_string"] = f"{revenue_details['label']} in {target_year_int} {revenue_display_val}"
#                 else:
#                     revenue_details["display_string"] = f"{revenue_details['label']} in {target_year_int} N/A"
#             final_results["RevenueDetails"] = revenue_details


#             # --- Assets Details Structure ---
#             assets_details = {
#                 "label": "Assets",
#                 "year": target_year_int,
#                 "value": org_assets_value if org_assets_value is not None else "N/A",
#                 "unit": "Million" if org_assets_value is not None else None,
#                 "currency": "Rs." if org_assets_value is not None else None,
#                 "rank": assets_rank,
#                 "total_in_sector": total_assets_orgs,
#                 "sector": sector_display_name,
#                 "display_string": "" # This will be the formatted string for quick display
#             }
#             if org_assets_value is not None and pd.notna(org_assets_value):
#                 assets_display_val = f"Rs. {org_assets_value:,.3f} Million"
#                 if assets_rank is not None and total_assets_orgs is not None:
#                     assets_details["display_string"] = f"Assets as of {target_year_int} {assets_display_val} (ranked {assets_rank} out of {total_assets_orgs} in {sector_display_name})"
#                 elif assets_rank is not None:
#                     assets_details["display_string"] = f"Assets as of {target_year_int} {assets_display_val} (ranked {assets_rank} in {sector_display_name})"
#                 else:
#                     assets_details["display_string"] = f"Assets as of {target_year_int} {assets_display_val}"
#             else:
#                 assets_details["display_string"] = f"Assets as of {target_year_int} N/A"
#             final_results["AssetsDetails"] = assets_details

#         return final_results

#     def calculate_financial_ratios_for_specific_sector(self, entity_type: str, sector: str, target_year: str = None) -> dict:
#         """
#         Calculates the average financial ratios for all organizations within a given sector
#         (including all sub-sectors).

#         Args:
#             entity_type (str): The type of entity ("company" or "bank").
#             sector (str): The sector for which to calculate average ratios.
#             target_year (str, optional): The year for which to calculate ratios.
#                                          If 'all', calculates for all available years. Defaults to None.

#         Returns:
#             dict: A dictionary containing the calculated average ratios, categorized by type.
#                   Returns an empty dictionary if no data is fetched or ratios cannot be calculated.
#         """
#         # Fetch aggregated variables for the sector using the FinancialVariablesService
#         sector_data = financial_variables_service_instance.get_specific_variables_by_sector(
#             entity_type=entity_type,
#             sector=sector,
#             target_year=target_year # Pass target_year to filter variables
#         )

#         if not sector_data: # Check if the dictionary is empty or None
#             print(f"No sector data found for {sector} for year {target_year}.")
#             return {}

#         calculator = None
#         if entity_type.lower() == "company":
#             calculator = CompanyFinancialRatiosCalculator(sector_data, target_year)
#         elif entity_type.lower() == "bank":
#             calculator = BankFinancialRatiosCalculator(sector_data, target_year)
#         else:
#             print(f"Error: Invalid entity type: {entity_type}. Must be 'company' or 'bank'.")
#             return {}

#         calculator.calculate_ratios()
#         return calculator.get_ratios()

# # Instantiate the service for use in views
# financial_ratios_service_instance = FinancialRatiosService()






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
                    # print(f"Error calculating ratio for year {y}: {e}") # Suppress for cleaner output unless debugging
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
                # print(f"Error calculating ratio for year {year_input}: {e}") # Suppress for cleaner output unless debugging
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
    def _get_rank(self, org_name: str, org_value: float, all_orgs_values: list[tuple[str, float]], higher_is_better: bool = True) -> tuple[int | None, int | None]:
        """
        Calculates the rank of an organization's value within a list of all organizations' values.

        Args:
            org_name (str): The name of the organization to rank.
            org_value (float): The value of the specific organization.
            all_orgs_values (list[tuple[str, float]]): List of (organization_name, value) tuples for the sector.
            higher_is_better (bool): True if higher values mean better rank (e.g., Revenue),
                                     False if lower values mean better rank (e.g., NPLs).

        Returns:
            tuple[int | None, int | None]: A tuple containing (rank, total_organizations).
                                         Returns (None, None) if the organization's value is None,
                                         not found, or no valid data to rank against.
        """
        if org_value is None or pd.isna(org_value):
            return None, None

        # Create a Series for ranking from valid organization data
        valid_orgs_data = {name: val for name, val in all_orgs_values if val is not None and pd.notna(val)}
        
        # Get the total count of valid organizations *before* ranking
        total_valid_orgs = len(valid_orgs_data)

        if not valid_orgs_data:
            return None, None # No valid data to rank against

        temp_series = pd.Series(valid_orgs_data)

        # Rank the series. 'dense' method gives consecutive ranks without gaps.
        # `ascending=False` for higher_is_better (e.g., Revenue: 1st is highest)
        # `ascending=True` for lower_is_better (e.g., NPLs: 1st is lowest)
        ranked_series = temp_series.rank(method='dense', ascending=not higher_is_better)

        # Get the rank of the specific organization
        rank = ranked_series.get(org_name)

        if pd.notna(rank):
            return int(rank), total_valid_orgs
        return None, None


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
            dict: A dictionary containing the calculated ratios, categorized by type,
                  plus Revenue and Assets details with structured ranking for the specified year(s).
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

        # Determine the years to process
        years_to_process = []
        if target_year is None or str(target_year).lower() == 'all':
            # Collect all unique years from any variable in extracted_data
            for var_key, year_data in extracted_data.items():
                if isinstance(year_data, dict):
                    years_to_process.extend(year_data.keys())
            years_to_process = sorted(list(set(years_to_process)))
        else:
            try:
                specific_year_int = int(target_year)
                years_to_process = [specific_year_int]
            except ValueError:
                print(f"Error: target_year '{target_year}' cannot be converted to an integer. Cannot perform ranking.")
                return {} # Return empty if target_year is invalid and not 'all'

        # Initialize results with existing ratio calculation
        final_results = {}
        calculator = None

        # --- Determine calculator and specific labels ---
        revenue_var_key = "REVENUE"
        assets_var_key = "ASSETS"
        
        revenue_display_label = "" 

        if entity_type.lower() == "company":
            calculator = CompanyFinancialRatiosCalculator(extracted_data, target_year)
            revenue_display_label = "Sales"
        elif entity_type.lower() == "bank":
            calculator = BankFinancialRatiosCalculator(extracted_data, target_year)
            revenue_display_label = "Revenue"
        else:
            print(f"Error: Invalid entity type: {entity_type}. Must be 'company' or 'bank'.")
            return {}

        calculator.calculate_ratios()
        final_results.update(calculator.get_ratios()) # Add existing ratios

        # --- Add Revenue and Assets with Structured Ranking for each relevant year ---
        final_results["RevenueDetails"] = {}
        final_results["AssetsDetails"] = {}
        sector_display_name = f"{sector} Sector" if sector else "Industry"

        for current_year in years_to_process:
            # Fetch all organizations' revenue for ranking using the internal 'revenue_var_key'
            all_orgs_revenue_data = financial_variables_service_instance.get_all_organizations_variable_for_year_by_sector(
                entity_type=entity_type,
                sector=sector,
                variable_key=revenue_var_key,
                target_year=current_year
            )
            
            # Fetch all organizations' assets for ranking using the internal 'assets_var_key'
            all_orgs_assets_data = financial_variables_service_instance.get_all_organizations_variable_for_year_by_sector(
                entity_type=entity_type,
                sector=sector,
                variable_key=assets_var_key,
                target_year=current_year
            )

            # Get the specific organization's values for the current year
            # Ensure we're getting it from extracted_data, which may contain only one year or all.
            org_revenue_value = extracted_data.get(revenue_var_key, {}).get(current_year)
            org_assets_value = extracted_data.get(assets_var_key, {}).get(current_year)
            
            # Determine ranks and total count
            revenue_rank, total_revenue_orgs = self._get_rank(org_name, org_revenue_value, all_orgs_revenue_data, higher_is_better=True)
            assets_rank, total_assets_orgs = self._get_rank(org_name, org_assets_value, all_orgs_assets_data, higher_is_better=True) 
            
            # --- Revenue Details Structure for the current_year ---
            revenue_details_year = {
                "label": revenue_display_label,
                "year": current_year,
                "value": org_revenue_value if org_revenue_value is not None else "N/A",
                "unit": "Million" if org_revenue_value is not None else None,
                "currency": "Rs." if org_revenue_value is not None else None,
                "rank": revenue_rank,
                "total_in_sector": total_revenue_orgs,
                "sector": sector_display_name,
                "display_string": "" # This will be the formatted string for quick display
            }
            # Special case for banks: Revenue should always be "N/A"
            if entity_type.lower() == "bank":
                revenue_details_year["value"] = "N/A"
                revenue_details_year["unit"] = None
                revenue_details_year["currency"] = None
                revenue_details_year["rank"] = None
                revenue_details_year["total_in_sector"] = None
                revenue_details_year["display_string"] = f"Revenue in {current_year} N/A"
            else: # For companies, construct display string
                if org_revenue_value is not None and pd.notna(org_revenue_value):
                    revenue_display_val = f"Rs. {org_revenue_value:,.3f} Million"
                    if revenue_rank is not None and total_revenue_orgs is not None:
                        revenue_details_year["display_string"] = f"{revenue_details_year['label']} in {current_year} {revenue_display_val} (ranked {revenue_rank} out of {total_revenue_orgs} in {sector_display_name})"
                    elif revenue_rank is not None:
                        revenue_details_year["display_string"] = f"{revenue_details_year['label']} in {current_year} {revenue_display_val} (ranked {revenue_rank} in {sector_display_name})"
                    else:
                        revenue_details_year["display_string"] = f"{revenue_details_year['label']} in {current_year} {revenue_display_val}"
                else:
                    revenue_details_year["display_string"] = f"{revenue_details_year['label']} in {current_year} N/A"
            
            final_results["RevenueDetails"][current_year] = revenue_details_year


            # --- Assets Details Structure for the current_year ---
            assets_details_year = {
                "label": "Assets",
                "year": current_year,
                "value": org_assets_value if org_assets_value is not None else "N/A",
                "unit": "Million" if org_assets_value is not None else None,
                "currency": "Rs." if org_assets_value is not None else None,
                "rank": assets_rank,
                "total_in_sector": total_assets_orgs,
                "sector": sector_display_name,
                "display_string": "" # This will be the formatted string for quick display
            }
            if org_assets_value is not None and pd.notna(org_assets_value):
                assets_display_val = f"Rs. {org_assets_value:,.3f} Million"
                if assets_rank is not None and total_assets_orgs is not None:
                    assets_details_year["display_string"] = f"Assets as of {current_year} {assets_display_val} (ranked {assets_rank} out of {total_assets_orgs} in {sector_display_name})"
                elif assets_rank is not None:
                    assets_details_year["display_string"] = f"Assets as of {current_year} {assets_display_val} (ranked {assets_rank} in {sector_display_name})"
                else:
                    assets_details_year["display_string"] = f"Assets as of {current_year} {assets_display_val}"
            else:
                assets_details_year["display_string"] = f"Assets as of {current_year} N/A"
            
            final_results["AssetsDetails"][current_year] = assets_details_year

        return final_results

    def calculate_financial_ratios_for_specific_sector(self, entity_type: str, sector: str, target_year: str = None) -> dict:
        """
        Calculates the average financial ratios for all organizations within a given sector
        (including all sub-sectors).

        Args:
            entity_type (str): The type of entity ("company" or "bank").
            sector (str): The sector for which to calculate average ratios.
            target_year (str, optional): The year to retrieve data for. Can be a year (e.g., "2023")
                                         or "all" for all available years. Defaults to None (all years).

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