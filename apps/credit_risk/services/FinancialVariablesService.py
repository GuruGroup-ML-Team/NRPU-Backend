# # project_root/credit_risk/services/logic_two_service.py

# import pandas as pd
# # Import the instance of OrganizationDataService to fetch base data
# from credit_risk.services.OrganizationDataService import organization_data_service_instance

# class FinancialVariablesService:
#     """
#     Service responsible for extracting specific financial variables for individual
#     organizations or calculating averages for entire sectors.
#     """

#     # --- Module-level Variable Mappings (DRY Principle) ---
#     # These mappings define the user-friendly variable names and their corresponding
#     # search terms found in the 'Indicator', 'Sub Indicator', or 'Sub-Sub Indicator' columns
#     # of the Excel data.
#     BANK_VARIABLES_MAP = {
#         # PROFITABILITY AND EFFICIENCY
#         "SPREAD_RATIO": "1. Spread Ratio (D3/D1)",
#         "NET_INTEREST_MARGIN": "2. Net markup/interest margin (D1-D2)/C",
#         "RETURN_ON_EQUITY": "3. Return on equity (ROE) (D10/A)",
#         "RETURN_ON_ASSETS": "4. Return on assets (ROA) (D10/C)",
#         "NON_INTEREST_INCOME_RATIO": "5. Non-markup/interest income to total assets (D6/C)",
        
#         # LIQUIDITY 
#         "CASH_TO_TOTAL_ASSETS_RATIO": "1. Cash & cash equivalent to total assets (C1+C2)/C",
#         "INVESTMENT_TO_TOTAL_ASSETS": "2. Investment to total assets (C4/C)",
#         "ADVANCES_TO_TOTAL_ASSETS": "3. Advances net of provisions to total assets (C8/C)",
#         "DEPOSIT_TO_TOTAL_ASSETS": "4. Deposits to total assets (B3/C)",
#         "TOTAL_LIABILITIES_TO_TOTAL_ASSETS": "5. Total liabilities to total assets (B/C)",
#         "GROSS_ADVANCES_TO_DEPOSITS": "6. Gross advances to deposits (C5/B3)",
#         "GROSS_ADVANCES_TO_BORROWING_AND_DEPOSIT": "7. Gross advances to borrowing & deposits C5/(B2+B3)",

#         # ASSETS QUALITY RATIOS
#         "NON_PERFORMING_LOANS_TO_GROSS_ADVANCES": "1. Non-performing loans to gross advances (C6/C5)",
#         "PROVISION_AGAINST_NPLS_TO_GROSS_ADVANCES": "2. Provisions against NPLs to gross advances (C7/C5)",
#         "NPL_TO_TOTAL_EQUITY": "3. NPLs to total equity (C6/A)",
        
#         # LEVERAGE RATIOS 
#         "CAPITAL_RATIO": "1. Capital ratio (A/C)",
#         "TOTAL_DEPOSIT_TO_EQUITY_RATIO": "3. Total deposit to total equity (B3/A) (times)",
#     }

#     COMPANY_VARIABLES_MAP = {
#         # "NET_PROFIT_MARGIN": "P1. Net Profit margin / Net profit to sales (F10 as % of F1)",  # 
#         "NET_PROFIT_MARGIN": "         P1. Net Profit  margin / Net profit to sales (F10 as % of F1)",
#         # "RETURN_ON_ASSETS": "P3. Return on Assets (F10 as a % of Avg {Current year(A+B),previous year (A+B)}", # 
#         "RETURN_ON_ASSETS": "         P3. Return on Assets  (F10 as a % of Avg {Current year(A+B),previous year (A+B)}", # 

#         "RETURN_ON_EQUITY": "P5. Return on equity (F10 as % of Avg {Current year(C),previous year (C)}",
#         # "GROSS_PROFIT_MARGIN": "P6. Gross profit margin / Gross profit to sales (F3 as % of F1)", # 
#         "GROSS_PROFIT_MARGIN": "         P6. Gross profit  margin / Gross profit to sales (F3 as % of F1)",
#         "OPERATING_RETURN_ON_ASSETS": "P7. Operating return on assets (F6 as a % of Avg. {Current year(A+B),previous year (A+B)}",
#         "RETURN_ON_CAPITAL_EMPLOYED": "P8. Return on capital employed(F7 as a % of Avg {Current year H1, previous year H1}",

#         "CURRENT_RATIO":"L1. Current ratio (B to E)",
#         "QUICK_RATIO": "L2. Quick ratio (B1+B3+B5 to E)",
#         "CASH_TO_CURRENT_LIABILITIES_RATIO": "L3. Cash to current liabilities (B1+B5 to E)",

#         "NUM_OF_DAYS_IN_INVENTORY": "AC2. No. of days in inventory ",
#         "NUM_OF_DAYS_IN_RECEIVABLES": "AC4. No. of days in receivables (365 to AC3)",
#         # "NUM_OF_DAYS_IN_PAYABLE": "AC6. No. of days in payable (365 to AC5)", # 
#         "NUM_OF_DAYS_IN_PAYABLE": "         AC6. No. of days in payable  (365 to AC5)", # 
#         "WORKING_CAPITAL_TURNOVER": "AC7. Working capital turnover (F1 to B-E)",
#         "CASH_CONVERSION_CYCLE": "AC8. Cash conversion cycle (AC2+AC4-AC6)",

#         "DEBT_EQUITY_RATIO": "S1. Debt equity ratio [(D+E) to C]",
#         # "DEBT_TO_ASSETS_RATIO": "S2. Debt to assets ratio ( D+E as % of Avg. {Current year(A+B),previous year (A+B)})", # 
#         "DEBT_TO_ASSETS_RATIO": "         S2. Debt to assets ratio (  D+E as % of Avg. {Current year(A+B),previous year (A+B)})",
#         "DEBT_TO_CAPITAL_RATIO": "S3. Debt to capital ratio (D+E to H1)",
#         "INTEREST_COVER_RATIO": "S4. Interest cover ratio ( F6 to F7(i))",
#     }
#     # --------------------------------------------------------

#     def get_specific_variables_for_specific_org(self, entity_type: str, sector: str = None, sub_sector: str = None, org_name: str = None, target_year: str = None) -> dict:
#         """
#         Extracts specific financial variables for a particular organization
#         based on entity type, sector, sub-sector, and organization name.
#         It can return data for a specific year or all available years.

