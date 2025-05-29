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

#     def _normalize_string(self, text: str) -> str:
#         """Removes leading/trailing spaces and condenses multiple internal spaces to a single space."""
#         if not isinstance(text, str):
#             text = str(text) # Ensure it's a string
#         return " ".join(text.split())

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
#             search_terms = [search_term_or_list] if isinstance(search_term_or_list, str) else search_term_or_list
#             normalized_search_terms = [self._normalize_string(term) for term in search_terms]


#             for _, row in df.iterrows():
#                 # Normalize the DataFrame column values once per row
#                 indicator_val = self._normalize_string(row.get('Indicator', ''))
#                 sub_indicator_val = self._normalize_string(row.get('Sub Indicator', ''))
#                 sub_sub_indicator_val = self._normalize_string(row.get('Sub-Sub Indicator', ''))

#                 for normalized_term in normalized_search_terms:
#                     # Using 'in' for literal substring check after normalization
#                     if (normalized_term in indicator_val or
#                         normalized_term in sub_indicator_val or
#                         normalized_term in sub_sub_indicator_val):
                        
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
#             search_terms = [search_term_or_list] if isinstance(search_term_or_list, str) else search_term_or_list
#             normalized_search_terms = [self._normalize_string(term) for term in search_terms]

#             # Initialize combined_condition with the same index as df_sector
#             combined_condition = pd.Series(False, index=df_sector.index) 
#             for normalized_term in normalized_search_terms:
#                 # Apply normalization directly before str.contains for efficiency on Series
#                 condition_for_term = (
#                     df_sector['Indicator'].astype(str).apply(self._normalize_string).str.contains(normalized_term, case=False, na=False, regex=False) |
#                     df_sector['Sub Indicator'].astype(str).apply(self._normalize_string).str.contains(normalized_term, case=False, na=False, regex=False) |
#                     df_sector['Sub-Sub Indicator'].astype(str).apply(self._normalize_string).str.contains(normalized_term, case=False, na=False, regex=False)
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
#         # NEW VARIABLES FOR RANKING - BANKS
#         "REVENUE": "D. Profit & loss account",
#         "ASSETS": "C. Total assets (C1 to C4 + C8 to C10)",
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
#         # NEW VARIABLES FOR RANKING - COMPANIES
#         "REVENUE": "1. Sales",
#         "ASSETS": " Total Assets (A+B) / Equity & Liabilities (C+D+E)",
#     }
#     # --------------------------------------------------------

#     def _normalize_string(self, text: str) -> str:
#         """Removes leading/trailing spaces and condenses multiple internal spaces to a single space."""
#         if not isinstance(text, str):
#             text = str(text) # Ensure it's a string
#         return " ".join(text.split())

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
#             search_terms = [search_term_or_list] if isinstance(search_term_or_list, str) else search_term_or_list
#             normalized_search_terms = [self._normalize_string(term) for term in search_terms]


#             for _, row in df.iterrows():
#                 # Normalize the DataFrame column values once per row
#                 indicator_val = self._normalize_string(row.get('Indicator', ''))
#                 sub_indicator_val = self._normalize_string(row.get('Sub Indicator', ''))
#                 sub_sub_indicator_val = self._normalize_string(row.get('Sub-Sub Indicator', ''))

#                 for normalized_term in normalized_search_terms:
#                     # Using 'in' for literal substring check after normalization
#                     if (normalized_term in indicator_val or
#                         normalized_term in sub_indicator_val or
#                         normalized_term in sub_sub_indicator_val):
                        
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
#             search_terms = [search_term_or_list] if isinstance(search_term_or_list, str) else search_term_or_list
#             normalized_search_terms = [self._normalize_string(term) for term in search_terms]

#             # Initialize combined_condition with the same index as df_sector
#             combined_condition = pd.Series(False, index=df_sector.index) 
#             for normalized_term in normalized_search_terms:
#                 # Apply normalization directly before str.contains for efficiency on Series
#                 condition_for_term = (
#                     df_sector['Indicator'].astype(str).apply(self._normalize_string).str.contains(normalized_term, case=False, na=False, regex=False) |
#                     df_sector['Sub Indicator'].astype(str).apply(self._normalize_string).str.contains(normalized_term, case=False, na=False, regex=False) |
#                     df_sector['Sub-Sub Indicator'].astype(str).apply(self._normalize_string).str.contains(normalized_term, case=False, na=False, regex=False)
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

#     def get_all_organizations_variable_for_year_by_sector(self, entity_type: str, sector: str, variable_key: str, target_year: int) -> list[tuple[str, float]]:
#         """
#         Retrieves a specific variable's numeric value for all organizations within a sector for a given year.
#         Used primarily for ranking.

