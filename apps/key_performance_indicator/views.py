# import pandas as pd
# from rest_framework.response import Response
# from rest_framework.views import APIView
# from rest_framework import status
# import re
# import numpy as np

# class KeyPerformanceIndicatorView(APIView):
    
#     def calculate_subsector_averages(self, df, sector, selected_years, sub_indicator, sub_sub_indicator):
#         """Helper function to calculate sub-sector and overall sector averages"""
#         result = []
#         total_orgs = 0
        
#         # For storing sum of all sub-sector values
#         subsector_sums = {year: 0.0 for year in selected_years}
        
#         # Get number of unique sub-sectors
#         num_subsectors = len(df['Sub-Sector'].unique())
        
#         # First calculate average for each sub-sector
#         for curr_subsector in df['Sub-Sector'].unique():
#             subsector_data = df[df['Sub-Sector'] == curr_subsector]
#             if not subsector_data.empty:
#                 # Calculate average for current sub-sector
#                 num_orgs = len(subsector_data['Org Name'].unique())
#                 subsector_avg = subsector_data[selected_years].mean()
                
#                 # Add subsector's actual values to total sum
#                 for year in selected_years:
#                     if not pd.isna(subsector_avg[year]):
#                         subsector_sums[year] += subsector_avg[year]
                
#                 total_orgs += num_orgs
                
#                 result.append({
#                     'Sector': sector,
#                     'Sub-Sector': curr_subsector,
#                     'Org Name': f'All ({num_orgs} organizations)',
#                     'Indicator': "I. Key Performance Indicators",
#                     'Sub Indicator': sub_indicator.strip(),
#                     'Sub-Sub Indicator': sub_sub_indicator.strip() if sub_sub_indicator else "",
#                     **{year: round(float(subsector_avg[year]), 5) if not pd.isna(subsector_avg[year]) else "N/A" 
#                     for year in selected_years}
#                 })
        
#         # Only calculate overall sector average if there are multiple sub-sectors
#         if total_orgs > 0 and num_subsectors > 1:
#             result.append({
#                 'Sector': sector,
#                 'Sub-Sector': 'All',
#                 'Org Name': f'All (Total {total_orgs} organizations)',
#                 'Indicator': "I. Key Performance Indicators",
#                 'Sub Indicator': sub_indicator.strip(),
#                 'Sub-Sub Indicator': sub_sub_indicator.strip() if sub_sub_indicator else "",
#                 'OverAll Average': {
#                     year: round(float(subsector_sums[year] / total_orgs), 5) if subsector_sums[year] != 0 else "N/A" 
#                     for year in selected_years
#                 }
#             })
            
#         return result
    
#     def get(self, request, *args, **kwargs):
#         try:
#             print("Request data (GET):", request.query_params)
#             sector = request.query_params.get('sector', 'All')
#             sub_sector = request.query_params.get('sub_sector', 'All')
#             org_name = request.query_params.get('org_name', 'All')
#             sub_indicator = request.query_params.get('sub_indicator', 'All')
#             sub_sub_indicator = request.query_params.get('sub_sub_indicator', None)
#             year = request.query_params.get('year', 'All')

#             # Validate input fields
#             if not year:
#                 return Response({"error": "Year is required."}, status=status.HTTP_400_BAD_REQUEST)
            
#             if sub_indicator == 'All':
#                 return Response({"error": "Sub Indicator cannot be 'All'."}, status=status.HTTP_400_BAD_REQUEST)
            
#             if not sub_sub_indicator:
#                 return Response({"error": "Sub_Sub_Indicator is required"}, status=status.HTTP_400_BAD_REQUEST)
            
#             if sub_sub_indicator == 'All':
#                 return Response({"error": "Sub Sub Indicator cannot be 'All'."}, status=status.HTTP_400_BAD_REQUEST)
            
#             # Define column names
#             columns = ['Sector', 'Sub-Sector', 'Org Name', 'Indicator', 'Sub Indicator', 'Sub-Sub Indicator', 
#                        '2017', '2018', '2019', '2020', '2021', '2022','2023]