#         Args:
#             entity_type (str): The type of entity to load data for ('company' or 'bank').
#             sector (str, optional): The sector to filter by. Defaults to None.
#             sub_sector (str, optional): The sub-sector to filter by. Defaults to None.
#             org_name (str, optional): The organization name to filter by. Defaults to None.
#             target_year (str, optional): The year to retrieve data for. Can be a year (e.g., "2023")
#                                          or "all" for all available years. Defaults to None (all years).

#         Returns:
#             dict: A dictionary containing the extracted variables and their values.
#                   Returns an empty dictionary if no data or variables are found.
#         """
#         # Use the existing OrganizationDataService to fetch the filtered DataFrame
#         df = organization_data_service_instance.fetch_data_for_specific_org(
#             entity_type=entity_type,
#             sector=sector,
#             sub_sector=sub_sector,
#             org_name=org_name,
#         )

#         if df is None or df.empty:
#             print("Error: No data fetched for the specified organization.")
#             return {}

#         # Determine which variable map to use based on entity type
#         variables_to_map = self.BANK_VARIABLES_MAP if entity_type.lower() == "bank" else self.COMPANY_VARIABLES_MAP

#         extracted_data = {}
#         # Identify columns that represent years (assuming they are integers)
#         year_columns = [col for col in df.columns if isinstance(col, int)]

#         # Convert target_year to int if it's a string and not 'all'
#         target_year_int = None
#         if target_year is not None and target_year.lower() != 'all':
#             try:
#                 target_year_int = int(target_year)
#             except ValueError:
#                 print(f"Error: target_year '{target_year}' cannot be converted to an integer. Returning empty data.")
#                 return {}

#         # Iterate through each defined variable to find its value in the DataFrame
#         for var_name, search_term in variables_to_map.items():
#             found_data_for_var = False
#             # Iterate through rows to find the indicator/sub-indicator
#             for _, row in df.iterrows():
#                 # Check if the search term exists in 'Indicator', 'Sub Indicator', or 'Sub-Sub Indicator'
#                 # .strip() is used to remove leading/trailing whitespace for accurate matching
#                 # str() conversion handles potential non-string types in these columns
#                 if (search_term.strip() in str(row.get('Indicator', '')).strip() or
#                     search_term.strip() in str(row.get('Sub Indicator', '')).strip() or
#                     search_term.strip() in str(row.get('Sub-Sub Indicator', '')).strip()):
                    
#                     found_data_for_var = True
#                     yearly_data_full = {}
#                     # Collect data for all identified year columns
#                     for year in year_columns:
#                         if year in row:
#                             yearly_data_full[year] = row[year]

#                     if target_year_int is not None:  # A specific year (integer) is requested
#                         # Get the value for the specific year, default to None if not found
#                         extracted_data[var_name] = {target_year_int: yearly_data_full.get(target_year_int, None)}
#                     else:  # 'all' or None (meaning all years)
#                         extracted_data[var_name] = yearly_data_full
#                     break  # Break out of the inner loop once the variable is found for this org

#             if not found_data_for_var:
#                 # If the variable was not found in any row for the given organization,
#                 # initialize with None for the target year or all years.
#                 if target_year_int is not None:
#                     extracted_data[var_name] = {target_year_int: None}
#                 else:
#                     extracted_data[var_name] = {year: None for year in year_columns}
#                 # If there are no year columns, ensure it's None directly
#                 if not extracted_data[var_name]:
#                     extracted_data[var_name] = None

#         return extracted_data

#     def get_specific_variables_by_sector(self, entity_type: str, sector: str, target_year: str = None) -> dict:
#         """
#         Calculates the average of specific financial variables for all
#         organizations within a given sector (including all sub-sectors).
#         It can return averages for a specific year or all available years.

#         Args:
#             entity_type (str): The type of entity to load data for ('company' or 'bank').
#             sector (str): The sector to filter by.
#             target_year (str, optional): The year to retrieve data for. Can be a year (e.g., "2023")
#                                          or "all" for all available years. Defaults to None (all years).

#         Returns:
#             dict: A dictionary containing the aggregated (averaged) variables and their values.
#                   Returns an empty dictionary if no data or variables are found for the sector.
#         """
#         # Use the existing OrganizationDataService to fetch the sector-filtered DataFrame
#         df_sector = organization_data_service_instance.fetch_data_by_sector(entity_type=entity_type, sector=sector)

#         if df_sector is None or df_sector.empty:
#             print(f"Error: No data fetched for the sector: {sector}.")
#             return {}

#         # Determine which variable map to use based on entity type
#         variables_to_map = self.BANK_VARIABLES_MAP if entity_type.lower() == "bank" else self.COMPANY_VARIABLES_MAP

#         aggregated_data = {}
#         # Identify columns that represent years (assuming they are integers)
#         year_columns = [col for col in df_sector.columns if isinstance(col, int)]

#         # Convert target_year to int if it's a string and not 'all'
#         target_year_int = None
#         if target_year is not None and target_year.lower() != 'all':
#             try:
#                 target_year_int = int(target_year)
#             except ValueError:
#                 print(f"Error: target_year '{target_year}' cannot be converted to an integer. Returning empty data.")
#                 return {}

#         # Iterate through each defined variable to calculate its average across the sector
#         for var_name, search_term in variables_to_map.items():
#             # Filter rows that contain the search term in 'Indicator', 'Sub Indicator', or 'Sub-Sub Indicator'
#             # `astype(str)` and `.str.strip()` ensure robust string comparison.
#             # `na=False` handles NaN values in these columns gracefully.
#             matching_rows = df_sector[
#                 df_sector['Indicator'].astype(str).str.strip().str.contains(search_term.strip(), case=False, na=False, regex=False) |
#                 df_sector['Sub Indicator'].astype(str).str.strip().str.contains(search_term.strip(), case=False, na=False, regex=False) |
#                 df_sector['Sub-Sub Indicator'].astype(str).str.strip().str.contains(search_term.strip(), case=False, na=False, regex=False)
#             ]

