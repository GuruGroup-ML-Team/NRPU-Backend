# project_root/credit_risk/services/logic_five_service.py

import pandas as pd
from .RatioComparisonService import ratio_comparison_service_instance

class OverallScoreService:
    """
    Service responsible for calculating the overall weighted financial score
    for an organization based on its ratio comparison results and defined weightages.
    It supports both default and custom weightage schemes.
    """

    def _get_default_weights(self, entity_type: str, user_type: str) -> dict:
        """
        Returns default weightages for financial ratio categories based on entity and user type.
        """
        entity_type_lower = entity_type.lower()
        user_type_lower = user_type.lower()

        if entity_type_lower == "bank":
            if user_type_lower == "lender":
                return {
                    "Solvency Ratios": 0.4,
                    "Liquidity Ratios": 0.3,
                    "Profitability And Efficiency Ratios": 0.2,
                    "Asset Quality Ratios": 0.1
                }
            elif user_type_lower == "investor":
                return {
                    "Solvency Ratios": 0.1,
                    "Liquidity Ratios": 0.3,
                    "Profitability And Efficiency Ratios": 0.5,
                    "Asset Quality Ratios": 0.1
                }
        elif entity_type_lower == "company":
            if user_type_lower == "lender":
                return {
                    "Solvency Ratios": 0.4,
                    "Liquidity Ratios": 0.3,
                    "Efficiency Ratios": 0.2,
                    "Profitability Ratios": 0.1
                }
            elif user_type_lower == "investor":
                return {
                    "Solvency Ratios": 0.1,
                    "Liquidity Ratios": 0.3,
                    "Efficiency Ratios": 0.2,
                    "Profitability Ratios": 0.4
                }
        return {} 

    def _get_score_interpretation(self, score: float | None) -> str:
        """
        Provides a qualitative interpretation for a given numerical score based on predefined ranges.

        Args:
            score (float | None): The financial score.

        Returns:
            str: The interpretation string, or "N/A" if the score is None.
        """
        if score is None:
            return "N/A - Score not available"
        elif score >= 4.5:
            return "Strong Financial Health / Low Risk"
        elif 4.0 <= score < 4.5:
            return "Good Financial Health / Moderate-Low Risk"
        elif 3.0 <= score < 4.0:
            return "Average Financial Health / Moderate Risk"
        elif 2.0 <= score < 3.0:
            return "Below Average Financial Health / Moderate-High Risk"
        elif score < 2.0:
            return "Weak Financial Health / High Risk"
        return "N/A - Could not interpret score" # Fallback, should not be reached

    def calculate_overall_score(self, entity_type: str, sector: str, sub_sector: str, org_name: str, year: int | str,
                                 weight_type: str, user_type: str = None, custom_weights: dict = None) -> tuple[dict | None, dict, dict, str | dict]:
        """
        Calculates the overall weighted financial score for a company or bank.
        Returns a dictionary containing the raw score and its percentage equivalent if a specific year is requested,
        or a dictionary of {year: {raw_score, percentage_score}} if 'all' years are requested.
        Also returns the dictionary of weights that were applied, a detailed breakdown of the calculation,
        and an interpretation of the overall score.

        Args:
            entity_type (str): "Company" or "Bank".
            sector (str): The sector of the organization.
            sub_sector (str): The sub-sector of the organization.
            org_name (str): The name of the organization.
            year (int | str): The year for which to perform the comparison. Can be an integer or 'all'.
            weight_type (str): 'default' or 'custom'.
            user_type (str, optional): "Lender" or "Investor". Required if weight_type is 'default'.
            custom_weights (dict, optional): A dictionary of custom weights. Required if weight_type is 'custom'.

        Returns:
            tuple: A tuple containing:
                - dict | None: The final weighted overall score (raw and percentage) (if specific year) or
                               a dictionary of overall weighted scores by year (if 'all' years), or None.
                - dict: The dictionary of weights that were applied.
                - dict: A detailed breakdown of the calculation per category.
                - str | dict: The interpretation of the overall score (string for specific year, dict for 'all' years).
        """
        is_all_years = (str(year).lower() == 'all')

        category_scores_data = ratio_comparison_service_instance.compare_financial_ratios(
            entity_type=entity_type,
            sector=sector,
            sub_sector=sub_sector,
            org_name=org_name,
            year=year
        )

        detailed_breakdown = {}
        overall_score_interpretation = "N/A" # Default interpretation

        if not category_scores_data:
            print("Failed to retrieve category scores from ratio comparison. Cannot calculate overall score.")
            return None, {}, detailed_breakdown, overall_score_interpretation

        weights = {}
        if weight_type.lower() == 'default':
            if not user_type:
                print("Error: 'user_type' is required for 'default' weight calculation.")
                return None, {}, detailed_breakdown, overall_score_interpretation
            weights = self._get_default_weights(entity_type, user_type)
        elif weight_type.lower() == 'custom':
            if not custom_weights or not isinstance(custom_weights, dict):
                print("Error: 'custom_weights' (a dictionary) is required for 'custom' weight calculation.")
                return None, {}, detailed_breakdown, overall_score_interpretation
            
            total_custom_weight = sum(custom_weights.values())
            if not (0.99 <= total_custom_weight <= 1.01):
                print(f"Error: Custom weights do not sum to 1.0 (Sum: {total_custom_weight:.2f}).")
                return None, {}, detailed_breakdown, overall_score_interpretation
            
            # Use "Lender" as a fallback user_type for default_categories_ref if user_type is not provided for custom weights
            default_categories_ref = self._get_default_weights(entity_type, user_type if user_type else "Lender").keys() 
            for category in custom_weights.keys():
                if category not in default_categories_ref:
                    print(f"Warning: Custom weight provided for non-applicable category: '{category}'. It will be ignored.")
            
            weights = custom_weights
        else:
            print(f"Error: Invalid 'weight_type' '{weight_type}'. Must be 'default' or 'custom'.")
            return None, {}, detailed_breakdown, overall_score_interpretation

        if not weights:
            print(f"No weights defined or provided for entity '{entity_type}' and chosen weight type.")
            return None, {}, detailed_breakdown, overall_score_interpretation

        overall_score_result = None

        MAX_SCORE = 5.0 # Define the maximum possible score for percentage calculation

        if is_all_years:
            overall_scores_by_year = {}
            interpretations_by_year = {} # To store interpretation for each year
            all_years = set()
            for category, data in category_scores_data.items():
                avg_scores_for_category = data.get("Average Category Score")
                if isinstance(avg_scores_for_category, dict):
                    all_years.update(avg_scores_for_category.keys())
            
            for y in sorted(list(all_years)):
                current_year_total_score = 0
                valid_weights_sum = 0
                
                current_year_breakdown_for_this_year = {} # Temp dict for breakdown for THIS specific year

                for category, weight in weights.items():
                    category_data = category_scores_data.get(category, {})
                    avg_scores_for_category = category_data.get("Average Category Score")

                    category_avg_score = None
                    weighted_contribution = None

                    if isinstance(avg_scores_for_category, dict):
                        category_avg_score = avg_scores_for_category.get(y)
                        
                        if category_avg_score is not None:
                            weighted_contribution = category_avg_score * weight
                            current_year_total_score += weighted_contribution
                            valid_weights_sum += weight
                    
                    current_year_breakdown_for_this_year[category] = {
                        "Average Category Score": category_avg_score,
                        "Weight Applied": weight,
                        "Weighted Contribution": weighted_contribution
                    }
                
                if valid_weights_sum > 0:
                    calculated_overall_for_year = current_year_total_score / valid_weights_sum
                    percentage_for_year = (calculated_overall_for_year / MAX_SCORE) * 100
                    overall_scores_by_year[y] = {
                        "raw_score": calculated_overall_for_year,
                        "percentage_score": percentage_for_year
                    }
                    interpretations_by_year[y] = self._get_score_interpretation(calculated_overall_for_year)
                else:
                    overall_scores_by_year[y] = {
                        "raw_score": None,
                        "percentage_score": None
                    }
                    interpretations_by_year[y] = self._get_score_interpretation(None) # Pass None for N/A interpretation
                
                # Store the detailed breakdown for this specific year within the overall breakdown structure
                for cat_name, cat_data in current_year_breakdown_for_this_year.items():
                    if cat_name not in detailed_breakdown:
                        detailed_breakdown[cat_name] = {"Breakdown By Year": {}}
                    detailed_breakdown[cat_name]["Breakdown By Year"][y] = cat_data

            overall_score_result = overall_scores_by_year
            overall_score_interpretation = interpretations_by_year # Store the dict of interpretations

        else: # Specific year
            final_overall_score = 0
            valid_weights_sum = 0 

            for category, weight in weights.items():
                avg_score = category_scores_data.get(category, {}).get("Average Category Score")
                
                weighted_contribution = None
                if avg_score is not None:
                    weighted_contribution = avg_score * weight
                    final_overall_score += weighted_contribution
                    valid_weights_sum += weight
                
                detailed_breakdown[category] = {
                    "Average Category Score": avg_score,
                    "Weight Applied": weight,
                    "Weighted Contribution": weighted_contribution
                }
            
            if valid_weights_sum > 0:
                calculated_overall_score = final_overall_score / valid_weights_sum
                percentage_score = (calculated_overall_score / MAX_SCORE) * 100
                overall_score_result = {
                    "raw_score": calculated_overall_score,
                    "percentage_score": percentage_score
                }
                overall_score_interpretation = self._get_score_interpretation(calculated_overall_score)
            else:
                overall_score_result = {
                    "raw_score": None,
                    "percentage_score": None
                }
                overall_score_interpretation = self._get_score_interpretation(None)

        return overall_score_result, weights, detailed_breakdown, overall_score_interpretation

# Instantiate the service for use in views
overall_score_service_instance = OverallScoreService()