#             # Load Excel data
#             try:
#                 file_path = 'Data/input_data.xlsx'  # Adjust path as needed
#                 df = pd.read_excel(file_path, header=None, names=columns)
#             except Exception as e:
#                 return Response({"error": f"Error loading the Excel file: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

#             # Clean the data
#             df['Indicator'] = df['Indicator'].str.strip()
#             df['Sub Indicator'] = df['Sub Indicator'].str.strip()
#             df['Sub-Sub Indicator'] = df['Sub-Sub Indicator'].str.strip()
#             df['Sector'] = df['Sector'].str.strip()
#             df['Sub-Sector'] = df['Sub-Sector'].str.strip()
#             df['Org Name'] = df['Org Name'].str.strip()

#             # Filter to only include "I. Key Performance Indicators"
#             df = df[df['Indicator'] == "I. Key Performance Indicators"]

#             # Convert year columns to numeric
#             year_columns = ['2017', '2018', '2019', '2020', '2021', '2022','2023]
#             for year_col in year_columns:
#                 df[year_col] = pd.to_numeric(df[year_col], errors='coerce')

#             # Handle year selection
#             if year == 'All':
#                 selected_years = year_columns
#             elif year in year_columns:
#                 selected_years = [year]
#             else:
#                 return Response({"error": "Invalid year specified"}, status=status.HTTP_400_BAD_REQUEST)

#             # Predefined sectors
#             predefined_sectors = [
#                 "Textile Sector", "Sugar", "Food", "Chemicals, Chemical Products and Pharmaceuticals",
#                 "Manufacturing", "Mineral products", "Cement", "Motor Vehicles, Trailers & Autoparts",
#                 "Fuel and Energy Sector", "Information and Communication Services", 
#                 "Coke and Refined Petroleum Products", "Paper, Paperboard and Products",
#                 "Electrical Machinery and Apparatus", "Other Services Activities"
#             ]

#             # Sector filtering
#             if sector == 'All':
#                 df = df[df['Sector'].isin(predefined_sectors)]
#             else:
#                 df = df[df['Sector'].str.strip() == sector.strip()]

#             # Indicator filtering
#             # if sub_indicator != 'All':
#             #     clean_sub_indicator = sub_indicator.strip()
#             #     df = df[df['Sub Indicator'].str.strip().str.contains(clean_sub_indicator, case=False, na=False)]
                
#             #     if sub_sub_indicator:
#             clean_sub_sub_indicator = sub_sub_indicator.strip()
#             df['Clean Sub-Sub'] = df['Sub-Sub Indicator'].str.extract(r'([^(]+)')[0].str.strip()
#             df = df[df['Clean Sub-Sub'].str.contains(clean_sub_sub_indicator, case=False, na=False)]

#             result = []

#             if org_name != 'All':
#                 # First try exact match
#                 filtered_df = df[df['Org Name'] == org_name.strip()]
                
#                 if filtered_df.empty:
#                     filtered_df = df[df['Org Name'].str.contains(org_name.strip(), case=False, na=False)]
                
#                 if not filtered_df.empty:
#                     # Process each matching row
#                     for idx, row in filtered_df.iterrows():
#                         result.append({
#                             'Sector': row['Sector'],
#                             'Sub-Sector': row['Sub-Sector'],
#                             'Org Name': row['Org Name'],
#                             'Indicator': "I. Key Performance Indicators",
#                             'Sub Indicator': sub_indicator.strip(),
#                             'Sub-Sub Indicator': sub_sub_indicator.strip() if sub_sub_indicator else "",
#                             **{year: round(float(row[year]), 5) if not pd.isna(row[year]) else "N/A" 
#                                for year in selected_years}
#                         })

#             # Case 1: Specific sector, specific sub-sector, org_name='All'
#             elif sector != 'All' and sub_sector != 'All' and org_name == 'All':
#                 filtered_df = df[df['Sub-Sector'].str.strip() == sub_sector.strip()]
#                 if not filtered_df.empty:
#                     avg_values = filtered_df[selected_years].mean()
#                     num_orgs = len(filtered_df['Org Name'].unique())
                    