#             if not matching_rows.empty:
#                 if target_year_int is not None:
#                     # Calculate average for a specific year
#                     # `pd.to_numeric` with `errors='coerce'` converts non-numeric values to NaN
#                     values = pd.to_numeric(matching_rows[target_year_int], errors='coerce')
#                     valid_values = values.dropna()  # Drop NaN values before calculating mean
#                     avg_value = valid_values.mean() if not valid_values.empty else None
#                     aggregated_data[var_name] = {target_year_int: avg_value}
#                 else:
#                     # Calculate average for all available years
#                     yearly_averages = {}
#                     for year in year_columns:
#                         values = pd.to_numeric(matching_rows[year], errors='coerce')
#                         valid_values = values.dropna()
#                         yearly_averages[year] = valid_values.mean() if not valid_values.empty else None
#                     aggregated_data[var_name] = yearly_averages
#             else:
#                 # If no matching rows for the variable, set to None or empty dict based on target_year
#                 if target_year_int is not None:
#                     aggregated_data[var_name] = {target_year_int: None}
#                 else:
#                     aggregated_data[var_name] = {year: None for year in year_columns}
#                 if not aggregated_data[var_name]: # If no year columns found, ensure it's None directly
#                     aggregated_data[var_name] = None
#         return aggregated_data

# # Instantiate the service for use in views
# financial_variables_service_instance = FinancialVariablesService()








# # project_root/credit_risk/services/logic_two_service.py

# import pandas as pd
# # from credit_risk.services.OrganizationDataService import organization_data_service_instance
# from .OrganizationDataService import organization_data_service_instance

# class FinancialVariablesService:
#     """
#     Service responsible for extracting specific financial variables for individual
#     organizations or calculating averages for entire sectors.
#     """

#     # --- Module-level Variable Mappings (DRY Principle) ---
#     # These mappings define the user-friendly variable names and their corresponding
#     # search terms found in the 'Indicator', 'Sub Indicator', or 'Sub-Sub Indicator' columns
#     # of the Excel data.
#     BANK_VARIABLES_MAP = {
#         # PROFITABILITY AND EFFICIENCY
#         "SPREAD_RATIO": "1. Spread Ratio (D3/D1)",
#         "NET_INTEREST_MARGIN": "2. Net markup/interest margin (D1-D2)/C",
#         "RETURN_ON_EQUITY": "3. Return on equity (ROE) (D10/A)",
#         "RETURN_ON_ASSETS": "4. Return on assets (ROA) (D10/C)",
#         "NON_INTEREST_INCOME_RATIO": "5. Non-markup/interest income to total assets (D6/C)",
        
#         # LIQUIDITY 
#         "CASH_TO_TOTAL_ASSETS_RATIO": "1. Cash & cash equivalent to total assets (C1+C2)/C",
#         "INVESTMENT_TO_TOTAL_ASSETS": "2. Investment to total assets (C4/C)",
#         "ADVANCES_TO_TOTAL_ASSETS": "3. Advances net of provisions to total assets (C8/C)",
#         "DEPOSIT_TO_TOTAL_ASSETS": "4. Deposits to total assets (B3/C)",
#         "TOTAL_LIABILITIES_TO_TOTAL_ASSETS": "5. Total liabilities to total assets (B/C)",
#         "GROSS_ADVANCES_TO_DEPOSITS": "6. Gross advances to deposits (C5/B3)",
#         "GROSS_ADVANCES_TO_BORROWING_AND_DEPOSIT": "7. Gross advances to borrowing & deposits C5/(B2+B3)",

#         # ASSETS QUALITY RATIOS
#         "NON_PERFORMING_LOANS_TO_GROSS_ADVANCES": "1. Non-performing loans to gross advances (C6/C5)",
#         "PROVISION_AGAINST_NPLS_TO_GROSS_ADVANCES": "2. Provisions against NPLs to gross advances (C7/C5)",
#         "NPL_TO_TOTAL_EQUITY": "3. NPLs to total equity (C6/A)",
        
#         # LEVERAGE RATIOS 
#         "CAPITAL_RATIO": "1. Capital ratio (A/C)",
#         # MODIFIED: Allow for either '3.' or '4.' prefix
#         "TOTAL_DEPOSIT_TO_EQUITY_RATIO": [
#             "3. Total deposit to total equity (B3/A) (times)",
#             "4. Total deposit to total equity (B3/A) (times)"
#         ],
#     }

#     COMPANY_VARIABLES_MAP = {
#         "NET_PROFIT_MARGIN": "        P1. Net Profit  margin / Net profit to sales (F10 as % of F1)",
#         "RETURN_ON_ASSETS": "        P3. Return on Assets  (F10 as a % of Avg {Current year(A+B),previous year (A+B)}",
#         "RETURN_ON_EQUITY": "P5. Return on equity (F10 as % of Avg {Current year(C),previous year (C)}",
#         "GROSS_PROFIT_MARGIN": "        P6. Gross profit  margin / Gross profit to sales (F3 as % of F1)",
#         "OPERATING_RETURN_ON_ASSETS": "P7. Operating return on assets (F6 as a % of Avg. {Current year(A+B),previous year (A+B)}",
#         "RETURN_ON_CAPITAL_EMPLOYED": "P8. Return on capital employed(F7 as a % of Avg {Current year H1, previous year H1}",

#         "CURRENT_RATIO":"L1. Current ratio (B to E)",
#         "QUICK_RATIO": "L2. Quick ratio (B1+B3+B5 to E)",
#         "CASH_TO_CURRENT_LIABILITIES_RATIO": "L3. Cash to current liabilities (B1+B5 to E)",

#         "NUM_OF_DAYS_IN_INVENTORY": "AC2. No. of days in inventory ",
#         "NUM_OF_DAYS_IN_RECEIVABLES": "AC4. No. of days in receivables (365 to AC3)",
#         "NUM_OF_DAYS_IN_PAYABLE": "        AC6. No. of days in payable  (365 to AC5)",
#         "WORKING_CAPITAL_TURNOVER": "AC7. Working capital turnover (F1 to B-E)",
#         "CASH_CONVERSION_CYCLE": "AC8. Cash conversion cycle (AC2+AC4-AC6)",

