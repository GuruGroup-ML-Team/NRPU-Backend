# # project_root/credit_risk/services/logic_four_service.py

# import pandas as pd
# # Import the instance of FinancialRatiosService to fetch calculated ratios
# from credit_risk.services.FinancialRatiosService import financial_ratios_service_instance

# class RatioComparisonService:
#     """
#     Service responsible for comparing an organization's financial ratios against
#     industry benchmarks and assigning a score.
#     """

#     def _score_ratio(self, company_ratio, industry_ratio) -> int | None:
#         """
#         Compares a company's ratio to the industry benchmark and assigns a score
#         based on the universal mechanism. Handles non-numeric inputs like " -",
#         and provides specific logic for negative industry benchmarks.

#         Args:
#             company_ratio (float | str | None): The calculated ratio for the specific company/bank.
#             industry_ratio (float | str | None): The average ratio for the industry/sector.

#         Returns:
#             int: A score from 1 to 5, or None if comparison is not applicable or data is missing/invalid.
#         """
#         # --- Input Type Conversion and Handling Non-Numeric Values ---
#         try:
#             company_ratio = float(company_ratio) if company_ratio is not None else None
#         except (ValueError, TypeError):
#             # Catches cases where company_ratio might be a string like " -" or other non-numeric
#             company_ratio = None
        
#         try:
#             industry_ratio = float(industry_ratio) if industry_ratio is not None else None
#         except (ValueError, TypeError):
#             # Catches cases where industry_ratio might be a string like " -" or other non-numeric
#             industry_ratio = None

#         # If either value is not available or could not be converted to a number, cannot score.
#         if company_ratio is None or industry_ratio is None:
#             return None

#         # --- Edge Case Handling for Industry Ratio ---
#         if industry_ratio == 0:
#             if company_ratio == 0:
#                 return 3 # Both zero, considered on par
#             else:
#                 # If industry is zero, and company is not zero, direct percentage comparison is not meaningful.
#                 # Returning None, as a score cannot be logically derived from standard percentage rules.
#                 return None 

#         # --- Logic for Negative Industry Ratio Values (Universal "Higher is Better" Context) ---
#         if industry_ratio < 0:
#             if company_ratio >= 0:
#                 # If company is positive/zero, and industry is negative, this is generally a strong performance
#                 # relative to a struggling industry. Assigning a top score (5).
#                 return 5
#             else: # Both company_ratio and industry_ratio are negative (company_ratio < 0 and industry_ratio < 0)
#                 # In a "higher is better" context, a less negative value is better (closer to zero).
#                 # To apply the percentage logic, we'll compare absolute values but reverse the scoring:
#                 # A lower percentage (company's absolute value is much smaller than industry's absolute value)
#                 # implies better performance (less negative).

#                 percentage_of_industry_abs = (abs(company_ratio) / abs(industry_ratio)) * 100

#                 # Applying the "lower is better" mapping to the absolute percentage:
#                 if percentage_of_industry_abs <= 80: # Company is much less negative (better)
#                     return 5
#                 elif 81 <= percentage_of_industry_abs < 90: # Company is less negative (better)
#                     return 4
#                 elif 90 <= percentage_of_industry_abs <= 110: # Company is on par
#                     return 3
#                 elif 111 <= percentage_of_industry_abs < 120: # Company is more negative (worse)
#                     return 2
#                 elif percentage_of_industry_abs >= 120: # Company is much more negative (significantly worse)
#                     return 1
#                 # Fallback for unexpected cases within this negative-negative scenario
#                 return None

#         # --- Standard Scoring Logic (Industry Ratio is Positive) ---
#         # This applies when industry_ratio is positive.
#         # Calculate percentage of company ratio relative to industry ratio
#         percentage_of_industry = (company_ratio / industry_ratio) * 100

#         # Apply the universal scoring logic (higher is better)
#         if percentage_of_industry >= 120:
#             return 5
#         elif 111 <= percentage_of_industry < 120:
#             return 4
#         elif 90 <= percentage_of_industry <= 110:
#             return 3
#         elif 80 <= percentage_of_industry < 90:
#             return 2
#         elif percentage_of_industry < 80:
#             return 1
        
#         # Fallback for any uncovered scenarios (should not be reached if all ranges are covered)
#         return None

#     def compare_financial_ratios(self, entity_type: str, sector: str, sub_sector: str, org_name: str, year: int) -> dict | None:
#         """
#         Compares the financial ratios of a specific organization with its industry average
#         and provides a score for each sub-ratio and an average score for each main ratio category.

