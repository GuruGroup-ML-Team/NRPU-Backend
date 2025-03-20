from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import pandas as pd
import numpy as np

class GeneralizedMethodOfMoment(APIView):
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        try:
            self.df = pd.read_excel("Data/gmm_signed.xlsx")
            self.sector_avg_df = pd.read_excel("Data/gmm_sector_averages_signed.xlsx")
            print("GMM dataset and sector averages loaded successfully.")
        except Exception as e:
            print(f"Error loading datasets: {str(e)}")
            self.df = pd.DataFrame()
            self.sector_avg_df = pd.DataFrame()

    def calculate_gmm_score(self, df_filtered):
        print("Inside calculate_gmm_score method")

        
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

        for _, row in df_filtered.iterrows():
            year = row['Year']
            components = {key: None for _, key in gmm_components.values()}

            for col_name, (category, key) in gmm_components.items():
                if category in df_filtered.columns:
                    components[key] = row[category]

            print(f"Components for year {year}: {components}")

            
            required_components = ['PS', 'log_GDP', 'BM', 'log_CD', 'log_OFA', 'log_IMP', 'log_TE', 'log_FS', 'log_GO2', 'AZ_L1_log']
            
            if not all(components.get(comp) is not None for comp in required_components):
                missing = [comp for comp in required_components if components.get(comp) is None]
                print(f"Missing components for year {year}: {missing}")
                gmm_scores[year] = "Insufficient data"
                continue
                
            try:
                gmm_score = (
                    3.876022 +
                    0.1441676 * components['AZ_L1_log'] +
                    0.0486955 * components['PS'] -
                    0.1198662 * components['log_GDP'] -
                    0.0079648 * components['BM'] +
                    0.035262 * components['log_CD'] -
                    0.09469 * components['log_OFA'] -
                    0.0111375 * components['log_IMP'] +
                    0.0011545 * components['log_TE'] -
                    0.0928376 * components['log_FS'] +
                    0.091969 * components['log_GO2']
                )
                
                gmm_scores[year] = gmm_score
                print(f"Calculated GMM Score for {year}: {gmm_score}")
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

            # if sector and sector.lower() == "all":
            #     # Use the sector_avg_df directly
            #     filtered_df = self.sector_avg_df.copy()
                
            #     # We need all data, not just "Average" rows, to calculate proper sector-wide averages
            #     all_data = filtered_df.copy()
                
            #     # Filter by year if specified
            #     if year and year.lower() != "all":
            #         all_data = all_data[all_data['Year'].astype(str).str.contains(str(year))]
                
            #     # Group data by sector
            #     sector_groups = {}
                
            #     # First group all data by sector, sub-sector and year
            #     for sector_name, sector_data in all_data.groupby('Sector'):
            #         # Initialize sector structure if not exists
            #         if sector_name not in sector_groups:
            #             sector_groups[sector_name] = {
            #                 "sector": sector_name,
            #                 "sub_sectors": {},
            #                 "years": {}
            #             }
                    
            #         # Process each sub-sector within this sector
            #         for sub_sector_name, sub_sector_data in sector_data.groupby('Sub-Sector'):
            #             if sub_sector_name not in sector_groups[sector_name]["sub_sectors"]:
            #                 sector_groups[sector_name]["sub_sectors"][sub_sector_name] = {
            #                     "name": sub_sector_name,
            #                     "years": {}
            #                 }
                        
            #             # Calculate year-wise averages for each sub-sector
            #             for year_val, year_data in sub_sector_data.groupby('Year'):
            #                 # Skip rows with "Average" in org name - we'll calculate our own averages
            #                 non_average_data = year_data[~year_data['Org Name'].str.contains('Average', case=False, na=False)]
                            
            #                 if not non_average_data.empty:
            #                     # Calculate average GMM Score for this sub-sector and year
            #                     scores = non_average_data['GMM Score'].dropna()
            #                     if not scores.empty:
            #                         avg_score = scores.mean()
            #                         sector_groups[sector_name]["sub_sectors"][sub_sector_name]["years"][str(year_val)] = avg_score
                
            #     # Now calculate overall sector averages by combining sub-sector data
            #     for sector_name, sector_info in sector_groups.items():
            #         # For each year, combine all sub-sector averages
            #         all_years = set()
            #         for sub_sector_info in sector_info["sub_sectors"].values():
            #             all_years.update(sub_sector_info["years"].keys())
                    
            #         # Calculate sector-wide average for each year
            #         for year_str in all_years:
            #             # Collect all sub-sector scores for this year
            #             sub_sector_scores = []
            #             total_orgs = 0
                        
            #             for sub_sector_name, sub_sector_info in sector_info["sub_sectors"].items():
            #                 if year_str in sub_sector_info["years"]:
            #                     # Get the sub-sector's score for this year
            #                     sub_score = sub_sector_info["years"][year_str]
                                
            #                     # Count organizations in this sub-sector for this year
            #                     year_int = int(year_str)
            #                     orgs_in_subsector = len(all_data[
            #                         (all_data['Sector'] == sector_name) & 
            #                         (all_data['Sub-Sector'] == sub_sector_name) & 
            #                         (all_data['Year'] == year_int) &
            #                         (~all_data['Org Name'].str.contains('Average', case=False, na=False))
            #                     ])
                                
            #                     if not pd.isna(sub_score):
            #                         sub_sector_scores.append(sub_score * orgs_in_subsector)
            #                         total_orgs += orgs_in_subsector
                        
            #             # Calculate weighted average across all sub-sectors
            #             if total_orgs > 0 and sub_sector_scores:
            #                 sector_avg = sum(sub_sector_scores) / total_orgs
            #                 sector_groups[sector_name]["years"][year_str] = sector_avg
                
            #     # Convert the sector groups to a list of results
            #     results = []
            #     for sector_name, sector_info in sector_groups.items():
            #         # Create a sector entry with overall averages
            #         sector_entry = {
            #             "sector": sector_name,
            #             "org_name": "Sector Average",
            #             "years": sector_info["years"]
            #         }
                    
            #         # Add sub-sector details
            #         sub_sectors = []
            #         for sub_name, sub_info in sector_info["sub_sectors"].items():
            #             sub_sectors.append({
            #                 "sub_sector": sub_name,
            #                 "years": sub_info["years"]
            #             })
                    
            #         sector_entry["sub_sectors"] = sub_sectors
            #         results.append(sector_entry)
                
            #     # Handle NaN values before returning
            #     results = self.replace_nan(results)
                
            #     return Response(
            #         {
            #             "sector": "All",
            #             "year": year if year else "all",
            #             "gmm_scores": results
            #         },
            #         status=status.HTTP_200_OK
            #     )
            
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
                            gmm_score = row['GMM Score']
                            if not pd.isna(gmm_score):
                                sector_groups[sector_name]["sub_sectors"][sub_sector_name]["years"][year_str] = gmm_score
                
                # Calculate overall sector averages by summing sub-sector averages and dividing by total orgs
                for sector_name, sector_info in sector_groups.items():
                    for year_str in [str(yr) for yr in all_possible_years]:
                        valid_subsectors = []
                        for sub_sector_info in sector_info["sub_sectors"].values():
                            if sub_sector_info["years"][year_str] is not None:
                                valid_subsectors.append(sub_sector_info)
                        
                        if valid_subsectors:
                            if len(valid_subsectors) > 1:
                                sum_of_averages = sum(sub["years"][year_str] for sub in valid_subsectors)
                                # Divide by total organizations in the sector
                                if sector_info["total_organizations"] > 0:
                                    sector_avg = sum_of_averages / sector_info["total_organizations"]
                                    sector_groups[sector_name]["years"][year_str] = sector_avg
                            else:
                                # For sectors with only one sub-sector, use the sub-sector average directly
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