#         "DEBT_EQUITY_RATIO": "S1. Debt equity ratio [(D+E) to C]",
#         "DEBT_TO_ASSETS_RATIO": "        S2. Debt to assets ratio (  D+E as % of Avg. {Current year(A+B),previous year (A+B)})",
#         "DEBT_TO_CAPITAL_RATIO": "S3. Debt to capital ratio (D+E to H1)",
#         "INTEREST_COVER_RATIO": "S4. Interest cover ratio ( F6 to F7(i))",
#     }
#     # --------------------------------------------------------

#     def get_specific_variables_for_specific_org(self, entity_type: str, sector: str = None, sub_sector: str = None, org_name: str = None, target_year: str = None) -> dict:
#         """
#         Extracts specific financial variables for a particular organization
#         based on entity type, sector, sub-sector, and organization name.
#         It can return data for a specific year or all available years.

#         Args:
#             entity_type (str): The type of entity to load data for ('company' or 'bank').
#             sector (str, optional): The sector to filter by. Defaults to None.
#             sub_sector (str, optional): The sub-sector to filter by. Defaults to None.
#             org_name (str, optional): The organization name to filter by. Defaults to None.
#             target_year (str, optional): The year to retrieve data for. Can be a year (e.g., "2023")
#                                          or "all" for all available years. Defaults to None (all years).

#         Returns:
#             dict: A dictionary containing the extracted variables and their values.
#                   Returns an empty dictionary if no data or variables are found.
#         """
#         df = organization_data_service_instance.fetch_data_for_specific_org(
#             entity_type=entity_type,
#             sector=sector,
#             sub_sector=sub_sector,
#             org_name=org_name,
#         )

#         if df is None or df.empty:
#             print("Error: No data fetched for the specified organization.")
#             return {}

#         variables_to_map = self.BANK_VARIABLES_MAP if entity_type.lower() == "bank" else self.COMPANY_VARIABLES_MAP

#         extracted_data = {}
#         year_columns = [col for col in df.columns if isinstance(col, int)]

#         target_year_int = None
#         if target_year is not None and target_year.lower() != 'all':
#             try:
#                 target_year_int = int(target_year)
#             except ValueError:
#                 print(f"Error: target_year '{target_year}' cannot be converted to an integer. Returning empty data.")
#                 return {}

#         for var_name, search_term_or_list in variables_to_map.items():
#             found_data_for_var = False
#             # Normalize search_term_or_list into a list of strings
#             search_terms = [search_term_or_list] if isinstance(search_term_or_list, str) else search_term_or_list

#             for _, row in df.iterrows():
#                 # Check each search term in the list against the indicator columns
#                 for term in search_terms:
#                     if (term.strip() in str(row.get('Indicator', '')).strip() or
#                         term.strip() in str(row.get('Sub Indicator', '')).strip() or
#                         term.strip() in str(row.get('Sub-Sub Indicator', '')).strip()):
                        
#                         found_data_for_var = True
#                         yearly_data_full = {}
#                         for year in year_columns:
#                             if year in row:
#                                 yearly_data_full[year] = row[year]

#                         if target_year_int is not None:
#                             extracted_data[var_name] = {target_year_int: yearly_data_full.get(target_year_int, None)}
#                         else:
#                             extracted_data[var_name] = yearly_data_full
#                         break # Break from inner 'for term in search_terms' loop once found
#                 if found_data_for_var:
#                     break # Break from outer 'for _, row in df.iterrows()' loop once found for this var

#             if not found_data_for_var:
#                 if target_year_int is not None:
#                     extracted_data[var_name] = {target_year_int: None}
#                 else:
#                     extracted_data[var_name] = {year: None for year in year_columns}
#                 if not extracted_data[var_name]:
#                     extracted_data[var_name] = None

#         return extracted_data

#     def get_specific_variables_by_sector(self, entity_type: str, sector: str, target_year: str = None) -> dict:
#         """
#         Calculates the average of specific financial variables for all
#         organizations within a given sector (including all sub-sectors).
#         It can return averages for a specific year or all available years.

#         Args:
#             entity_type (str): The type of entity to load data for ('company' or 'bank').
#             sector (str): The sector to filter by.
#             target_year (str, optional): The year to retrieve data for. Can be a year (e.g., "2023")
#                                          or "all" for all available years. Defaults to None (all years).

#         Returns:
#             dict: A dictionary containing the aggregated (averaged) variables and their values.
#                   Returns an empty dictionary if no data or variables are found for the sector.
#         """
#         df_sector = organization_data_service_instance.fetch_data_by_sector(entity_type=entity_type, sector=sector)

#         if df_sector is None or df_sector.empty:
#             print(f"Error: No data fetched for the sector: {sector}.")
#             return {}

#         variables_to_map = self.BANK_VARIABLES_MAP if entity_type.lower() == "bank" else self.COMPANY_VARIABLES_MAP

#         aggregated_data = {}
#         year_columns = [col for col in df_sector.columns if isinstance(col, int)]

#         target_year_int = None
#         if target_year is not None and target_year.lower() != 'all':
#             try:
#                 target_year_int = int(target_year)
#             except ValueError:
#                 print(f"Error: target_year '{target_year}' cannot be converted to an integer. Returning empty data.")
#                 return {}

#         for var_name, search_term_or_list in variables_to_map.items():
#             # Normalize search_term_or_list into a list of strings
#             search_terms = [search_term_or_list] if isinstance(search_term_or_list, str) else search_term_or_list

#             # Build a combined boolean condition for matching rows
#             combined_condition = pd.Series([False] * len(df_sector)) # Initialize with all False
#             for term in search_terms:
#                 term_strip = term.strip()
#                 condition_for_term = (
#                     df_sector['Indicator'].astype(str).str.strip().str.contains(term_strip, case=False, na=False, regex=False) |
#                     df_sector['Sub Indicator'].astype(str).str.strip().str.contains(term_strip, case=False, na=False, regex=False) |
#                     df_sector['Sub-Sub Indicator'].astype(str).str.strip().str.contains(term_strip, case=False, na=False, regex=False)
#                 )
#                 combined_condition = combined_condition | condition_for_term # OR conditions for each term

#             matching_rows = df_sector[combined_condition]