#                     result.append({
#                         'Sector': sector,
#                         'Sub-Sector': sub_sector,
#                         'Org Name': f'All ({num_orgs} organizations)',
#                         'Indicator': "I. Key Performance Indicators",
#                         'Sub Indicator': sub_indicator.strip(),
#                         'Sub-Sub Indicator': sub_sub_indicator.strip() if sub_sub_indicator else "",
#                         **{year: round(float(avg_values[year]), 5) if not pd.isna(avg_values[year]) else "N/A" 
#                            for year in selected_years}
#                     })

#             # Case 2: Sector='All'
#             elif sector == 'All':
#                 for curr_sector in predefined_sectors:
#                     sector_data = df[df['Sector'] == curr_sector]
#                     if not sector_data.empty:
#                         sector_results = self.calculate_subsector_averages(
#                             sector_data, curr_sector, selected_years, sub_indicator, sub_sub_indicator
#                         )
#                         if isinstance(sector_results, list):
#                             result.extend(sector_results)
#                         else:
#                             # Handle case where an error dict is returned
#                             if 'error' in sector_results:
#                                 return Response(sector_results, status=status.HTTP_400_BAD_REQUEST)

#             # Case 3: Multiple sub-sectors within a sector
#             elif sector != 'All' and sub_sector == 'All':
#                 sector_results = self.calculate_subsector_averages(
#                     df, sector, selected_years, sub_indicator, sub_sub_indicator
#                 )
#                 if isinstance(sector_results, list):
#                     result.extend(sector_results)
#                 else:
#                     # Handle case where an error dict is returned
#                     if 'error' in sector_results:
#                         return Response(sector_results, status=status.HTTP_400_BAD_REQUEST)

#             print("Filtered DataFrame:")
#             print(df[['Sector', 'Sub-Sector', 'Org Name', 'Sub Indicator', 'Sub-Sub Indicator'] + selected_years])
#             print("\nCalculated Result:")
#             print(result)

#             if not result:
#                 return Response({"message": "No data found matching the criteria."}, status=status.HTTP_404_NOT_FOUND)

#             return Response(result, status=status.HTTP_200_OK)

#         except KeyError as e:
#             return Response({"error": f"Missing expected column in the dataset: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
#         except ValueError as e:
#             return Response({"error": f"Invalid data format: {str(e)}"}, status=status.HTTP_400_BAD_REQUEST)
#         except Exception as e:
#             return Response({"error": f"Unexpected error: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)








import pandas as pd
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
import re
import numpy as np