#         Args:
#             entity_type (str): The type of entity ("company" or "bank").
#             sector (str): The sector of the organization.
#             sub_sector (str): The sub-sector of the organization.
#             org_name (str): The name of the organization.
#             year (int): The year for which to perform the comparison.

#         Returns:
#             dict: A nested dictionary containing the comparison scores for each ratio,
#                   and average scores for each main ratio category.
#                   Returns None if data fetching fails or no ratios can be compared.
#         """
#         # Fetch company-specific ratios using the FinancialRatiosService
#         company_ratios = financial_ratios_service_instance.calculate_financial_ratios_for_specific_entity(
#             entity_type=entity_type,
#             sector=sector,
#             sub_sector=sub_sector,
#             org_name=org_name,
#             target_year=str(year) # Ensure year is passed as string to the underlying service
#         )
        
#         # Determine the industry sector for comparison. For banks, it's always "Banks".
#         industry_sector = "Banks" if entity_type.lower() == "bank" else sector
        
#         # Fetch industry average ratios using the FinancialRatiosService
#         industry_ratios = financial_ratios_service_instance.calculate_financial_ratios_for_specific_sector(
#             entity_type=entity_type,
#             sector=industry_sector,
#             target_year=str(year) # Ensure year is passed as string to the underlying service
#         )

#         if not company_ratios or not industry_ratios:
#             print(f"Could not retrieve ratios for comparison for {org_name} or its industry for year {year}.")
#             return None

#         comparison_results = {}
        
#         for main_ratio_category, company_sub_ratios in company_ratios.items():
#             # Ensure the main category exists in industry ratios before proceeding
#             if main_ratio_category not in industry_ratios:
#                 continue

#             industry_sub_ratios = industry_ratios[main_ratio_category]
            
#             # This list will hold only the *successfully calculated numerical scores*
#             # to ensure the average is only based on available, comparable ratios.
#             valid_scores_for_average = [] 
#             sub_ratio_scores = {}

#             for sub_ratio_name, company_raw_value in company_sub_ratios.items():
#                 # --- START OF FIX ---
#                 # When FinancialRatiosService is called with a specific target_year,
#                 # the individual ratio values are returned directly, not as a dict keyed by year.
#                 # So, company_raw_value is already the actual ratio value.
#                 company_value = company_raw_value
                
#                 # Retrieve the industry value for the current sub_ratio_name
#                 industry_value = industry_sub_ratios.get(sub_ratio_name)
#                 # --- END OF FIX ---

#                 score = self._score_ratio(company_value, industry_value) 
                
#                 sub_ratio_scores[sub_ratio_name] = {
#                     "Company Value": company_value,
#                     "Industry Value": industry_value,
#                     "Score": score
#                 }
                
#                 # ONLY append the score if it is NOT None. This excludes ratios that couldn't be scored
#                 # from influencing the average category score.
#                 if score is not None:
#                     valid_scores_for_average.append(score) 

#             # Calculate average category score based ONLY on valid_scores_for_average.
#             # If valid_scores_for_average is empty (all ratios in category were null), average will be None.
#             average_category_score = sum(valid_scores_for_average) / len(valid_scores_for_average) if valid_scores_for_average else None
            
#             comparison_results[main_ratio_category] = {
#                 "Sub-Ratios": sub_ratio_scores,
#                 "Average Category Score": average_category_score
#             }

#         return comparison_results

# # Instantiate the service for use in views
# ratio_comparison_service_instance = RatioComparisonService()
# project_root/credit_risk/services/logic_four_service.py
# project_root/credit_risk/services/logic_four_service.py

import pandas as pd
# Import the instance of FinancialRatiosService to fetch calculated ratios
# from credit_risk.services.FinancialRatiosService import financial_ratios_service_instance
from .FinancialRatiosService import financial_ratios_service_instance