#             if not matching_rows.empty:
#                 if target_year_int is not None:
#                     values = pd.to_numeric(matching_rows[target_year_int], errors='coerce')
#                     valid_values = values.dropna()
#                     avg_value = valid_values.mean() if not valid_values.empty else None
#                     aggregated_data[var_name] = {target_year_int: avg_value}
#                 else:
#                     yearly_averages = {}
#                     for year in year_columns:
#                         values = pd.to_numeric(matching_rows[year], errors='coerce')
#                         valid_values = values.dropna()
#                         yearly_averages[year] = valid_values.mean() if not valid_values.empty else None
#                     aggregated_data[var_name] = yearly_averages
#             else:
#                 if target_year_int is not None:
#                     aggregated_data[var_name] = {target_year_int: None}
#                 else:
#                     aggregated_data[var_name] = {year: None for year in year_columns}
#                 if not aggregated_data[var_name]:
#                     aggregated_data[var_name] = None
#         return aggregated_data

# # Instantiate the service for use in views
# financial_variables_service_instance = FinancialVariablesService()




# import pandas as pd
# # from credit_risk.services.OrganizationDataService import organization_data_service_instance
# from .OrganizationDataService import organization_data_service_instance

# class FinancialVariablesService:
#     """
#     Service responsible for extracting specific financial variables for individual
#     organizations or calculating averages for entire sectors.
#     """

#     # --- Module-level Variable Mappings (DRY Principle) ---
#     # These mappings define the user-friendly variable names and their corresponding
#     # search terms found in the 'Indicator', 'Sub Indicator', or 'Sub-Sub Indicator' columns
#     # of the Excel data.
#     BANK_VARIABLES_MAP = {
#         # PROFITABILITY AND EFFICIENCY
#         "SPREAD_RATIO": "1. Spread Ratio (D3/D1)",
#         "NET_INTEREST_MARGIN": "2. Net markup/interest margin (D1-D2)/C",
#         "RETURN_ON_EQUITY": "3. Return on equity (ROE) (D10/A)",
#         "RETURN_ON_ASSETS": "4. Return on assets (ROA) (D10/C)",
#         "NON_INTEREST_INCOME_RATIO": "5. Non-markup/interest income to total assets (D6/C)",
        
#         # LIQUIDITY 
#         "CASH_TO_TOTAL_ASSETS_RATIO": "1. Cash & cash equivalent to total assets (C1+C2)/C",
#         "INVESTMENT_TO_TOTAL_ASSETS": "2. Investment to total assets (C4/C)",
#         "ADVANCES_TO_TOTAL_ASSETS": "3. Advances net of provisions to total assets (C8/C)",
#         "DEPOSIT_TO_TOTAL_ASSETS": "4. Deposits to total assets (B3/C)",
#         "TOTAL_LIABILITIES_TO_TOTAL_ASSETS": "5. Total liabilities to total assets (B/C)",
#         "GROSS_ADVANCES_TO_DEPOSITS": "6. Gross advances to deposits (C5/B3)",
#         "GROSS_ADVANCES_TO_BORROWING_AND_DEPOSIT": "7. Gross advances to borrowing & deposits C5/(B2+B3)",

#         # ASSETS QUALITY RATIOS
#         "NON_PERFORMING_LOANS_TO_GROSS_ADVANCES": "1. Non-performing loans to gross advances (C6/C5)",
#         "PROVISION_AGAINST_NPLS_TO_GROSS_ADVANCES": "2. Provisions against NPLs to gross advances (C7/C5)",
#         "NPL_TO_TOTAL_EQUITY": "3. NPLs to total equity (C6/A)",
        
#         # LEVERAGE RATIOS 
#         "CAPITAL_RATIO": "1. Capital ratio (A/C)",
#         # MODIFIED: Allow for either '3.' or '4.' prefix
#         "TOTAL_DEPOSIT_TO_EQUITY_RATIO": [
#             "3. Total deposit to total equity (B3/A) (times)",
#             "4. Total deposit to total equity (B3/A) (times)"
#         ],
#     }

#     COMPANY_VARIABLES_MAP = {
#         "NET_PROFIT_MARGIN": "         P1. Net Profit  margin / Net profit to sales (F10 as % of F1)",
#         "RETURN_ON_ASSETS": "         P3. Return on Assets  (F10 as a % of Avg {Current year(A+B),previous year (A+B)}",
#         "RETURN_ON_EQUITY": "P5. Return on equity (F10 as % of Avg {Current year(C),previous year (C)}",
#         "GROSS_PROFIT_MARGIN": "         P6. Gross profit  margin / Gross profit to sales (F3 as % of F1)",
#         "OPERATING_RETURN_ON_ASSETS": "P7. Operating return on assets (F6 as a % of Avg. {Current year(A+B),previous year (A+B)}",
#         "RETURN_ON_CAPITAL_EMPLOYED": "P8. Return on capital employed(F7 as a % of Avg {Current year H1, previous year H1}",

#         "CURRENT_RATIO":"L1. Current ratio (B to E)",
#         "QUICK_RATIO": "L2. Quick ratio (B1+B3+B5 to E)",
#         "CASH_TO_CURRENT_LIABILITIES_RATIO": "L3. Cash to current liabilities (B1+B5 to E)",

#         "NUM_OF_DAYS_IN_INVENTORY": "AC2. No. of days in inventory ",
#         "NUM_OF_DAYS_IN_RECEIVABLES": "AC4. No. of days in receivables (365 to AC3)",
#         "NUM_OF_DAYS_IN_PAYABLE": "         AC6. No. of days in payable  (365 to AC5)",
#         "WORKING_CAPITAL_TURNOVER": "AC7. Working capital turnover (F1 to B-E)",
#         "CASH_CONVERSION_CYCLE": "AC8. Cash conversion cycle (AC2+AC4-AC6)",

#         "DEBT_EQUITY_RATIO": "S1. Debt equity ratio [(D+E) to C]",
#         "DEBT_TO_ASSETS_RATIO": "         S2. Debt to assets ratio (  D+E as % of Avg. {Current year(A+B),previous year (A+B)})",
#         "DEBT_TO_CAPITAL_RATIO": "S3. Debt to capital ratio (D+E to H1)",
#         "INTEREST_COVER_RATIO": "S4. Interest cover ratio ( F6 to F7(i))",
#     }
#     # --------------------------------------------------------

