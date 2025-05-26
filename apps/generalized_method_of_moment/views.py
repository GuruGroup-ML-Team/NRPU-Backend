# from rest_framework.views import APIView
# from rest_framework.response import Response
# from rest_framework import status
# import pandas as pd
# import numpy as np
# import math

# class GeneralizedMethodOfMoment(APIView):
    
#     def __init__(self, **kwargs):
#         super().__init__(**kwargs)
#         try:
#             self.df = pd.read_excel("Data/gmm.xlsx")
#             self.sector_avg_df = pd.read_excel("Data/gmm_sector_averages.xlsx")
#             print("GMM dataset and sector averages loaded successfully.")
#         except Exception as e:
#             print(f"Error loading datasets: {str(e)}")
#             self.df = pd.DataFrame()
#             self.sector_avg_df = pd.DataFrame()

#     def calculate_gmm_score(self, df_filtered):
#         print("Inside calculate_gmm_score method")

#         # Define the mapping of column names to their keys
#         gmm_components = {
#             'Political Stability': ('Political Stability', 'PS'),
#             'Log_GDP per capita (current US$)': ('Log_GDP per capita (current US$)', 'log_GDP'),
#             'Broad money (% of GDP)': ('Broad money (% of GDP)', 'BM'),
#             'Log_Firm Size': ('Log_Firm Size', 'log_FS'),
#             'Log_Growth Opportunities 2': ('Log_Growth Opportunities 2', 'log_GO2'),
#             'Log_Cash Dividends': ('Log_Cash Dividends', 'log_CD'),
#             'Log_Interest / Markup Payables': ('Log_Interest / Markup Payables', 'log_IMP'),
#             'Log_Operating Fixed Assets': ('Log_Operating Fixed Assets', 'log_OFA'),
#             'Log_Tax Expenses': ('Log_Tax Expenses', 'log_TE'),
#             'AltmanZscore_Lag1 of Log': ('AltmanZscore_Lag1 of Log', 'AZ_L1_log')
#         }

#         gmm_scores = {}
#         # Iterate through each row in the filtered DataFrame
#         for _, row in df_filtered.iterrows():
#             year = row['Year']
#             components = {key: None for _, key in gmm_components.values()}
#             # Extract relevant components for calculation
#             for col_name, (category, key) in gmm_components.items():
#                 if category in df_filtered.columns:
#                     components[key] = row[category]

#             print(f"Components for year {year}: {components}")

#             # Required components for GMM Score Calculation
#             required_components = ['PS', 'log_GDP', 'BM', 'log_CD', 'log_OFA', 'log_IMP', 'log_TE', 'log_FS', 'log_GO2', 'AZ_L1_log']
#             # Check if all required components are available
#             if not all(components.get(comp) is not None for comp in required_components):
#                 missing = [comp for comp in required_components if components.get(comp) is None]
#                 print(f"Missing components for year {year}: {missing}")
#                 gmm_scores[year] = "Insufficient data"
#                 continue
                
#             try:
#                 # Compute the GMM score using the formula
#                 gmm_score = (
#                     4.437 +
#                     0.103 * components['AZ_L1_log'] +
#                     0.038 * components['PS'] -
#                     0.185 * components['log_GDP'] -
#                     0.008 * components['BM'] +
#                     0.064 * components['log_CD'] +
#                     0.048 * components['log_OFA'] -
#                     0.0111 * components['log_IMP'] +
#                     0.031 * components['log_TE'] -
#                     0.194 * components['log_FS'] +
#                     0.085 * components['log_GO2']
#                 )
                
#                 gmm_scores[year] = math.exp(gmm_score)
#                 print(f"Calculated GMM Score for {year}: {gmm_score}, Antilog: {math.exp(gmm_score)}")
#             except Exception as e:
#                 print(f"Error in calculating GMM Score for year {year}: {str(e)}")
#                 gmm_scores[year] = f"Error: {str(e)}"

#         return gmm_scores
    
#     # Helper function to handle NaN values in data
#     def replace_nan(self, data):
#         """Replace NaN values with None for JSON serialization"""
#         if isinstance(data, dict):
#             return {k: self.replace_nan(v) for k, v in data.items()}
#         elif isinstance(data, list):
#             return [self.replace_nan(item) for item in data]
#         elif isinstance(data, float) and np.isnan(data):
#             return None
#         elif pd.isna(data):
#             return None
#         return data
        