class RatioComparisonService:
    """
    Service responsible for comparing an organization's financial ratios against
    industry benchmarks and assigning a score.
    """

    def _score_ratio(self, company_ratio, industry_ratio) -> int | None:
        """
        Compares a company's ratio to the industry benchmark and assigns a score
        based on the universal mechanism. Handles non-numeric inputs like " -",
        and provides specific logic for negative industry benchmarks.

        Args:
            company_ratio (float | str | None): The calculated ratio for the specific company/bank.
            industry_ratio (float | str | None): The average ratio for the industry/sector.

        Returns:
            int: A score from 1 to 5, or None if comparison is not applicable or data is missing/invalid.
        """
        # --- Input Type Conversion and Handling Non-Numeric Values ---
        try:
            company_ratio = float(company_ratio) if company_ratio is not None else None
        except (ValueError, TypeError):
            # Catches cases where company_ratio might be a string like " -" or other non-numeric
            company_ratio = None
        
        try:
            industry_ratio = float(industry_ratio) if industry_ratio is not None else None
        except (ValueError, TypeError):
            # Catches cases where industry_ratio might be a string like " -" or other non-numeric
            industry_ratio = None

        # If either value is not available or could not be converted to a number, cannot score.
        if company_ratio is None or industry_ratio is None:
            return None

        # --- Edge Case Handling for Industry Ratio ---
        if industry_ratio == 0:
            if company_ratio == 0:
                return 3 # Both zero, considered on par
            else:
                # If industry is zero, and company is not zero, direct percentage comparison is not meaningful.
                # Returning None, as a score cannot be logically derived from standard percentage rules.
                return None 

        # --- Logic for Negative Industry Ratio Values (Universal "Higher is Better" Context) ---
        if industry_ratio < 0:
            if company_ratio >= 0:
                # If company is positive/zero, and industry is negative, this is generally a strong performance
                # relative to a struggling industry. Assigning a top score (5).
                return 5
            else: # Both company_ratio and industry_ratio are negative (company_ratio < 0 and industry_ratio < 0)
                # In a "higher is better" context, a less negative value is better (closer to zero).
                # To apply the percentage logic, we'll compare absolute values but reverse the scoring:
                # A lower percentage (company's absolute value is much smaller than industry's absolute value)
                # implies better performance (less negative).

                percentage_of_industry_abs = (abs(company_ratio) / abs(industry_ratio)) * 100

                # Applying the "lower is better" mapping to the absolute percentage:
                if percentage_of_industry_abs <= 80: # Company is much less negative (better)
                    return 5
                elif 81 <= percentage_of_industry_abs < 90: # Company is less negative (better)
                    return 4
                elif 90 <= percentage_of_industry_abs <= 110.999: # Adjusted upper boundary for Score 3
                    return 3
                elif 111 <= percentage_of_industry_abs < 120: # Company is more negative (worse)
                    return 2
                elif percentage_of_industry_abs >= 120: # Company is much more negative (significantly worse)
                    return 1
                # Fallback for unexpected cases within this negative-negative scenario
                return None

        # --- Standard Scoring Logic (Industry Ratio is Positive) ---
        # This applies when industry_ratio is positive.
        # Calculate percentage of company ratio relative to industry ratio
        percentage_of_industry = (company_ratio / industry_ratio) * 100

        # Apply the universal scoring logic (higher is better)
        if percentage_of_industry >= 120:
            return 5
        elif 111 <= percentage_of_industry < 120:
            return 4
        elif 90 <= percentage_of_industry <= 110.999: # Adjusted upper boundary for Score 3
            return 3
        elif 80 <= percentage_of_industry < 90:
            return 2
        elif percentage_of_industry < 80:
            return 1
        
        # Fallback for any uncovered scenarios (should not be reached if all ranges are covered)
        return None

    def compare_financial_ratios(self, entity_type: str, sector: str, sub_sector: str, org_name: str, year: int | str) -> dict | None:
        """
        Compares the financial ratios of a specific organization with its industry average
        and provides a score for each sub-ratio and an average score for each main ratio category.

        Args:
            entity_type (str): The type of entity ("company" or "bank").
            sector (str): The sector of the organization.
            sub_sector (str): The sub-sector of the organization.
            org_name (str): The name of the organization.
            year (int | str): The year for which to perform the comparison. Can be an integer or 'all'.

        Returns:
            dict: A nested dictionary containing the comparison scores for each ratio,
                  and average scores for each main ratio category.
                  Returns None if data fetching fails or no ratios can be compared.
        """
        # Fetch company-specific ratios using the FinancialRatiosService
        company_ratios = financial_ratios_service_instance.calculate_financial_ratios_for_specific_entity(
            entity_type=entity_type,
            sector=sector,
            sub_sector=sub_sector,
            org_name=org_name,
            target_year=str(year) # Ensure year is passed as string to the underlying service
        )
        
        # Determine the industry sector for comparison. For banks, it's always "Banks".
        industry_sector = "Banks" if entity_type.lower() == "bank" else sector
        
        # Fetch industry average ratios using the FinancialRatiosService
        industry_ratios = financial_ratios_service_instance.calculate_financial_ratios_for_specific_sector(
            entity_type=entity_type,
            sector=industry_sector,
            target_year=str(year) # Ensure year is passed as string to the underlying service
        )

        if not company_ratios or not industry_ratios:
            print(f"Could not retrieve ratios for comparison for {org_name} or its industry for year {year}.")
            return None

        comparison_results = {}
        
        # Check if we are processing for a specific year or all years
        is_all_years = (str(year).lower() == 'all')

        for main_ratio_category, company_sub_ratios_data in company_ratios.items():
            # Ensure the main category exists in industry ratios before proceeding
            if main_ratio_category not in industry_ratios:
                continue

            industry_sub_ratios_data = industry_ratios[main_ratio_category]
            
            sub_ratio_scores = {}
            # Initialize for collecting scores per year for category average
            category_scores_by_year = {} # Stores {year: [score1, score2, ...]}

            for sub_ratio_name, company_ratio_value_or_dict in company_sub_ratios_data.items():
                
                # Retrieve the industry value for the current sub_ratio_name
                industry_ratio_value_or_dict = industry_sub_ratios_data.get(sub_ratio_name)

                if is_all_years:
                    # When year is 'all', company_ratio_value_or_dict and industry_ratio_value_or_dict
                    # are expected to be dictionaries of year -> value.
                    individual_year_scores = {}
                    individual_year_company_values = {}
                    individual_year_industry_values = {}
                    
                    # Collect all unique years from both company and industry data for this sub-ratio
                    all_years_for_sub_ratio = set()
                    if isinstance(company_ratio_value_or_dict, dict):
                        all_years_for_sub_ratio.update(company_ratio_value_or_dict.keys())
                    if isinstance(industry_ratio_value_or_dict, dict):
                        all_years_for_sub_ratio.update(industry_ratio_value_or_dict.keys())

                    for y in sorted(list(all_years_for_sub_ratio)):
                        company_val = company_ratio_value_or_dict.get(y) if isinstance(company_ratio_value_or_dict, dict) else None
                        industry_val = industry_ratio_value_or_dict.get(y) if isinstance(industry_ratio_value_or_dict, dict) else None
                        
                        score = self._score_ratio(company_val, industry_val)
                        
                        individual_year_scores[y] = score
                        individual_year_company_values[y] = company_val
                        individual_year_industry_values[y] = industry_val

                        # Collect score for category average calculation by year
                        if score is not None:
                            if y not in category_scores_by_year:
                                category_scores_by_year[y] = []
                            category_scores_by_year[y].append(score)
                    
                    sub_ratio_scores[sub_ratio_name] = {
                        "Company Value": individual_year_company_values,
                        "Industry Value": individual_year_industry_values,
                        "Score By Year": individual_year_scores
                    }
                else:
                    # When a specific year is requested, company_ratio_value_or_dict and
                    # industry_ratio_value_or_dict are expected to be the direct values.
                    company_val = company_ratio_value_or_dict
                    industry_val = industry_ratio_value_or_dict
                    
                    score = self._score_ratio(company_val, industry_val)
                    
                    sub_ratio_scores[sub_ratio_name] = {
                        "Company Value": company_val,
                        "Industry Value": industry_val,
                        "Score": score
                    }
                    
                    # For specific year, collect score for single category average
                    if score is not None:
                        if 'single_year_scores' not in locals(): # This helps avoid issues if 'single_year_scores' is not defined.
                            single_year_scores = []
                        single_year_scores.append(score)


            # Calculate average category score(s)
            if is_all_years:
                average_category_score = {}
                for y, scores_list in category_scores_by_year.items():
                    if scores_list:
                        average_category_score[y] = sum(scores_list) / len(scores_list)
                    else:
                        average_category_score[y] = None # No valid scores for this year in category
            else:
                # Calculate single average for the specific year
                if 'single_year_scores' in locals() and single_year_scores:
                    average_category_score = sum(single_year_scores) / len(single_year_scores)
                else:
                    average_category_score = None # No valid scores for the specific year in category
            
            comparison_results[main_ratio_category] = {
                "Sub-Ratios": sub_ratio_scores,
                "Average Category Score": average_category_score
            }

        return comparison_results

# Instantiate the service for use in views
ratio_comparison_service_instance = RatioComparisonService()