#     def get_specific_variables_for_specific_org(self, entity_type: str, sector: str = None, sub_sector: str = None, org_name: str = None, target_year: str = None) -> dict:
#         """
#         Extracts specific financial variables for a particular organization
#         based on entity type, sector, sub-sector, and organization name.
#         It can return data for a specific year or all available years.

#         Args:
#             entity_type (str): The type of entity to load data for ('company' or 'bank').
#             sector (str, optional): The sector to filter by. Defaults to None.
#             sub_sector (str, optional): The sub-sector to filter by. Defaults to None.
#             org_name (str, optional): The organization name to filter by. Defaults to None.
#             target_year (str, optional): The year to retrieve data for. Can be a year (e.g., "2023")
#                                          or "all" for all available years. Defaults to None (all years).

#         Returns:
#             dict: A dictionary containing the extracted variables and their values.
#                   Returns an empty dictionary if no data or variables are found.
#         """
#         df = organization_data_service_instance.fetch_data_for_specific_org(
#             entity_type=entity_type,
#             sector=sector,
#             sub_sector=sub_sector,
#             org_name=org_name,
#         )

#         if df is None or df.empty:
#             print("Error: No data fetched for the specified organization.")
#             return {}

#         variables_to_map = self.BANK_VARIABLES_MAP if entity_type.lower() == "bank" else self.COMPANY_VARIABLES_MAP

#         extracted_data = {}
#         year_columns = [col for col in df.columns if isinstance(col, int)]

#         target_year_int = None
#         if target_year is not None and target_year.lower() != 'all':
#             try:
#                 target_year_int = int(target_year)
#             except ValueError:
#                 print(f"Error: target_year '{target_year}' cannot be converted to an integer. Returning empty data.")
#                 return {}

#         for var_name, search_term_or_list in variables_to_map.items():
#             found_data_for_var = False
#             # Normalize search_term_or_list into a list of strings
#             search_terms = [search_term_or_list] if isinstance(search_term_or_list, str) else search_term_or_list

#             for _, row in df.iterrows():
#                 # Check each search term in the list against the indicator columns
#                 for term in search_terms:
#                     # Removed .strip() from both term and DataFrame columns for exact matching
#                     if (term in str(row.get('Indicator', '')) or
#                         term in str(row.get('Sub Indicator', '')) or
#                         term in str(row.get('Sub-Sub Indicator', ''))):
                        
#                         found_data_for_var = True
#                         yearly_data_full = {}
#                         for year in year_columns:
#                             if year in row:
#                                 yearly_data_full[year] = row[year]

#                         if target_year_int is not None:
#                             extracted_data[var_name] = {target_year_int: yearly_data_full.get(target_year_int, None)}
#                         else:
#                             extracted_data[var_name] = yearly_data_full
#                         break # Break from inner 'for term in search_terms' loop once found
#                 if found_data_for_var:
#                     break # Break from outer 'for _, row in df.iterrows()' loop once found for this var

#             if not found_data_for_var:
#                 if target_year_int is not None:
#                     extracted_data[var_name] = {target_year_int: None}
#                 else:
#                     extracted_data[var_name] = {year: None for year in year_columns}
#                 if not extracted_data[var_name]:
#                     extracted_data[var_name] = None

#         return extracted_data

#     def get_specific_variables_by_sector(self, entity_type: str, sector: str, target_year: str = None) -> dict:
#         """
#         Calculates the average of specific financial variables for all
#         organizations within a given sector (including all sub-sectors).
#         It can return averages for a specific year or all available years.

#         Args:
#             entity_type (str): The type of entity to load data for ('company' or 'bank').
#             sector (str): The sector to filter by.
#             target_year (str, optional): The year to retrieve data for. Can be a year (e.g., "2023")
#                                          or "all" for all available years. Defaults to None (all years).

#         Returns:
#             dict: A dictionary containing the aggregated (averaged) variables and their values.
#                   Returns an empty dictionary if no data or variables are found for the sector.
#         """
#         df_sector = organization_data_service_instance.fetch_data_by_sector(entity_type=entity_type, sector=sector)

#         if df_sector is None or df_sector.empty:
#             print(f"Error: No data fetched for the sector: {sector}.")
#             return {}

#         variables_to_map = self.BANK_VARIABLES_MAP if entity_type.lower() == "bank" else self.COMPANY_VARIABLES_MAP

#         aggregated_data = {}
#         year_columns = [col for col in df_sector.columns if isinstance(col, int)]

#         target_year_int = None
#         if target_year is not None and target_year.lower() != 'all':
#             try:
#                 target_year_int = int(target_year)
#             except ValueError:
#                 print(f"Error: target_year '{target_year}' cannot be converted to an integer. Returning empty data.")
#                 return {}

#         for var_name, search_term_or_list in variables_to_map.items():
#             # Normalize search_term_or_list into a list of strings
#             search_terms = [search_term_or_list] if isinstance(search_term_or_list, str) else search_term_or_list

#             # Build a combined boolean condition for matching rows
#             combined_condition = pd.Series([False] * len(df_sector)) # Initialize with all False
#             for term in search_terms:
#                 # Removed .strip() from both term and DataFrame columns for exact matching
#                 condition_for_term = (
#                     df_sector['Indicator'].astype(str).str.contains(term, case=False, na=False, regex=False) |
#                     df_sector['Sub Indicator'].astype(str).str.contains(term, case=False, na=False, regex=False) |
#                     df_sector['Sub-Sub Indicator'].astype(str).str.contains(term, case=False, na=False, regex=False)
#                 )
#                 combined_condition = combined_condition | condition_for_term # OR conditions for each term

#             matching_rows = df_sector[combined_condition]

#             if not matching_rows.empty:
#                 if target_year_int is not None:
#                     values = pd.to_numeric(matching_rows[target_year_int], errors='coerce')
#                     valid_values = values.dropna()
#                     avg_value = valid_values.mean() if not valid_values.empty else None
#                     aggregated_data[var_name] = {target_year_int: avg_value}
#                 else:
#                     yearly_averages = {}
#                     for year in year_columns:
#                         values = pd.to_numeric(matching_rows[year], errors='coerce')
#                         valid_values = values.dropna()
#                         yearly_averages[year] = valid_values.mean() if not valid_values.empty else None
#                     aggregated_data[var_name] = yearly_averages
#             else:
#                 if target_year_int is not None:
#                     aggregated_data[var_name] = {target_year_int: None}
#                 else:
#                     aggregated_data[var_name] = {year: None for year in year_columns}
#                 if not aggregated_data[var_name]:
#                     aggregated_data[var_name] = None
#         return aggregated_data