#     def get(self, request):
#         try:
#             sector = request.query_params.get('sector', None)
#             sub_sector = request.query_params.get('sub_sector', None)
#             org_name = request.query_params.get('org_name', None)
#             year = request.query_params.get('year', None)
#             # Check if 'All' is requested for organization name
#             if org_name and org_name.lower() == "all":
#                 try:
#                     # Get data from gmm_sector_averages.xlsx where Org Name contains "Average"
#                     average_data = self.sector_avg_df[self.sector_avg_df['Org Name'].str.contains('Average', case=False, na=False)]
                    
#                     if sector and sector.lower() != "all":
#                         average_data = average_data[average_data['Sector'] == sector]
                    
#                     if sub_sector and sub_sector.lower() != "all":
#                         average_data = average_data[average_data['Sub-Sector'] == sub_sector]
                    
#                     if average_data.empty:
#                         return Response({"message": "No average data found matching the specified criteria."}, 
#                                         status=status.HTTP_404_NOT_FOUND)
#                     # If a specific year is requested, filter data accordingly
#                     if year and year.lower() != "all":
#                         year_data = average_data[average_data['Year'] == int(year)]
                        
#                         if year_data.empty:
#                             return Response({"message": f"No data found for the year {year}."},
#                                         status=status.HTTP_404_NOT_FOUND)
                                
#                         result_value = year_data['GMM Score'].iloc[0]
#                         if pd.isna(result_value):
#                             result_value = None
                                
#                         return Response({
#                             "sector": sector,
#                             "sub_sector": sub_sector,
#                             "org_name": "All",
#                             "year": year,
#                             "gmm_score": result_value
#                         }, status=status.HTTP_200_OK)
#                     else:
#                         result_dict = {}
#                         for _, row in average_data.iterrows():
#                             year_val = row['Year']
#                             score_val = row['GMM Score']
#                             if pd.isna(score_val):
#                                 score_val = None
#                             result_dict[year_val] = score_val
                                
#                         return Response({
#                             "sector": sector,
#                             "sub_sector": sub_sector,
#                             "org_name": "All",
#                             "year": "all",
#                             "gmm_score": result_dict
#                         }, status=status.HTTP_200_OK)
#                 except Exception as e:
#                     print(f"Error processing average data: {str(e)}")
#                     return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

#             if sector and sector.lower() == "all":
#                 filtered_df = self.sector_avg_df.copy()
#                 all_possible_years = sorted(filtered_df['Year'].unique())
#                 sector_groups = {}
                
#                 subsector_averages = filtered_df[filtered_df['Org Name'].str.contains('Average', case=False, na=False)]
                
#                 regular_orgs = filtered_df[~filtered_df['Org Name'].str.contains('Average', case=False, na=False)]
                
#                 # Process sector by sector
#                 for sector_name, sector_data in regular_orgs.groupby('Sector'):
#                     if sector_name not in sector_groups:
#                         sector_groups[sector_name] = {
#                             "sector": sector_name,
#                             "sub_sectors": {},
#                             "years": {str(yr): None for yr in all_possible_years},
#                             "total_organizations": len(sector_data['Org Name'].unique())
#                         }
                    
#                     # Process each sub-sector within this sector
#                     for sub_sector_name, sub_sector_data in sector_data.groupby('Sub-Sector'):
#                         total_orgs_in_subsector = len(sub_sector_data['Org Name'].unique())
                        
#                         if sub_sector_name not in sector_groups[sector_name]["sub_sectors"]:
#                             sector_groups[sector_name]["sub_sectors"][sub_sector_name] = {
#                                 "sub_sector": sub_sector_name,
#                                 "years": {str(yr): None for yr in all_possible_years},
#                                 "total_organizations": total_orgs_in_subsector
#                             }
                        
#                         # Get the pre-calculated averages for this sub-sector
#                         sub_avg_data = subsector_averages[
#                             (subsector_averages['Sector'] == sector_name) & 
#                             (subsector_averages['Sub-Sector'] == sub_sector_name)
#                         ]
                        