class KeyPerformanceIndicatorView(APIView):
    
    def calculate_subsector_averages(self, df, sector, selected_years, sub_indicator, sub_sub_indicator):
        """Helper function to calculate sub-sector and overall sector averages"""
        result = []
        total_orgs = 0
        
        # For storing sum of all sub-sector values
        subsector_sums = {year: 0.0 for year in selected_years}
        
        # Get number of unique sub-sectors
        # num_subsectors = len(df['Sub-Sector'].unique())
        
        # First calculate average for each sub-sector
        for curr_subsector in df['Sub-Sector'].unique():
            subsector_data = df[df['Sub-Sector'] == curr_subsector]
            if not subsector_data.empty:
                # Calculate average for current sub-sector
                num_orgs = len(subsector_data['Org Name'].unique())
                subsector_avg = subsector_data[selected_years].mean()
                
                # Add subsector's actual values to total sum
                for year in selected_years:
                    if not pd.isna(subsector_avg[year]):
                        subsector_sums[year] += subsector_avg[year]
                
                total_orgs += num_orgs
                
                result.append({
                    'Sector': sector,
                    'Sub-Sector': curr_subsector,
                    'Org Name': f'All ({num_orgs} organizations)',
                    'Indicator': "I. Key Performance Indicators",
                    'Sub Indicator': sub_indicator.strip(),
                    'Sub-Sub Indicator': sub_sub_indicator.strip() if sub_sub_indicator else "",
                    **{year: round(float(subsector_avg[year]), 5) if not pd.isna(subsector_avg[year]) else "N/A" 
                    for year in selected_years}
                })
        
        return result, total_orgs, subsector_sums
    
    def get(self, request, *args, **kwargs):
        try:
            print("Request data (GET):", request.query_params)
            sector = request.query_params.get('sector', 'All')
            sub_sector = request.query_params.get('sub_sector', 'All')
            org_name = request.query_params.get('org_name', 'All')
            sub_indicator = request.query_params.get('sub_indicator', 'All')
            sub_sub_indicator = request.query_params.get('sub_sub_indicator', None)
            year = request.query_params.get('year', 'All')

            # Validate input fields
            if not year:
                return Response({"error": "Year is required."}, status=status.HTTP_400_BAD_REQUEST)
            
            if sub_indicator == 'All':
                return Response({"error": "Sub Indicator cannot be 'All'."}, status=status.HTTP_400_BAD_REQUEST)
            
            if not sub_sub_indicator:
                return Response({"error": "Sub_Sub_Indicator is required"}, status=status.HTTP_400_BAD_REQUEST)
            
            if sub_sub_indicator == 'All':
                return Response({"error": "Sub Sub Indicator cannot be 'All'."}, status=status.HTTP_400_BAD_REQUEST)
            
            # Define column names
            columns = ['Sector', 'Sub-Sector', 'Org Name', 'Indicator', 'Sub Indicator', 'Sub-Sub Indicator', 
                       '2017', '2018', '2019', '2020', '2021', '2022','2023']

            # Load Excel data
            try:
                file_path = 'Data/input_data.xlsx' 
                df = pd.read_excel(file_path, header=None, names=columns)
            except Exception as e:
                return Response({"error": f"Error loading the Excel file: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

            # Clean the data
            df['Indicator'] = df['Indicator'].str.strip()
            df['Sub Indicator'] = df['Sub Indicator'].str.strip()
            df['Sub-Sub Indicator'] = df['Sub-Sub Indicator'].str.strip()
            df['Sector'] = df['Sector'].str.strip()
            df['Sub-Sector'] = df['Sub-Sector'].str.strip()
            df['Org Name'] = df['Org Name'].str.strip()

            # Filter to only include "I. Key Performance Indicators"
            df = df[df['Indicator'] == "I. Key Performance Indicators"]

            # Convert year columns to numeric
            year_columns = ['2017', '2018', '2019', '2020', '2021', '2022','2023']
            for year_col in year_columns:
                df[year_col] = pd.to_numeric(df[year_col], errors='coerce')

            if year == 'All':
                selected_years = year_columns
            elif year in year_columns:
                selected_years = [year]
            else:
                return Response({"error": "Invalid year specified"}, status=status.HTTP_400_BAD_REQUEST)

            # Predefined sectors
            predefined_sectors = [
                "Textile Sector", "Sugar", "Food", "Chemicals, Chemical Products and Pharmaceuticals",
                "Manufacturing", "Mineral products", "Cement", "Motor Vehicles, Trailers & Autoparts",
                "Fuel and Energy Sector", "Information and Communication Services", 
                "Coke and Refined Petroleum Products", "Paper, Paperboard and Products",
                "Electrical Machinery and Apparatus", "Other Services Activities"
            ]

            # Sector filtering
            if sector == 'All':
                df = df[df['Sector'].isin(predefined_sectors)]
            else:
                df = df[df['Sector'].str.strip() == sector.strip()]

            # Indicator filtering
            clean_sub_sub_indicator = sub_sub_indicator.strip()
            df['Clean Sub-Sub'] = df['Sub-Sub Indicator'].str.extract(r'([^(]+)')[0].str.strip()
            df = df[df['Clean Sub-Sub'].str.contains(clean_sub_sub_indicator, case=False, na=False)]

            result = []

            if org_name != 'All':
                # First try exact match
                filtered_df = df[df['Org Name'] == org_name.strip()]
                
                if filtered_df.empty:
                    filtered_df = df[df['Org Name'].str.contains(org_name.strip(), case=False, na=False)]
                
                if not filtered_df.empty:
                    # Process each matching row
                    for idx, row in filtered_df.iterrows():
                        result.append({
                            'Sector': row['Sector'],
                            'Sub-Sector': row['Sub-Sector'],
                            'Org Name': row['Org Name'],
                            'Indicator': "I. Key Performance Indicators",
                            'Sub Indicator': sub_indicator.strip(),
                            'Sub-Sub Indicator': sub_sub_indicator.strip() if sub_sub_indicator else "",
                            **{year: round(float(row[year]), 5) if not pd.isna(row[year]) else "N/A" 
                               for year in selected_years}
                        })

            # Case 1: Specific sector, specific sub-sector, org_name='All'
            elif sector != 'All' and sub_sector != 'All' and org_name == 'All':
                filtered_df = df[df['Sub-Sector'].str.strip() == sub_sector.strip()]
                if not filtered_df.empty:
                    avg_values = filtered_df[selected_years].mean()
                    num_orgs = len(filtered_df['Org Name'].unique())
                    
                    result = {
                        'Sector': sector,
                        'Sub-Sector': sub_sector,
                        'Organizations': f'All ({num_orgs} organizations)',
                        'Indicator': "I. Key Performance Indicators",
                        'Sub_Indicator': sub_indicator.strip(),
                        'Sub_Sub_Indicator': sub_sub_indicator.strip() if sub_sub_indicator else "",
                        'Subsector_Average': {
                            year: round(float(avg_values[year]), 5) if not pd.isna(avg_values[year]) else None
                            for year in selected_years
                        }
                    }

            # Case 2: Sector='All'
            elif sector == 'All':
                all_sectors_result = []
                
                for curr_sector in predefined_sectors:
                    sector_data = df[df['Sector'] == curr_sector]
                    if not sector_data.empty:
                        sector_results, total_orgs, subsector_sums = self.calculate_subsector_averages(
                            sector_data, curr_sector, selected_years, sub_indicator, sub_sub_indicator
                        )
                        
                        # Only add sectors with data
                        if sector_results:
                            sector_data_formatted = {
                                'Sector': curr_sector,
                                'Organizations': f'All ({total_orgs} organizations)',
                                'Indicator': "I. Key Performance Indicators",
                                'Sub_Indicator': sub_indicator.strip(),
                                'Sub_Sub_Indicator': sub_sub_indicator.strip() if sub_sub_indicator else "",
                                'Subsector_Averages': sector_results,
                            }
                            
                            # Only add Combined Sector Average if multiple subsectors exist
                            if total_orgs > 0:
                                if len(sector_data['Sub-Sector'].unique()) > 1:
                                    sector_data_formatted['Combined Sector Average'] = {
                                        year: subsector_sums[year] / total_orgs if subsector_sums[year] != 0 else None
                                        for year in selected_years
                                    }
                                else:
                                    sector_data_formatted['Combined Sector Average'] = {
                                        year: subsector_sums[year] if subsector_sums[year] != 0 else None
                                        for year in selected_years
                                    }
                            
                            all_sectors_result.append(sector_data_formatted)
                
                result = all_sectors_result  

            # Case 3: Multiple sub-sectors within a sector
            elif sector != 'All' and sub_sector == 'All':
                subsector_results, total_orgs, subsector_sums = self.calculate_subsector_averages(
                    df, sector, selected_years, sub_indicator, sub_sub_indicator
                )
                
                result = {
                    'Sector': sector,
                    'Organizations': f'All ({total_orgs} organizations)',
                    'Indicator': "I. Key Performance Indicators",
                    'Sub_Indicator': sub_indicator.strip(),
                    'Sub_Sub_Indicator': sub_sub_indicator.strip() if sub_sub_indicator else "",
                    'Subsector_Averages': subsector_results,
                }
                
                if total_orgs > 0 and len(df['Sub-Sector'].unique()) > 1:
                    result['Combined Sector Average'] = {
                        year: round(float(subsector_sums[year] / total_orgs), 5) if subsector_sums[year] != 0 else None
                        for year in selected_years
                    }

            print("Filtered DataFrame:")
            print(df[['Sector', 'Sub-Sector', 'Org Name', 'Sub Indicator', 'Sub-Sub Indicator'] + selected_years])
            print("\nCalculated Result:")
            print(result)

            if not result:
                return Response({"message": "No data found matching the criteria."}, status=status.HTTP_404_NOT_FOUND)

            return Response(result, status=status.HTTP_200_OK)

        except KeyError as e:
            return Response({"error": f"Missing expected column in the dataset: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        except ValueError as e:
            return Response({"error": f"Invalid data format: {str(e)}"}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"error": f"Unexpected error: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)