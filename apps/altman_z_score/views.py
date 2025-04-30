# from rest_framework.views import APIView
# from rest_framework.response import Response
# from rest_framework import status
# import pandas as pd
# import numpy as np

# class AltmanZScoreView(APIView):
    
#     def __init__(self, **kwargs):
#         super().__init__(**kwargs)
#         try:
#             self.df_pivot = pd.read_excel("Data/input_data.xlsx")
#             self.df_sector_avg = pd.read_excel("Data/altman_sector_averages.xlsx")  
#             print("Datasets loaded successfully.")
#         except Exception as e:
#             print(f"Error loading datasets: {str(e)}")
#             self.df_pivot = pd.DataFrame()
#             self.df_sector_avg = pd.DataFrame()

#     def calculate_altman_score(self, df_filtered):
#         print("Inside calculate_altman_score method")

#         zscore_components = {
#             '1. Capital work in progress': ('Sub Indicator', 'wc'),
#             'Total Assets (A+B) / Equity & Liabilities (C+D+E)': ('Sub Indicator', 'ta'),
#             'of which: un-appropriated profit(loss) / retained earnings': ('Sub-Sub Indicator', 're'),
#             '6. EBIT (F3-F4+F5)': ('Sub Indicator', 'ebit'),
#             "C. Shareholders' Equity (C1+C2+C3)": ('Indicator', 'mve'),
#             'D. Non-Current Liabilities (D1+D2+D3+D4+D5)': ('Indicator', 'tl_d'),
#             'E. Current Liabilities (E1+E2+E3+E4)': ('Indicator', 'tl_e')
#         }

#         # year_columns = [col for col in df_filtered.columns if col.isdigit()]
#         # year_columns = [str(col) for col in df_filtered.columns if str(col).isdigit()]

#         # altman_scores = {}

#         # for year in year_columns:
#         #     components = {key: None for _, key in zscore_components.values()}

#         #     for col_name, (category, key) in zscore_components.items():
#         #         row = df_filtered[df_filtered[category].str.strip().str.lower() == col_name.lower()]
#         #         if not row.empty:
#         #             components[key] = row.iloc[0][year]

#         #     print(f"Components for year {year}: {components}")
#                 # Get all numeric year columns - fix: Check for year pattern instead of just digits
#         year_columns = []
#         for col in df_filtered.columns:
#             if str(col).isdigit():
#                 year_columns.append(str(col))
#             elif isinstance(col, str) and col.startswith('AltmanZscore '):
#                 year_value = col.split(' ')[1]
#                 if year_value.isdigit():
#                     year_columns.append(year_value)

#         for col in df_filtered.columns:
#             if str(col).isdigit() and str(col) not in year_columns:
#                 year_columns.append(str(col))

#         print(f"Identified year columns: {year_columns}")
#         altman_scores = {}

#         for year in year_columns:
#             components = {key: None for _, key in zscore_components.values()}

#             for col_name, (category, key) in zscore_components.items():
#                 # Handle potential whitespace and case differences
#                 row = df_filtered[df_filtered[category].str.strip().str.lower() == col_name.lower()]
#                 if not row.empty:
#                     # Try to access the year column directly
#                     if year in row.columns:
#                         components[key] = row.iloc[0][year]
#                     # If not found, try with "AltmanZscore " prefix
#                     elif f"AltmanZscore {year}" in row.columns:
#                         components[key] = row.iloc[0][f"AltmanZscore {year}"]

#             print(f"Components for year {year}: {components}")
            
#             if not all(k in components and components[k] is not None for k in ['ta', 'tl_d', 'tl_e']):
#                 print(f"Missing critical components for year {year}")
#                 altman_scores[year] = "Insufficient data"
#                 continue
                
#             try:
#                 tl = (components.get('tl_d', 0) or 0) + (components.get('tl_e', 0) or 0)

#                 x1 = components.get('wc', 0) / components['ta'] if 'wc' in components else 0
#                 x2 = components.get('re', 0) / components['ta'] if 're' in components else 0
#                 x3 = components.get('ebit', 0) / components['ta'] if 'ebit' in components else 0
#                 x4 = components.get('mve', 0) / tl if 'mve' in components and tl > 0 else 0