#         Args:
#             entity_type (str): 'company' or 'bank'.
#             sector (str): The sector to filter by.
#             variable_key (str): The internal key of the variable in BANK_VARIABLES_MAP or COMPANY_VARIABLES_MAP (e.g., "REVENUE", "ASSETS", "RETURN_ON_ASSETS").
#             target_year (int): The specific year to retrieve data for.

#         Returns:
#             list[tuple[str, float]]: A list of (organization_name, variable_value) tuples.
#                                      Values will be None if not found or non-numeric.
#         """
#         # Fetch raw data for all organizations in the sector.
#         # This assumes fetch_data_by_sector returns a DataFrame where 'Org Name'
#         # is a column, and data is not yet aggregated/averaged.
#         df_all_orgs_in_sector = organization_data_service_instance.fetch_data_by_sector(entity_type=entity_type, sector=sector)

#         if df_all_orgs_in_sector is None or df_all_orgs_in_sector.empty:
#             print(f"No raw data fetched for sector {sector} for ranking variable {variable_key}.")
#             return []

#         variables_map = self.BANK_VARIABLES_MAP if entity_type.lower() == "bank" else self.COMPANY_VARIABLES_MAP

#         search_term_or_list = variables_map.get(variable_key)
#         if search_term_or_list is None:
#             print(f"Warning: Variable key '{variable_key}' not found in {entity_type} map. Cannot rank.")
#             return []

#         search_terms = [search_term_or_list] if isinstance(search_term_or_list, str) else search_term_or_list
#         normalized_search_terms = [self._normalize_string(term) for term in search_terms]

#         organization_values = {}
        
#         # Group by 'Org Name' to process each organization's set of variables
#         ORG_NAME_COLUMN = 'Org Name' 
#         if ORG_NAME_COLUMN not in df_all_orgs_in_sector.columns:
#             # Rephrase the error message to reflect the current service's expectation
#             print(f"Error: '{ORG_NAME_COLUMN}' column not found in DataFrame for ranking in FinancialVariablesService. Please ensure OrganizationDataService provides this column as '{ORG_NAME_COLUMN}'.")
#             return []

#         for org_name, org_df in df_all_orgs_in_sector.groupby(ORG_NAME_COLUMN):
#             found_value = None
#             # Iterate through rows for this specific organization to find the variable
#             for _, row in org_df.iterrows():
#                 indicator_val = self._normalize_string(row.get('Indicator', ''))
#                 sub_indicator_val = self._normalize_string(row.get('Sub Indicator', ''))
#                 sub_sub_indicator_val = self._normalize_string(row.get('Sub-Sub Indicator', ''))

#                 for normalized_term in normalized_search_terms:
#                     if (normalized_term in indicator_val or
#                         normalized_term in sub_indicator_val or
#                         normalized_term in sub_sub_indicator_val):
                        
#                         # Check if the target_year column exists and has a non-null value
#                         if target_year in row and pd.notna(row[target_year]):
#                             try:
#                                 found_value = float(row[target_year])
#                             except (ValueError, TypeError):
#                                 # If conversion fails, value remains None
#                                 found_value = None
#                             break # Found the variable's row for this organization
#                 if found_value is not None:
#                     break # Found the value for this organization, move to next organization

#             organization_values[org_name] = found_value
            