# # Instantiate the service for use in views
# financial_variables_service_instance = FinancialVariablesService()


import pandas as pd
# from credit_risk.services.OrganizationDataService import organization_data_service_instance
from .OrganizationDataService import organization_data_service_instance

class FinancialVariablesService:
    """
    Service responsible for extracting specific financial variables for individual
    organizations or calculating averages for entire sectors.
    """

    # --- Module-level Variable Mappings (DRY Principle) ---
    # These mappings define the user-friendly variable names and their corresponding
    # search terms found in the 'Indicator', 'Sub Indicator', or 'Sub-Sub Indicator' columns
    # of the Excel data.
    BANK_VARIABLES_MAP = {
        # PROFITABILITY AND EFFICIENCY
        "SPREAD_RATIO": "1. Spread Ratio (D3/D1)",
        "NET_INTEREST_MARGIN": "2. Net markup/interest margin (D1-D2)/C",
        "RETURN_ON_EQUITY": "3. Return on equity (ROE) (D10/A)",
        "RETURN_ON_ASSETS": "4. Return on assets (ROA) (D10/C)",
        "NON_INTEREST_INCOME_RATIO": "5. Non-markup/interest income to total assets (D6/C)",
        
        # LIQUIDITY 
        "CASH_TO_TOTAL_ASSETS_RATIO": "1. Cash & cash equivalent to total assets (C1+C2)/C",
        "INVESTMENT_TO_TOTAL_ASSETS": "2. Investment to total assets (C4/C)",
        "ADVANCES_TO_TOTAL_ASSETS": "3. Advances net of provisions to total assets (C8/C)",
        "DEPOSIT_TO_TOTAL_ASSETS": "4. Deposits to total assets (B3/C)",
        "TOTAL_LIABILITIES_TO_TOTAL_ASSETS": "5. Total liabilities to total assets (B/C)",
        "GROSS_ADVANCES_TO_DEPOSITS": "6. Gross advances to deposits (C5/B3)",
        "GROSS_ADVANCES_TO_BORROWING_AND_DEPOSIT": "7. Gross advances to borrowing & deposits C5/(B2+B3)",

        # ASSETS QUALITY RATIOS
        "NON_PERFORMING_LOANS_TO_GROSS_ADVANCES": "1. Non-performing loans to gross advances (C6/C5)",
        "PROVISION_AGAINST_NPLS_TO_GROSS_ADVANCES": "2. Provisions against NPLs to gross advances (C7/C5)",
        "NPL_TO_TOTAL_EQUITY": "3. NPLs to total equity (C6/A)",
        
        # LEVERAGE RATIOS 
        "CAPITAL_RATIO": "1. Capital ratio (A/C)",
        # MODIFIED: Allow for either '3.' or '4.' prefix
        "TOTAL_DEPOSIT_TO_EQUITY_RATIO": [
            "3. Total deposit to total equity (B3/A) (times)",
            "4. Total deposit to total equity (B3/A) (times)"
        ],
    }

    COMPANY_VARIABLES_MAP = {
        "NET_PROFIT_MARGIN": "         P1. Net Profit  margin / Net profit to sales (F10 as % of F1)",
        "RETURN_ON_ASSETS": "         P3. Return on Assets  (F10 as a % of Avg {Current year(A+B),previous year (A+B)}",
        "RETURN_ON_EQUITY": "P5. Return on equity (F10 as % of Avg {Current year(C),previous year (C)}",
        "GROSS_PROFIT_MARGIN": "         P6. Gross profit  margin / Gross profit to sales (F3 as % of F1)",
        "OPERATING_RETURN_ON_ASSETS": "P7. Operating return on assets (F6 as a % of Avg. {Current year(A+B),previous year (A+B)}",
        "RETURN_ON_CAPITAL_EMPLOYED": "P8. Return on capital employed(F7 as a % of Avg {Current year H1, previous year H1}",

        "CURRENT_RATIO":"L1. Current ratio (B to E)",
        "QUICK_RATIO": "L2. Quick ratio (B1+B3+B5 to E)",
        "CASH_TO_CURRENT_LIABILITIES_RATIO": "L3. Cash to current liabilities (B1+B5 to E)",

        "NUM_OF_DAYS_IN_INVENTORY": "AC2. No. of days in inventory ",
        "NUM_OF_DAYS_IN_RECEIVABLES": "AC4. No. of days in receivables (365 to AC3)",
        "NUM_OF_DAYS_IN_PAYABLE": "         AC6. No. of days in payable  (365 to AC5)",
        "WORKING_CAPITAL_TURNOVER": "AC7. Working capital turnover (F1 to B-E)",
        "CASH_CONVERSION_CYCLE": "AC8. Cash conversion cycle (AC2+AC4-AC6)",

        "DEBT_EQUITY_RATIO": "S1. Debt equity ratio [(D+E) to C]",
        "DEBT_TO_ASSETS_RATIO": "         S2. Debt to assets ratio (  D+E as % of Avg. {Current year(A+B),previous year (A+B)})",
        "DEBT_TO_CAPITAL_RATIO": "S3. Debt to capital ratio (D+E to H1)",
        "INTEREST_COVER_RATIO": "S4. Interest cover ratio ( F6 to F7(i))",
    }
    # --------------------------------------------------------

    def _normalize_string(self, text: str) -> str:
        """Removes leading/trailing spaces and condenses multiple internal spaces to a single space."""
        if not isinstance(text, str):
            text = str(text) # Ensure it's a string
        return " ".join(text.split())

    def get_specific_variables_for_specific_org(self, entity_type: str, sector: str = None, sub_sector: str = None, org_name: str = None, target_year: str = None) -> dict:
        """
        Extracts specific financial variables for a particular organization
        based on entity type, sector, sub-sector, and organization name.
        It can return data for a specific year or all available years.

        Args:
            entity_type (str): The type of entity to load data for ('company' or 'bank').
            sector (str, optional): The sector to filter by. Defaults to None.
            sub_sector (str, optional): The sub-sector to filter by. Defaults to None.
            org_name (str, optional): The organization name to filter by. Defaults to None.
            target_year (str, optional): The year to retrieve data for. Can be a year (e.g., "2023")
                                         or "all" for all available years. Defaults to None (all years).

        Returns:
            dict: A dictionary containing the extracted variables and their values.
                  Returns an empty dictionary if no data or variables are found.
        """
        df = organization_data_service_instance.fetch_data_for_specific_org(
            entity_type=entity_type,
            sector=sector,
            sub_sector=sub_sector,
            org_name=org_name,
        )

        if df is None or df.empty:
            print("Error: No data fetched for the specified organization.")
            return {}

        variables_to_map = self.BANK_VARIABLES_MAP if entity_type.lower() == "bank" else self.COMPANY_VARIABLES_MAP

        extracted_data = {}
        year_columns = [col for col in df.columns if isinstance(col, int)]

        target_year_int = None
        if target_year is not None and target_year.lower() != 'all':
            try:
                target_year_int = int(target_year)
            except ValueError:
                print(f"Error: target_year '{target_year}' cannot be converted to an integer. Returning empty data.")
                return {}

        for var_name, search_term_or_list in variables_to_map.items():
            found_data_for_var = False
            search_terms = [search_term_or_list] if isinstance(search_term_or_list, str) else search_term_or_list
            normalized_search_terms = [self._normalize_string(term) for term in search_terms]


            for _, row in df.iterrows():
                # Normalize the DataFrame column values once per row
                indicator_val = self._normalize_string(row.get('Indicator', ''))
                sub_indicator_val = self._normalize_string(row.get('Sub Indicator', ''))
                sub_sub_indicator_val = self._normalize_string(row.get('Sub-Sub Indicator', ''))

                for normalized_term in normalized_search_terms:
                    # Using 'in' for literal substring check after normalization
                    if (normalized_term in indicator_val or
                        normalized_term in sub_indicator_val or
                        normalized_term in sub_sub_indicator_val):
                        
                        found_data_for_var = True
                        yearly_data_full = {}
                        for year in year_columns:
                            if year in row:
                                yearly_data_full[year] = row[year]

                        if target_year_int is not None:
                            extracted_data[var_name] = {target_year_int: yearly_data_full.get(target_year_int, None)}
                        else:
                            extracted_data[var_name] = yearly_data_full
                        break # Break from inner 'for term in search_terms' loop once found
                if found_data_for_var:
                    break # Break from outer 'for _, row in df.iterrows()' loop once found for this var

            if not found_data_for_var:
                if target_year_int is not None:
                    extracted_data[var_name] = {target_year_int: None}
                else:
                    extracted_data[var_name] = {year: None for year in year_columns}
                if not extracted_data[var_name]:
                    extracted_data[var_name] = None

        return extracted_data

    def get_specific_variables_by_sector(self, entity_type: str, sector: str, target_year: str = None) -> dict:
        """
        Calculates the average of specific financial variables for all
        organizations within a given sector (including all sub-sectors).
        It can return averages for a specific year or all available years.

        Args:
            entity_type (str): The type of entity to load data for ('company' or 'bank').
            sector (str): The sector to filter by.
            target_year (str, optional): The year to retrieve data for. Can be a year (e.g., "2023")
                                         or "all" for all available years. Defaults to None (all years).

        Returns:
            dict: A dictionary containing the aggregated (averaged) variables and their values.
                  Returns an empty dictionary if no data or variables are found for the sector.
        """
        df_sector = organization_data_service_instance.fetch_data_by_sector(entity_type=entity_type, sector=sector)

        if df_sector is None or df_sector.empty:
            print(f"Error: No data fetched for the sector: {sector}.")
            return {}

        variables_to_map = self.BANK_VARIABLES_MAP if entity_type.lower() == "bank" else self.COMPANY_VARIABLES_MAP

        aggregated_data = {}
        year_columns = [col for col in df_sector.columns if isinstance(col, int)]

        target_year_int = None
        if target_year is not None and target_year.lower() != 'all':
            try:
                target_year_int = int(target_year)
            except ValueError:
                print(f"Error: target_year '{target_year}' cannot be converted to an integer. Returning empty data.")
                return {}

        for var_name, search_term_or_list in variables_to_map.items():
            search_terms = [search_term_or_list] if isinstance(search_term_or_list, str) else search_term_or_list
            normalized_search_terms = [self._normalize_string(term) for term in search_terms]

            # Initialize combined_condition with the same index as df_sector
            combined_condition = pd.Series(False, index=df_sector.index) 
            for normalized_term in normalized_search_terms:
                # Apply normalization directly before str.contains for efficiency on Series
                condition_for_term = (
                    df_sector['Indicator'].astype(str).apply(self._normalize_string).str.contains(normalized_term, case=False, na=False, regex=False) |
                    df_sector['Sub Indicator'].astype(str).apply(self._normalize_string).str.contains(normalized_term, case=False, na=False, regex=False) |
                    df_sector['Sub-Sub Indicator'].astype(str).apply(self._normalize_string).str.contains(normalized_term, case=False, na=False, regex=False)
                )
                combined_condition = combined_condition | condition_for_term # OR conditions for each term

            matching_rows = df_sector[combined_condition]

            if not matching_rows.empty:
                if target_year_int is not None:
                    values = pd.to_numeric(matching_rows[target_year_int], errors='coerce')
                    valid_values = values.dropna()
                    avg_value = valid_values.mean() if not valid_values.empty else None
                    aggregated_data[var_name] = {target_year_int: avg_value}
                else:
                    yearly_averages = {}
                    for year in year_columns:
                        values = pd.to_numeric(matching_rows[year], errors='coerce')
                        valid_values = values.dropna()
                        yearly_averages[year] = valid_values.mean() if not valid_values.empty else None
                    aggregated_data[var_name] = yearly_averages
            else:
                if target_year_int is not None:
                    aggregated_data[var_name] = {target_year_int: None}
                else:
                    aggregated_data[var_name] = {year: None for year in year_columns}
                if not aggregated_data[var_name]:
                    aggregated_data[var_name] = None
        return aggregated_data

# Instantiate the service for use in views
financial_variables_service_instance = FinancialVariablesService()