#                 altman_zscore = 3.25 + (6.56 * x1) + (3.26 * x2) + (6.72 * x3) + (1.05 * x4)
#                 altman_scores[year] = altman_zscore
#                 print(f"Calculated Altman Z-Score for {year}: {altman_zscore}")
#             except Exception as e:
#                 print(f"Error in calculating Altman Z-Score for year {year}: {str(e)}")
#                 altman_scores[year] = f"Error: {str(e)}"

#         return altman_scores
    
#     def replace_nan(self, data):
#         """
#         Replace NaN values with None in a nested dictionary structure
#         """
#         if isinstance(data, dict):
#             return {k: self.replace_nan(v) for k, v in data.items()}
#         elif isinstance(data, list):
#             return [self.replace_nan(item) for item in data]
#         elif pd.isna(data):
#             return None
#         else:
#             return data
    
#     def get_sector_averages(self, sector, year):
#         """
#         Retrieve the sector-wise average Altman Z-Score for a specific year or all years.
#         """
#         try:
#             if sector and sector.lower() != "all":
#                 averages_df = self.df_sector_avg[self.df_sector_avg['Sector'] == sector]
#                 if averages_df.empty:
#                     #case-insensitive matching
#                     sector_match = self.df_sector_avg[self.df_sector_avg['Sector'].str.lower() == sector.lower()]
#                     if not sector_match.empty:
#                         averages_df = sector_match
#                         print(f"Found sector using case-insensitive match: {sector_match['Sector'].iloc[0]}")
#             else:
#                 averages_df = self.df_sector_avg

#             if averages_df.empty:
#                 print(f"No data found for sector: {sector}")
#                 return {"error": f"No data found for sector: {sector}"}
            
#             # Filter by year if specified
#             if year and year.lower() != "all":
#                 year_column = f"AltmanZscore {year}"
#                 if year_column not in self.df_sector_avg.columns:
#                     return {"error": f"Year {year} is not available in the dataset."}

#                 # Select only the relevant year column and average row
#                 averages_df = averages_df[averages_df['Org Name'] == 'Sector Average'][['Sector', year_column]]
#                 return averages_df.rename(columns={year_column: "AltmanZscore"}).to_dict(orient="records")
#             else:
#                 averages_df = averages_df[averages_df['Org Name'] == 'Sector Average']
#                 averages_df = averages_df.drop(columns=['Sub-Sector', 'Org Name'], errors='ignore')
#                 return averages_df.to_dict(orient="records")

#         except Exception as e:
#             print(f"Error retrieving sector averages: {str(e)}")
#             return {"error": str(e)}
#     def get(self, request):
#         try:
#             sector = request.query_params.get('sector', None)
#             sub_sector = request.query_params.get('sub_sector', None)
#             org_name = request.query_params.get('org_name', None)
#             year = request.query_params.get('year', None)

#             # Handle the case where org_name is "All"
#             if org_name and org_name.lower() == "all":
#                 try:
#                     # Get rows where Org Name contains "Average"
#                     average_data = self.df_sector_avg[self.df_sector_avg['Org Name'].str.contains('Average', case=False, na=False)]
                    
#                     if sector and sector.lower() != "all":
#                         average_data = average_data[average_data['Sector'] == sector]
                    
#                     if sub_sector:
#                         average_data = average_data[average_data['Sub-Sector'] == sub_sector]
                    
#                     if average_data.empty:
#                         return Response({"message": "No average data found matching the specified criteria."}, 
#                                         status=status.HTTP_404_NOT_FOUND)
                    
#                     if year and year.lower() != "all":
#                         year_column = f"AltmanZscore {year}"
#                         if year_column not in average_data.columns:
#                             return Response({"message": f"No data found for the year {year}."},
#                                         status=status.HTTP_404_NOT_FOUND)
                                
#                         result_value = average_data[year_column].iloc[0]
                                
#                         return Response({
#                             "sector": sector,
#                             "sub_sector": sub_sector,
#                             "org_name": "All",
#                             "year": year,
#                             "altman_zscore": result_value
#                         }, status=status.HTTP_200_OK)
#                     else:
#                         year_columns = [col for col in average_data.columns if col.startswith('AltmanZscore')]
                                
#                         result_dict = {}
#                         for col in year_columns:
#                             year_value = col.split(' ')[1]  
#                             result_dict[year_value] = average_data[col].iloc[0]
                                