#         # Filter out organizations with None values for the target variable and return
#         return [(org, value) for org, value in organization_values.items() if value is not None]

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
        # NEW VARIABLES FOR RANKING - BANKS
        "REVENUE": "D. Profit & loss account", # This might need refinement based on exact data, if 'D. Profit & loss account' is too general and covers many rows.
        "ASSETS": "C. Total assets (C1 to C4 + C8 to C10)",
    }

    COMPANY_VARIABLES_MAP = {
        "NET_PROFIT_MARGIN": "P1. Net Profit margin / Net profit to sales (F10 as % of F1)",
        "RETURN_ON_ASSETS": "P3. Return on Assets (F10 as a % of Avg {Current year(A+B),previous year (A+B)}",
        "RETURN_ON_EQUITY": "P5. Return on equity (F10 as % of Avg {Current year(C),previous year (C)}",
        "GROSS_PROFIT_MARGIN": "P6. Gross profit margin / Gross profit to sales (F3 as % of F1)",
        "OPERATING_RETURN_ON_ASSETS": "P7. Operating return on assets (F6 as a % of Avg. {Current year(A+B),previous year (A+B)}",
        "RETURN_ON_CAPITAL_EMPLOYED": "P8. Return on capital employed(F7 as a % of Avg {Current year H1, previous year H1}",

        "CURRENT_RATIO":"L1. Current ratio (B to E)",
        "QUICK_RATIO": "L2. Quick ratio (B1+B3+B5 to E)",
        "CASH_TO_CURRENT_LIABILITIES_RATIO": "L3. Cash to current liabilities (B1+B5 to E)",

        "NUM_OF_DAYS_IN_INVENTORY": "AC2. No. of days in inventory ",
        "NUM_OF_DAYS_IN_RECEIVABLES": "AC4. No. of days in receivables (365 to AC3)",
        "NUM_OF_DAYS_IN_PAYABLE": "AC6. No. of days in payable (365 to AC5)",
        "WORKING_CAPITAL_TURNOVER": "AC7. Working capital turnover (F1 to B-E)",
        "CASH_CONVERSION_CYCLE": "AC8. Cash conversion cycle (AC2+AC4-AC6)",

        "DEBT_EQUITY_RATIO": "S1. Debt equity ratio [(D+E) to C]",
        "DEBT_TO_ASSETS_RATIO": "S2. Debt to assets ratio ( D+E as % of Avg. {Current year(A+B),previous year (A+B)})",
        "DEBT_TO_CAPITAL_RATIO": "S3. Debt to capital ratio (D+E to H1)",
        "INTEREST_COVER_RATIO": "S4. Interest cover ratio ( F6 to F7(i))",
        # NEW VARIABLES FOR RANKING - COMPANIES
        "REVENUE": "1. Sales",
        "ASSETS": "Total Assets (A+B) / Equity & Liabilities (C+D+E)",
    }
    # --------------------------------------------------------

    def _normalize_string(self, text: str) -> str:
        """Removes leading/trailing spaces and condenses multiple internal spaces to a single space."""
        if not isinstance(text, str):
            text = str(text) # Ensure it's a string
        return " ".join(text.strip().split()) # Added .strip() for leading/trailing


    def _find_variable_row(self, df: pd.DataFrame, search_terms: list[str]) -> pd.Series | None:
        """
        Helper to find a row in a DataFrame that matches any of the search terms
        in 'Indicator', 'Sub Indicator', or 'Sub-Sub Indicator' columns.
        Returns the first matching row as a Series, or None if no match.
        """
        normalized_search_terms = [self._normalize_string(term) for term in search_terms]

        for col in ['Indicator', 'Sub Indicator', 'Sub-Sub Indicator']:
            if col in df.columns:
                # Ensure the column is string type, normalize, then check for containment
                normalized_col_series = df[col].astype(str).apply(self._normalize_string)
                for term in normalized_search_terms:
                    # Using regex=False for literal string matching for performance
                    matching_rows = df[normalized_col_series.str.contains(term, case=False, na=False, regex=False)]
                    if not matching_rows.empty:
                        return matching_rows.iloc[0] # Return the first matching row

        return None # No matching row found

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
            print(f"Error: No data fetched for the specified organization: {org_name}.")
            return {}

        variables_to_map = self.BANK_VARIABLES_MAP if entity_type.lower() == "bank" else self.COMPANY_VARIABLES_MAP

        extracted_data = {}
        # Get list of year columns present in the DataFrame
        year_columns = [col for col in df.columns if isinstance(col, int) and col > 1900 and col < 2100] # Basic year validation

        target_year_int = None
        if target_year is not None and str(target_year).lower() != 'all':
            try:
                target_year_int = int(target_year)
                if target_year_int not in year_columns:
                    print(f"Warning: Target year {target_year_int} not found in available data columns for {org_name}. Available years: {year_columns}")
                    # If target_year_int is not in columns, we can't fetch it, so treat as 'all' or return empty.
                    # For now, let's proceed and it will result in None for that year.
            except ValueError:
                print(f"Error: target_year '{target_year}' cannot be converted to an integer. Returning empty data.")
                return {}

        for var_name, search_term_or_list in variables_to_map.items():
            search_terms = [search_term_or_list] if isinstance(search_term_or_list, str) else search_term_or_list
            
            # Use the helper function to find the relevant row for this variable
            matching_row = self._find_variable_row(df, search_terms)

            if matching_row is not None:
                yearly_data_full = {}
                for year in year_columns:
                    if year in matching_row and pd.notna(matching_row[year]):
                        try:
                            yearly_data_full[year] = float(matching_row[year])
                        except (ValueError, TypeError):
                            yearly_data_full[year] = None # Coerce non-numeric to None
                    else:
                        yearly_data_full[year] = None

                if target_year_int is not None:
                    # If a specific year is requested, only include that year's data
                    extracted_data[var_name] = {target_year_int: yearly_data_full.get(target_year_int, None)}
                else:
                    # Otherwise, include all years
                    extracted_data[var_name] = yearly_data_full
            else:
                # If no matching row found for the variable
                if target_year_int is not None:
                    extracted_data[var_name] = {target_year_int: None}
                else:
                    # If 'all' years requested, but no row found, populate all years with None
                    extracted_data[var_name] = {year: None for year in year_columns}
                # If there are no year columns at all, and no row, ensure it's None.
                if not extracted_data[var_name] and (target_year_int is None or target_year_int not in year_columns):
                     extracted_data[var_name] = None # Fallback for no data for any year

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
        year_columns = [col for col in df_sector.columns if isinstance(col, int) and col > 1900 and col < 2100]

        target_year_int = None
        if target_year is not None and str(target_year).lower() != 'all':
            try:
                target_year_int = int(target_year)
            except ValueError:
                print(f"Error: target_year '{target_year}' cannot be converted to an integer. Returning empty data.")
                return {}

        for var_name, search_term_or_list in variables_to_map.items():
            search_terms = [search_term_or_list] if isinstance(search_term_or_list, str) else search_term_or_list
            normalized_search_terms = [self._normalize_string(term) for term in search_terms]

            # Build a combined boolean condition for all search terms
            combined_condition = pd.Series(False, index=df_sector.index) 
            for normalized_term in normalized_search_terms:
                # Apply normalization directly before str.contains for efficiency on Series
                # Use .fillna('') for string columns to avoid errors if there are NaNs
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
                # If no matching row found for the variable in the entire sector
                if target_year_int is not None:
                    aggregated_data[var_name] = {target_year_int: None}
                else:
                    # If 'all' years requested, but no row found, populate all years with None
                    aggregated_data[var_name] = {year: None for year in year_columns}
                # Fallback if no year columns found or no data
                if not aggregated_data[var_name] and (target_year_int is None or target_year_int not in year_columns):
                    aggregated_data[var_name] = None
        return aggregated_data

    def get_all_organizations_variable_for_year_by_sector(self, entity_type: str, sector: str, variable_key: str, target_year: int) -> list[tuple[str, float]]:
        """
        Retrieves a specific variable's numeric value for all organizations within a sector for a given year.
        Used primarily for ranking.

        Args:
            entity_type (str): 'company' or 'bank'.
            sector (str): The sector to filter by.
            variable_key (str): The internal key of the variable in BANK_VARIABLES_MAP or COMPANY_VARIABLES_MAP (e.g., "REVENUE", "ASSETS", "RETURN_ON_ASSETS").
            target_year (int): The specific year to retrieve data for.

        Returns:
            list[tuple[str, float]]: A list of (organization_name, variable_value) tuples.
                                     Values will be None if not found or non-numeric.
        """
        df_all_orgs_in_sector = organization_data_service_instance.fetch_data_by_sector(entity_type=entity_type, sector=sector)

        if df_all_orgs_in_sector is None or df_all_orgs_in_sector.empty:
            print(f"No raw data fetched for sector {sector} for ranking variable {variable_key}.")
            return []

        variables_map = self.BANK_VARIABLES_MAP if entity_type.lower() == "bank" else self.COMPANY_VARIABLES_MAP

        search_term_or_list = variables_map.get(variable_key)
        if search_term_or_list is None:
            print(f"Warning: Variable key '{variable_key}' not found in {entity_type} map. Cannot rank.")
            return []

        search_terms = [search_term_or_list] if isinstance(search_term_or_list, str) else search_term_or_list
        
        organization_values = []
        
        ORG_NAME_COLUMN = 'Org Name' 
        if ORG_NAME_COLUMN not in df_all_orgs_in_sector.columns:
            print(f"Error: '{ORG_NAME_COLUMN}' column not found in DataFrame for ranking. Please ensure OrganizationDataService provides this column as '{ORG_NAME_COLUMN}'.")
            return []

        # Iterate through each unique organization
        for org_name in df_all_orgs_in_sector[ORG_NAME_COLUMN].unique():
            org_df = df_all_orgs_in_sector[df_all_orgs_in_sector[ORG_NAME_COLUMN] == org_name].copy()
            
            # Use the helper function to find the relevant row for this variable within this organization's data
            matching_row = self._find_variable_row(org_df, search_terms)
            
            value_for_org = None
            if matching_row is not None:
                # Check if the target_year column exists and has a non-null value
                if target_year in matching_row and pd.notna(matching_row[target_year]):
                    try:
                        value_for_org = float(matching_row[target_year])
                    except (ValueError, TypeError):
                        value_for_org = None # If conversion fails, value remains None

            organization_values.append((org_name, value_for_org))
            
        # Filter out organizations with None values *after* attempting to get all values
        return [(org, value) for org, value in organization_values if value is not None]

# Instantiate the service for use in views
financial_variables_service_instance = FinancialVariablesService()