#                         for _, row in sub_avg_data.iterrows():
#                             year_str = str(row['Year'])
#                             # gmm_score = row['GMM Score']
#                             gmm_score = row['GMM Score']
#                             try:
#                                 gmm_score = float(gmm_score)
#                             except (ValueError, TypeError):
#                                 gmm_score = None

#                             if not pd.isna(gmm_score):
#                                 sector_groups[sector_name]["sub_sectors"][sub_sector_name]["years"][year_str] = gmm_score
                
#                 # Calculate overall sector averages by summing sub-sector averages and dividing by total orgs
#                 # for sector_name, sector_info in sector_groups.items():
#                 #     for year_str in [str(yr) for yr in all_possible_years]:
#                 #         valid_subsectors = []
#                 #         for sub_sector_info in sector_info["sub_sectors"].values():
#                 #             if sub_sector_info["years"][year_str] is not None:
#                 #                 valid_subsectors.append(sub_sector_info)
                        
#                 #         if valid_subsectors:
#                 #             if len(valid_subsectors) > 1:
#                 #                 sum_of_averages = sum(sub["years"][year_str] for sub in valid_subsectors)
#                 #                 # Divide by total organizations in the sector
#                 #                 if sector_info["total_organizations"] > 0:
#                 #                     sector_avg = sum_of_averages / sector_info["total_organizations"]
#                 #                     sector_groups[sector_name]["years"][year_str] = sector_avg
#                 #             else:
#                 #                 # For sectors with only one sub-sector, use the sub-sector average directly
#                 #                 sector_groups[sector_name]["years"][year_str] = valid_subsectors[0]["years"][year_str]

#                 for sector_name, sector_info in sector_groups.items():
#                     for year_str in [str(yr) for yr in all_possible_years]:
#                         valid_subsectors = []
#                         for sub_sector_info in sector_info["sub_sectors"].values():
#                             if sub_sector_info["years"][year_str] is not None:
#                                 valid_subsectors.append(sub_sector_info)

#                         if valid_subsectors:
#                             if len(valid_subsectors) > 1:
#                                 year_total_sum = 0
#                                 available_orgs = 0

#                                 for sub in valid_subsectors:
#                                     gmm_score = sub["years"][year_str]
#                                     if isinstance(gmm_score, (int, float)) and not pd.isna(gmm_score):
#                                         sub_orgs = regular_orgs[
#                                             (regular_orgs['Sector'] == sector_name) &
#                                             (regular_orgs['Sub-Sector'] == sub["sub_sector"]) &
#                                             (regular_orgs['Year'].astype(str) == year_str)
#                                         ]
#                                         gmm_values = sub_orgs['GMM Score']
#                                         numeric_gmm = [g for g in gmm_values if isinstance(g, (int, float)) and not pd.isna(g)]
#                                         valid_org_count = len(numeric_gmm)

#                                         if valid_org_count > 0:
#                                             available_orgs += valid_org_count
#                                             partial_sum = gmm_score * valid_org_count
#                                             year_total_sum += partial_sum

#                                             print(f"Sector: {sector_name}, Sub-Sector: {sub['sub_sector']}, Year: {year_str}, GMM Score: {gmm_score}, Valid Orgs: {valid_org_count}, Partial Sum: {partial_sum}")

#                                 if available_orgs > 0:
#                                     sector_avg = year_total_sum / available_orgs
#                                     sector_groups[sector_name]["years"][year_str] = sector_avg
#                                     print(f"[FINAL] Sector: {sector_name}, Year: {year_str}, Sector Avg GMM Score: {sector_avg}, Total Valid Orgs: {available_orgs}")

#                             else:
#                                 sector_groups[sector_name]["years"][year_str] = valid_subsectors[0]["years"][year_str]

                                

#                 results = []
#                 for sector_name, sector_info in sector_groups.items():
#                     sector_entry = {
#                         "sector": sector_name,
#                         "org_name": "Sector Average",
#                         "years": sector_info["years"],
#                         "total_organizations": sector_info["total_organizations"]
#                     }
                    