#                         return Response({
#                             "sector": sector,
#                             "sub_sector": sub_sector,
#                             "org_name": "All",
#                             "year": "all",
#                             "altman_zscore": result_dict
#                         }, status=status.HTTP_200_OK)
#                 except Exception as e:
#                     print(f"Error processing average data: {str(e)}")
#                     return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

#             if sector and sector.lower() == "all":
#                 filtered_df = self.df_sector_avg.copy()
#                 all_possible_years = []
                
#                 # Extract all year columns from the data
#                 for col in filtered_df.columns:
#                     if col.startswith('AltmanZscore '):
#                         year_value = col.split(' ')[1]
#                         all_possible_years.append(year_value)
#                 all_possible_years = sorted(all_possible_years)
                
#                 sector_groups = {}
                
#                 # Get subsector averages and  organizations
#                 subsector_averages = filtered_df[filtered_df['Org Name'].str.contains('Average', case=False, na=False)]
#                 regular_orgs = filtered_df[~filtered_df['Org Name'].str.contains('Average', case=False, na=False)]
                
#                 # Process sector by sector
#                 for sector_name, sector_data in regular_orgs.groupby('Sector'):
#                     if sector_name not in sector_groups:
#                         sector_groups[sector_name] = {
#                             "sector": sector_name,
#                             "sub_sectors": {},
#                             "years": {yr: None for yr in all_possible_years},
#                             "total_organizations": len(sector_data['Org Name'].unique())
#                         }
                    
#                     # Process each sub-sector within this sector
#                     for sub_sector_name, sub_sector_data in sector_data.groupby('Sub-Sector'):
#                         total_orgs_in_subsector = len(sub_sector_data['Org Name'].unique())
                        
#                         if sub_sector_name not in sector_groups[sector_name]["sub_sectors"]:
#                             sector_groups[sector_name]["sub_sectors"][sub_sector_name] = {
#                                 "sub_sector": sub_sector_name,
#                                 "years": {yr: None for yr in all_possible_years},
#                                 "total_organizations": total_orgs_in_subsector
#                             }
                        
#                         # Get the pre-calculated averages for this sub-sector
#                         sub_avg_data = subsector_averages[
#                             (subsector_averages['Sector'] == sector_name) & 
#                             (subsector_averages['Sub-Sector'] == sub_sector_name)
#                         ]
                        
#                         for _, row in sub_avg_data.iterrows():
#                             for yr in all_possible_years:
#                                 year_col = f"AltmanZscore {yr}"
#                                 if year_col in row.index and not pd.isna(row[year_col]):
#                                     sector_groups[sector_name]["sub_sectors"][sub_sector_name]["years"][yr] = row[year_col]
            
#                 # Calculate overall sector averages by summing sub-sector averages and dividing by total orgs
#                 for sector_name, sector_info in sector_groups.items():
#                     for year_str in all_possible_years:
#                         valid_subsectors = []
#                         for sub_sector_info in sector_info["sub_sectors"].values():
#                             if sub_sector_info["years"][year_str] is not None:
#                                 valid_subsectors.append(sub_sector_info)
                        
#                         if valid_subsectors:
#                             if len(valid_subsectors) > 1:
#                                 sum_of_averages = sum(sub["years"][year_str] for sub in valid_subsectors)
#                                 if sector_info["total_organizations"] > 0:
#                                     sector_avg = sum_of_averages / sector_info["total_organizations"]
#                                     sector_groups[sector_name]["years"][year_str] = sector_avg
#                             else:
#                                 # For sectors with only one sub-sector, use the sub-sector average directly
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
#                         "altman_zscores": results
#                     },
#                     status=status.HTTP_200_OK
#                 )
            
#             predefined_sub_indicators = [
#                 '    1. Capital work in progress',
#                 ' Total Assets (A+B) / Equity & Liabilities (C+D+E)',
#                 '         of which: un-appropriated profit(loss) / retained earnings',
#                 '    6. EBIT (F3-F4+F5)',
#                 "C. Shareholders' Equity (C1+C2+C3)",
#                 'D. Non-Current Liabilities (D1+D2+D3+D4+D5)',
#                 'E. Current Liabilities (E1+E2+E3+E4)'
#             ]

#             filtered_df = self.df_pivot
            
#             if sector:
#                 filtered_df = filtered_df[filtered_df['Sector'] == sector]
#             if sub_sector:
#                 filtered_df = filtered_df[filtered_df['Sub-Sector'] == sub_sector]
#             if org_name:
#                 filtered_df = filtered_df[filtered_df['Org Name'] == org_name]