#                     sub_sectors = []
#                     for sub_name, sub_info in sector_info["sub_sectors"].items():
#                         sub_sectors.append({
#                             "sub_sector": sub_info["sub_sector"],
#                             "years": sub_info["years"],
#                             "total_organizations": sub_info["total_organizations"]
#                         })
                    
#                     sector_entry["sub_sectors"] = sub_sectors
#                     results.append(sector_entry)
                
#                 results = self.replace_nan(results)
                
#                 return Response(
#                     {
#                         "sector": "All",
#                         "year": year if year else "all",
#                         "gmm_scores": results
#                     },
#                     status=status.HTTP_200_OK
#                 )

#             filtered_df = self.df
            
#             if sector:
#                 filtered_df = filtered_df[filtered_df['Sector'] == sector]
#             if sub_sector:
#                 filtered_df = filtered_df[filtered_df['Sub-Sector'] == sub_sector]
#             if org_name:
#                 filtered_df = filtered_df[filtered_df['Org Name'] == org_name]

#             if filtered_df.empty:
#                 if org_name:
#                     print(f"Trying flexible match for org_name: {org_name}")
#                     matched_df = self.df[self.df['Org Name'].str.contains(org_name, case=False, na=False)]
#                     if not matched_df.empty:
#                         filtered_df = matched_df
#                         print(f"Found organization using flexible match: {matched_df['Org Name'].iloc[0]}")

#             if filtered_df.empty:
#                 return Response({"message": "No data found matching the specified criteria."}, 
#                                 status=status.HTTP_404_NOT_FOUND)

#             # Filter by year if specified
#             if year and year.lower() != "all":
#                 filtered_df = filtered_df[filtered_df['Year'] == int(year)]
#                 if filtered_df.empty:
#                     return Response({"message": f"No data found for the year {year}."}, 
#                                     status=status.HTTP_404_NOT_FOUND)

#             gmm_score = self.calculate_gmm_score(filtered_df)
#             gmm_score = self.replace_nan(gmm_score)

#             response_data = {
#                 "sector": sector,
#                 "sub_sector": sub_sector,
#                 "org_name": org_name,
#                 "year": year if year else "all",
#                 "gmm_score": gmm_score
#             }

#             return Response(response_data, status=status.HTTP_200_OK)

#         except Exception as e:
#             return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)





from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import pandas as pd
import numpy as np
import math