#             if filtered_df.empty:
#                 if org_name:
#                     print(f"Trying flexible match for org_name: {org_name}")
#                     matched_df = self.df_pivot[self.df_pivot['Org Name'].str.contains(org_name, case=False, na=False)]
#                     if not matched_df.empty:
#                         filtered_df = matched_df
#                         print(f"Found organization using flexible match: {matched_df['Org Name'].iloc[0]}")

#             if filtered_df.empty:
#                 return Response({"message": "No data found matching the specified criteria."}, 
#                                 status=status.HTTP_404_NOT_FOUND)

#             filtered_df = filtered_df[
#                 (filtered_df['Sub Indicator'].isin(predefined_sub_indicators)) |
#                 (filtered_df['Indicator'].isin(predefined_sub_indicators)) |
#                 (filtered_df['Sub-Sub Indicator'].isin(predefined_sub_indicators))
#             ]
            
#             print(f"Filtered data shape after indicator matching: {filtered_df.shape}")
            
#             filtered_df = filtered_df.drop_duplicates(subset=['Indicator', 'Sub Indicator', 'Sub-Sub Indicator'], keep='first')

#             if year and year.lower() != "all":
#                 if year not in filtered_df.columns:
#                     return Response({"message": f"No data found for the year {year}."}, 
#                                     status=status.HTTP_404_NOT_FOUND)
                                    
#                 filtered_df = filtered_df[['Sector', 'Sub-Sector', 'Org Name', 'Indicator', 'Sub Indicator', 'Sub-Sub Indicator', year]]
                
#                 # Before passing filtered data to Altman calculation
#                 print(f"\nFiltered DataFrame for {org_name} ({year}):")
#                 print(filtered_df[['Indicator', 'Sub Indicator', 'Sub-Sub Indicator', year]])

#                 altman_zscore = self.calculate_altman_score(filtered_df)
#                 response_data = {
#                     "sector": sector,
#                     "sub_sector": sub_sector,
#                     "org_name": org_name,
#                     "year": year,
#                     "altman_zscore": altman_zscore.get(year, "Insufficient data or error in calculation")
#                 }
#             else:
#                 altman_zscore = self.calculate_altman_score(filtered_df)
#                 response_data = {
#                     "sector": sector,
#                     "sub_sector": sub_sector,
#                     "org_name": org_name,
#                     "year": "all",
#                     "altman_zscore": altman_zscore
#                 }

#             return Response(response_data, status=status.HTTP_200_OK)

#         except Exception as e:
#             return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
















































from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import pandas as pd
import numpy as np