class GeneralizedMethodOfMoment(APIView):
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        try:
            self.df = pd.read_excel("Data/gmm.xlsx")
            self.sector_avg_df = pd.read_excel("Data/gmm_sector_averages.xlsx")
            print("GMM dataset and sector averages loaded successfully.")
        except Exception as e:
            print(f"Error loading datasets: {str(e)}")
            self.df = pd.DataFrame()
            self.sector_avg_df = pd.DataFrame()

    def calculate_gmm_score(self, df_filtered):
        print("Inside calculate_gmm_score method")

        # Define the mapping of column names to their keys
        gmm_components = {
            'Political Stability': ('Political Stability', 'PS'),
            'Log_GDP per capita (current US$)': ('Log_GDP per capita (current US$)', 'log_GDP'),
            'Broad money (% of GDP)': ('Broad money (% of GDP)', 'BM'),
            'Log_Firm Size': ('Log_Firm Size', 'log_FS'),
            'Log_Growth Opportunities 2': ('Log_Growth Opportunities 2', 'log_GO2'),
            'Log_Cash Dividends': ('Log_Cash Dividends', 'log_CD'),
            'Log_Interest / Markup Payables': ('Log_Interest / Markup Payables', 'log_IMP'),
            'Log_Operating Fixed Assets': ('Log_Operating Fixed Assets', 'log_OFA'),
            'Log_Tax Expenses': ('Log_Tax Expenses', 'log_TE'),
            'AltmanZscore_Lag1 of Log': ('AltmanZscore_Lag1 of Log', 'AZ_L1_log')
        }

        gmm_scores = {}
        # Iterate through each row in the filtered DataFrame
        for _, row in df_filtered.iterrows():
            year = row['Year']
            components = {key: None for _, key in gmm_components.values()}
            # Extract relevant components for calculation
            for col_name, (category, key) in gmm_components.items():
                if category in df_filtered.columns:
                    components[key] = row[category]

            print(f"Components for year {year}: {components}")

            # Required components for GMM Score Calculation
            required_components = ['PS', 'log_GDP', 'BM', 'log_CD', 'log_OFA', 'log_IMP', 'log_TE', 'log_FS', 'log_GO2', 'AZ_L1_log']
            # Check if all required components are available
            if not all(components.get(comp) is not None for comp in required_components):
                missing = [comp for comp in required_components if components.get(comp) is None]
                print(f"Missing components for year {year}: {missing}")
                gmm_scores[year] = "Insufficient data"
                continue
                
            try:
                # Compute the GMM score using the formula
                gmm_score = (
                    4.437 +
                    0.103 * components['AZ_L1_log'] +
                    0.038 * components['PS'] -
                    0.185 * components['log_GDP'] -
                    0.008 * components['BM'] +
                    0.064 * components['log_CD'] +
                    0.048 * components['log_OFA'] -
                    0.0111 * components['log_IMP'] +
                    0.031 * components['log_TE'] -
                    0.194 * components['log_FS'] +
                    0.085 * components['log_GO2']
                )
                
                gmm_scores[year] = math.exp(gmm_score)
                print(f"Calculated GMM Score for {year}: {gmm_score}, Antilog: {math.exp(gmm_score)}")
            except Exception as e:
                print(f"Error in calculating GMM Score for year {year}: {str(e)}")
                gmm_scores[year] = f"Error: {str(e)}"

        return gmm_scores
    
    # Helper function to handle NaN values in data
    def replace_nan(self, data):
        """Replace NaN values with None for JSON serialization"""
        if isinstance(data, dict):
            return {k: self.replace_nan(v) for k, v in data.items()}
        elif isinstance(data, list):
            return [self.replace_nan(item) for item in data]
        elif isinstance(data, float) and np.isnan(data):
            return None
        elif pd.isna(data):
            return None
        return data
        
    def get(self, request):
        try:
            sector = request.query_params.get('sector', None)
            sub_sector = request.query_params.get('sub_sector', None)
            org_name = request.query_params.get('org_name', None)
            year = request.query_params.get('year', None)

            # New Use Case: sector given, no sub_sector, org_name is "all"
            if sector and sector.lower() != "all" and not sub_sector and org_name and org_name.lower() == "all":
                print(f"Handling new use case: sector={sector}, sub_sector=None, org_name=All")
                # Filter self.df (the main GMM data) for the specified sector
                sector_filtered_df = self.df[self.df['Sector'] == sector].copy()

                if sector_filtered_df.empty:
                    return Response({"message": f"No data found for sector '{sector}' with all organizations."},
                                    status=status.HTTP_404_NOT_FOUND)

                # If a specific year is requested, filter data accordingly
                if year and year.lower() != "all":
                    try:
                        year_int = int(year)
                        sector_filtered_df = sector_filtered_df[sector_filtered_df['Year'] == year_int]
                        if sector_filtered_df.empty:
                            return Response({"message": f"No data found for sector '{sector}' for year {year_int} with all organizations."},
                                            status=status.HTTP_404_NOT_FOUND)
                    except ValueError:
                        return Response({"message": "Invalid year format. Please provide a valid integer year or 'all'."},
                                        status=status.HTTP_400_BAD_REQUEST)
                
                # Calculate GMM scores for all organizations in the sector, for the given year(s)
                # We need to group by Org Name and then calculate the GMM for each organization.
                # If 'year' is specific, the calculate_gmm_score will return a single score for that year.
                # If 'year' is 'all', it will return scores for all available years for each organization.
                
                results_by_org = {}
                for org_name_in_sector, org_df in sector_filtered_df.groupby('Org Name'):
                    gmm_scores_for_org = self.calculate_gmm_score(org_df)
                    gmm_scores_for_org = self.replace_nan(gmm_scores_for_org)
                    results_by_org[org_name_in_sector] = gmm_scores_for_org

                response_data = {
                    "sector": sector,
                    "sub_sector": None, # Explicitly None as per use case
                    "org_name": "All",
                    "year": year if year else "all",
                    "gmm_scores_by_organization": results_by_org
                }
                return Response(response_data, status=status.HTTP_200_OK)


            # Check if 'All' is requested for organization name (existing logic for sector averages)
            if org_name and org_name.lower() == "all":
                try:
                    # Get data from gmm_sector_averages.xlsx where Org Name contains "Average"
                    average_data = self.sector_avg_df[self.sector_avg_df['Org Name'].str.contains('Average', case=False, na=False)]
                    
                    if sector and sector.lower() != "all":
                        average_data = average_data[average_data['Sector'] == sector]
                    
                    if sub_sector and sub_sector.lower() != "all":
                        average_data = average_data[average_data['Sub-Sector'] == sub_sector]
                    
                    if average_data.empty:
                        return Response({"message": "No average data found matching the specified criteria."}, 
                                         status=status.HTTP_404_NOT_FOUND)
                    # If a specific year is requested, filter data accordingly
                    if year and year.lower() != "all":
                        year_data = average_data[average_data['Year'] == int(year)]
                        
                        if year_data.empty:
                            return Response({"message": f"No data found for the year {year}."},
                                             status=status.HTTP_404_NOT_FOUND)
                                        
                        result_value = year_data['GMM Score'].iloc[0]
                        if pd.isna(result_value):
                            result_value = None
                                        
                        return Response({
                            "sector": sector,
                            "sub_sector": sub_sector,
                            "org_name": "All",
                            "year": year,
                            "gmm_score": result_value
                        }, status=status.HTTP_200_OK)
                    else:
                        result_dict = {}
                        for _, row in average_data.iterrows():
                            year_val = row['Year']
                            score_val = row['GMM Score']
                            if pd.isna(score_val):
                                score_val = None
                            result_dict[year_val] = score_val
                                        
                        return Response({
                            "sector": sector,
                            "sub_sector": sub_sector,
                            "org_name": "All",
                            "year": "all",
                            "gmm_score": result_dict
                        }, status=status.HTTP_200_OK)
                except Exception as e:
                    print(f"Error processing average data: {str(e)}")
                    return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

            if sector and sector.lower() == "all":
                filtered_df = self.sector_avg_df.copy()
                all_possible_years = sorted(filtered_df['Year'].unique())
                sector_groups = {}
                
                subsector_averages = filtered_df[filtered_df['Org Name'].str.contains('Average', case=False, na=False)]
                
                regular_orgs = filtered_df[~filtered_df['Org Name'].str.contains('Average', case=False, na=False)]
                
                # Process sector by sector
                for sector_name, sector_data in regular_orgs.groupby('Sector'):
                    if sector_name not in sector_groups:
                        sector_groups[sector_name] = {
                            "sector": sector_name,
                            "sub_sectors": {},
                            "years": {str(yr): None for yr in all_possible_years},
                            "total_organizations": len(sector_data['Org Name'].unique())
                        }
                    
                    # Process each sub-sector within this sector
                    for sub_sector_name, sub_sector_data in sector_data.groupby('Sub-Sector'):
                        total_orgs_in_subsector = len(sub_sector_data['Org Name'].unique())
                        
                        if sub_sector_name not in sector_groups[sector_name]["sub_sectors"]:
                            sector_groups[sector_name]["sub_sectors"][sub_sector_name] = {
                                "sub_sector": sub_sector_name,
                                "years": {str(yr): None for yr in all_possible_years},
                                "total_organizations": total_orgs_in_subsector
                            }
                        
                        # Get the pre-calculated averages for this sub-sector
                        sub_avg_data = subsector_averages[
                            (subsector_averages['Sector'] == sector_name) & 
                            (subsector_averages['Sub-Sector'] == sub_sector_name)
                        ]
                        
                        for _, row in sub_avg_data.iterrows():
                            year_str = str(row['Year'])
                            # gmm_score = row['GMM Score']
                            gmm_score = row['GMM Score']
                            try:
                                gmm_score = float(gmm_score)
                            except (ValueError, TypeError):
                                gmm_score = None

                            if not pd.isna(gmm_score):
                                sector_groups[sector_name]["sub_sectors"][sub_sector_name]["years"][year_str] = gmm_score
                
                for sector_name, sector_info in sector_groups.items():
                    for year_str in [str(yr) for yr in all_possible_years]:
                        valid_subsectors = []
                        for sub_sector_info in sector_info["sub_sectors"].values():
                            if sub_sector_info["years"][year_str] is not None:
                                valid_subsectors.append(sub_sector_info)

                        if valid_subsectors:
                            if len(valid_subsectors) > 1:
                                year_total_sum = 0
                                available_orgs = 0

                                for sub in valid_subsectors:
                                    gmm_score = sub["years"][year_str]
                                    if isinstance(gmm_score, (int, float)) and not pd.isna(gmm_score):
                                        sub_orgs = regular_orgs[
                                            (regular_orgs['Sector'] == sector_name) &
                                            (regular_orgs['Sub-Sector'] == sub["sub_sector"]) &
                                            (regular_orgs['Year'].astype(str) == year_str)
                                        ]
                                        gmm_values = sub_orgs['GMM Score']
                                        numeric_gmm = [g for g in gmm_values if isinstance(g, (int, float)) and not pd.isna(g)]
                                        valid_org_count = len(numeric_gmm)

                                        if valid_org_count > 0:
                                            available_orgs += valid_org_count
                                            partial_sum = gmm_score * valid_org_count
                                            year_total_sum += partial_sum

                                            print(f"Sector: {sector_name}, Sub-Sector: {sub['sub_sector']}, Year: {year_str}, GMM Score: {gmm_score}, Valid Orgs: {valid_org_count}, Partial Sum: {partial_sum}")

                                if available_orgs > 0:
                                    sector_avg = year_total_sum / available_orgs
                                    sector_groups[sector_name]["years"][year_str] = sector_avg
                                    print(f"[FINAL] Sector: {sector_name}, Year: {year_str}, Sector Avg GMM Score: {sector_avg}, Total Valid Orgs: {available_orgs}")

                            else:
                                sector_groups[sector_name]["years"][year_str] = valid_subsectors[0]["years"][year_str]

                                
                results = []
                for sector_name, sector_info in sector_groups.items():
                    sector_entry = {
                        "sector": sector_name,
                        "org_name": "Sector Average",
                        "years": sector_info["years"],
                        "total_organizations": sector_info["total_organizations"]
                    }
                    
                    sub_sectors = []
                    for sub_name, sub_info in sector_info["sub_sectors"].items():
                        sub_sectors.append({
                            "sub_sector": sub_info["sub_sector"],
                            "years": sub_info["years"],
                            "total_organizations": sub_info["total_organizations"]
                        })
                    
                    sector_entry["sub_sectors"] = sub_sectors
                    results.append(sector_entry)
                
                results = self.replace_nan(results)
                
                return Response(
                    {
                        "sector": "All",
                        "year": year if year else "all",
                        "gmm_scores": results
                    },
                    status=status.HTTP_200_OK
                )

            filtered_df = self.df
            
            if sector:
                filtered_df = filtered_df[filtered_df['Sector'] == sector]
            if sub_sector:
                filtered_df = filtered_df[filtered_df['Sub-Sector'] == sub_sector]
            if org_name:
                filtered_df = filtered_df[filtered_df['Org Name'] == org_name]

            if filtered_df.empty:
                if org_name:
                    print(f"Trying flexible match for org_name: {org_name}")
                    matched_df = self.df[self.df['Org Name'].str.contains(org_name, case=False, na=False)]
                    if not matched_df.empty:
                        filtered_df = matched_df
                        print(f"Found organization using flexible match: {matched_df['Org Name'].iloc[0]}")

            if filtered_df.empty:
                return Response({"message": "No data found matching the specified criteria."}, 
                                 status=status.HTTP_404_NOT_FOUND)

            # Filter by year if specified
            if year and year.lower() != "all":
                filtered_df = filtered_df[filtered_df['Year'] == int(year)]
                if filtered_df.empty:
                    return Response({"message": f"No data found for the year {year}."}, 
                                     status=status.HTTP_404_NOT_FOUND)

            gmm_score = self.calculate_gmm_score(filtered_df)
            gmm_score = self.replace_nan(gmm_score)

            response_data = {
                "sector": sector,
                "sub_sector": sub_sector,
                "org_name": org_name,
                "year": year if year else "all",
                "gmm_score": gmm_score
            }

            return Response(response_data, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)