class AltmanZScoreView(APIView):
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        try:
            self.df_pivot = pd.read_excel("Data/input_data.xlsx")
            self.df_sector_avg = pd.read_excel("Data/altman_sector_averages.xlsx")  
            print("Datasets loaded successfully.")
        except Exception as e:
            print(f"Error loading datasets: {str(e)}")
            self.df_pivot = pd.DataFrame()
            self.df_sector_avg = pd.DataFrame()

    def calculate_altman_score(self, df_filtered):
        print("Inside calculate_altman_score method")

        zscore_components = {
            '1. Capital work in progress': ('Sub Indicator', 'wc'),
            'Total Assets (A+B) / Equity & Liabilities (C+D+E)': ('Sub Indicator', 'ta'),
            'of which: un-appropriated profit(loss) / retained earnings': ('Sub-Sub Indicator', 're'),
            '6. EBIT (F3-F4+F5)': ('Sub Indicator', 'ebit'),
            "C. Shareholders' Equity (C1+C2+C3)": ('Indicator', 'mve'),
            'D. Non-Current Liabilities (D1+D2+D3+D4+D5)': ('Indicator', 'tl_d'),
            'E. Current Liabilities (E1+E2+E3+E4)': ('Indicator', 'tl_e')
        }

        # year_columns = [col for col in df_filtered.columns if col.isdigit()]
        # year_columns = [str(col) for col in df_filtered.columns if str(col).isdigit()]

        # altman_scores = {}

        # for year in year_columns:
        #     components = {key: None for _, key in zscore_components.values()}

        #     for col_name, (category, key) in zscore_components.items():
        #         row = df_filtered[df_filtered[category].str.strip().str.lower() == col_name.lower()]
        #         if not row.empty:
        #             components[key] = row.iloc[0][year]

        #     print(f"Components for year {year}: {components}")
                # Get all numeric year columns - fix: Check for year pattern instead of just digits
        year_columns = []
        for col in df_filtered.columns:
            if str(col).isdigit():
                year_columns.append(str(col))
            elif isinstance(col, str) and col.startswith('AltmanZscore '):
                year_value = col.split(' ')[1]
                if year_value.isdigit():
                    year_columns.append(year_value)
            print(year_columns)

        for col in df_filtered.columns:
            if str(col).isdigit() and str(col) not in year_columns:
                year_columns.append(str(col))
            print(year_columns)

        print(f"Identified year columns: {year_columns}")
        altman_scores = {}

        for year in year_columns:
            components = {key: None for _, key in zscore_components.values()}

            for col_name, (category, key) in zscore_components.items():
                # Handle potential whitespace and case differences
                row = df_filtered[df_filtered[category].str.strip().str.lower() == col_name.lower()]
                if not row.empty:
                    # Try to access the year column directly
                    if year in row.columns:
                        components[key] = row.iloc[0][year]
                    # If not found, try with "AltmanZscore " prefix
                    elif f"AltmanZscore {year}" in row.columns:
                        components[key] = row.iloc[0][f"AltmanZscore {year}"]

            print(f"Components for year {year}: {components}")
            
            if not all(k in components and components[k] is not None for k in ['ta', 'tl_d', 'tl_e']):
                print(f"Missing critical components for year {year}")
                altman_scores[year] = "Insufficient data"
                continue
                
            try:
                tl = (components.get('tl_d', 0) or 0) + (components.get('tl_e', 0) or 0)

                x1 = components.get('wc', 0) / components['ta'] if 'wc' in components else 0
                x2 = components.get('re', 0) / components['ta'] if 're' in components else 0
                x3 = components.get('ebit', 0) / components['ta'] if 'ebit' in components else 0
                x4 = components.get('mve', 0) / tl if 'mve' in components and tl > 0 else 0

                altman_zscore = 3.25 + (6.56 * x1) + (3.26 * x2) + (6.72 * x3) + (1.05 * x4)
                altman_scores[year] = altman_zscore
                print(f"Calculated Altman Z-Score for {year}: {altman_zscore}")
            except Exception as e:
                print(f"Error in calculating Altman Z-Score for year {year}: {str(e)}")
                altman_scores[year] = f"Error: {str(e)}"

        return altman_scores
    
    def replace_nan(self, data):
        """
        Replace NaN values with None in a nested dictionary structure
        """
        if isinstance(data, dict):
            return {k: self.replace_nan(v) for k, v in data.items()}
        elif isinstance(data, list):
            return [self.replace_nan(item) for item in data]
        elif pd.isna(data):
            return None
        else:
            return data
    
    def get_sector_averages(self, sector, year):
        """
        Retrieve the sector-wise average Altman Z-Score for a specific year or all years.
        """
        try:
            if sector and sector.lower() != "all":
                averages_df = self.df_sector_avg[self.df_sector_avg['Sector'] == sector]
                if averages_df.empty:
                    #case-insensitive matching
                    sector_match = self.df_sector_avg[self.df_sector_avg['Sector'].str.lower() == sector.lower()]
                    if not sector_match.empty:
                        averages_df = sector_match
                        print(f"Found sector using case-insensitive match: {sector_match['Sector'].iloc[0]}")
            else:
                averages_df = self.df_sector_avg

            if averages_df.empty:
                print(f"No data found for sector: {sector}")
                return {"error": f"No data found for sector: {sector}"}
            
            # Filter by year if specified
            if year and year.lower() != "all":
                year_column = f"AltmanZscore {year}"
                if year_column not in self.df_sector_avg.columns:
                    return {"error": f"Year {year} is not available in the dataset."}

                # Select only the relevant year column and average row
                averages_df = averages_df[averages_df['Org Name'] == 'Sector Average'][['Sector', year_column]]
                return averages_df.rename(columns={year_column: "AltmanZscore"}).to_dict(orient="records")
            else:
                averages_df = averages_df[averages_df['Org Name'] == 'Sector Average']
                averages_df = averages_df.drop(columns=['Sub-Sector', 'Org Name'], errors='ignore')
                return averages_df.to_dict(orient="records")

        except Exception as e:
            print(f"Error retrieving sector averages: {str(e)}")
            return {"error": str(e)}
    def get(self, request):
        try:
            sector = request.query_params.get('sector', None)
            sub_sector = request.query_params.get('sub_sector', None)
            org_name = request.query_params.get('org_name', None)
            year = request.query_params.get('year', None)

            # Handle the case where org_name is "All"
            if org_name and org_name.lower() == "all":
                try:
                    average_data = self.df_sector_avg[self.df_sector_avg['Org Name'].str.contains('Average', case=False, na=False)]
                    
                    if sector and sector.lower() != "all":
                        average_data = average_data[average_data['Sector'] == sector]
                    
                    if sub_sector:
                        average_data = average_data[average_data['Sub-Sector'] == sub_sector]
                    
                    if average_data.empty:
                        return Response({"message": "No average data found matching the specified criteria."}, 
                                        status=status.HTTP_404_NOT_FOUND)
                    
                    if year and year.lower() != "all":
                        year_column = f"AltmanZscore {year}"
                        if year_column not in average_data.columns:
                            return Response({"message": f"No data found for the year {year}."},
                                        status=status.HTTP_404_NOT_FOUND)
                                
                        result_value = average_data[year_column].iloc[0]
                                
                        return Response({
                            "sector": sector,
                            "sub_sector": sub_sector,
                            "org_name": "All",
                            "year": year,
                            "altman_zscore": result_value
                        }, status=status.HTTP_200_OK)
                    else:
                        year_columns = [col for col in average_data.columns if col.startswith('AltmanZscore')]
                                
                        result_dict = {}
                        for col in year_columns:
                            year_value = col.split(' ')[1]  
                            result_dict[year_value] = average_data[col].iloc[0]
                                
                        return Response({
                            "sector": sector,
                            "sub_sector": sub_sector,
                            "org_name": "All",
                            "year": "all",
                            "altman_zscore": result_dict
                        }, status=status.HTTP_200_OK)
                except Exception as e:
                    print(f"Error processing average data: {str(e)}")
                    return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

            if sector and sector.lower() == "all":
                filtered_df = self.df_sector_avg.copy()
                all_possible_years = []
                
                for col in filtered_df.columns:
                    if col.startswith('AltmanZscore '):
                        year_value = col.split(' ')[1]
                        all_possible_years.append(year_value)
                all_possible_years = sorted(all_possible_years)
                
                sector_groups = {}
                
                # Get subsector averages and  organizations
                subsector_averages = filtered_df[filtered_df['Org Name'].str.contains('Average', case=False, na=False)]
                regular_orgs = filtered_df[~filtered_df['Org Name'].str.contains('Average', case=False, na=False)]
                
                for sector_name, sector_data in regular_orgs.groupby('Sector'):
                    if sector_name not in sector_groups:
                        sector_groups[sector_name] = {
                            "sector": sector_name,
                            "sub_sectors": {},
                            "years": {yr: None for yr in all_possible_years},
                            "total_organizations": len(sector_data['Org Name'].unique())
                        }
                    
                    # Process each sub-sector within this sector
                    for sub_sector_name, sub_sector_data in sector_data.groupby('Sub-Sector'):
                        total_orgs_in_subsector = len(sub_sector_data['Org Name'].unique())
                        
                        if sub_sector_name not in sector_groups[sector_name]["sub_sectors"]:
                            sector_groups[sector_name]["sub_sectors"][sub_sector_name] = {
                                "sub_sector": sub_sector_name,
                                "years": {yr: None for yr in all_possible_years},
                                "total_organizations": total_orgs_in_subsector,
                                "": {yr: None for yr in all_possible_years} 
                            }
                        
                        # Get the pre-calculated averages for this sub-sector
                        sub_avg_data = subsector_averages[
                            (subsector_averages['Sector'] == sector_name) & 
                            (subsector_averages['Sub-Sector'] == sub_sector_name)
                        ]
                        
                        for _, row in sub_avg_data.iterrows():
                            for yr in all_possible_years:
                                year_col = f"AltmanZscore {yr}"
                                if year_col in row.index and not pd.isna(row[year_col]):
                                    sector_groups[sector_name]["sub_sectors"][sub_sector_name]["years"][yr] = row[year_col]
                                    # Calculate sum for sub-sector (average * number of organizations)
                                    sum_value = row[year_col] * total_orgs_in_subsector
                                    sector_groups[sector_name]["sub_sectors"][sub_sector_name][""][yr] = sum_value
            
                for sector_name, sector_info in sector_groups.items():
                    for year_str in all_possible_years:
                        valid_subsectors = []
                        year_total_sum = 0
                        
                        for sub_sector_info in sector_info["sub_sectors"].values():
                            if sub_sector_info[""][year_str] is not None:
                                valid_subsectors.append(sub_sector_info)
                                year_total_sum += sub_sector_info[""][year_str]
                        
                        if valid_subsectors:
                            if sector_info["total_organizations"] > 0:
                                sector_avg = year_total_sum / sector_info["total_organizations"]
                                sector_groups[sector_name]["years"][year_str] = sector_avg
                
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
                        sub_data = {
                            "sub_sector": sub_info["sub_sector"],
                            "years": sub_info["years"],
                            "total_organizations": sub_info["total_organizations"]
                        }
                        sub_sectors.append(sub_data)
                    
                    sector_entry["sub_sectors"] = sub_sectors
                    results.append(sector_entry)
                
                results = self.replace_nan(results)
                
                return Response(
                    {
                        "sector": "All",
                        "year": year if year else "all",
                        "altman_zscores": results
                    },
                    status=status.HTTP_200_OK
                )
            
            predefined_sub_indicators = [
                '    1. Capital work in progress',
                ' Total Assets (A+B) / Equity & Liabilities (C+D+E)',
                '         of which: un-appropriated profit(loss) / retained earnings',
                '    6. EBIT (F3-F4+F5)',
                "C. Shareholders' Equity (C1+C2+C3)",
                'D. Non-Current Liabilities (D1+D2+D3+D4+D5)',
                'E. Current Liabilities (E1+E2+E3+E4)'
            ]

            filtered_df = self.df_pivot
            
            if sector:
                filtered_df = filtered_df[filtered_df['Sector'] == sector]
            if sub_sector:
                filtered_df = filtered_df[filtered_df['Sub-Sector'] == sub_sector]
            if org_name:
                filtered_df = filtered_df[filtered_df['Org Name'] == org_name]

            if filtered_df.empty:
                if org_name:
                    print(f"Trying flexible match for org_name: {org_name}")
                    matched_df = self.df_pivot[self.df_pivot['Org Name'].str.contains(org_name, case=False, na=False)]
                    if not matched_df.empty:
                        filtered_df = matched_df
                        print(f"Found organization using flexible match: {matched_df['Org Name'].iloc[0]}")

            if filtered_df.empty:
                return Response({"message": "No data found matching the specified criteria."}, 
                                status=status.HTTP_404_NOT_FOUND)

            filtered_df = filtered_df[
                (filtered_df['Sub Indicator'].isin(predefined_sub_indicators)) |
                (filtered_df['Indicator'].isin(predefined_sub_indicators)) |
                (filtered_df['Sub-Sub Indicator'].isin(predefined_sub_indicators))
            ]
            
            print(f"Filtered data shape after indicator matching: {filtered_df.shape}")
            
            filtered_df = filtered_df.drop_duplicates(subset=['Indicator', 'Sub Indicator', 'Sub-Sub Indicator'], keep='first')

            if year and year.lower() != "all":
                if year not in filtered_df.columns:
                    return Response({"message": f"No data found for the year {year}."}, 
                                    status=status.HTTP_404_NOT_FOUND)
                                    
                filtered_df = filtered_df[['Sector', 'Sub-Sector', 'Org Name', 'Indicator', 'Sub Indicator', 'Sub-Sub Indicator', year]]
                
                print(f"\nFiltered DataFrame for {org_name} ({year}):")
                print(filtered_df[['Indicator', 'Sub Indicator', 'Sub-Sub Indicator', year]])

                altman_zscore = self.calculate_altman_score(filtered_df)
                response_data = {
                    "sector": sector,
                    "sub_sector": sub_sector,
                    "org_name": org_name,
                    "year": year,
                    "altman_zscore": altman_zscore.get(year, "Insufficient data or error in calculation")
                }
            else:
                altman_zscore = self.calculate_altman_score(filtered_df)
                response_data = {
                    "sector": sector,
                    "sub_sector": sub_sector,
                    "org_name": org_name,
                    "year": "all",
                    "altman_zscore": altman_zscore
                }

            return Response(response_data, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)