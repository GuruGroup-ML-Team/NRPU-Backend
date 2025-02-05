# import pandas as pd
# import numpy as np
# from rest_framework.response import Response
# from rest_framework.views import APIView
# from rest_framework import status
# import re

# class FinancialStatementAnalysisView(APIView):
#     def get(self, request):
#         try:
#             print("Request data (GET):", request.query_params)

#             sector = request.query_params.get('sector', 'All')
#             sub_sector = request.query_params.get('sub_sector', 'All')
#             org_name = request.query_params.get('org_name', 'All')
#             indicator = request.query_params.get('indicator', 'All')
#             sub_indicator = request.query_params.get('sub_indicator', None)
#             sub_sub_indicator = request.query_params.get('sub_sub_indicator', None)
#             year = request.query_params.get('year', 'All')

#             if not year:
#                 return Response({"error": "Year is required."}, status=status.HTTP_400_BAD_REQUEST)

#             columns = ['Sector', 'Sub-Sector', 'Org Name', 'Indicator', 'Sub Indicator', 'Sub-Sub Indicator', 
#                        '2017', '2018', '2019', '2020', '2021', '2022']
#             try:
#                 file_path = 'Data/input_data.xlsx'
#                 df = pd.read_excel(file_path, header=None, names=columns)
#             except Exception as e:
#                 return Response({"error": f"Error loading the Excel file: {str(e)}"}, 
#                               status=status.HTTP_500_INTERNAL_SERVER_ERROR)

#             df['Indicator'] = df['Indicator'].str.strip()

#             # Add filter for main indicators when sub-indicators are not requested
#             if sub_indicator is None and sub_sub_indicator is None:
#                 df = df[df['Sub Indicator'].isna() & df['Sub-Sub Indicator'].isna()]

#             year_columns = ['2017', '2018', '2019', '2020', '2021', '2022']
#             if year == 'All':
#                 selected_years = year_columns
#             elif year in year_columns:
#                 selected_years = [year]
#             else:
#                 return Response({"error": "Invalid year specified"}, status=status.HTTP_400_BAD_REQUEST)

#             predefined_sectors = [
#                 "Textile Sector", "Sugar", "Food", "Chemicals, Chemical Products and Pharmaceuticals",
#                 "Manufacturing", "Mineral products", "Cement", "Motor Vehicles, Trailers & Autoparts",
#                 "Fuel and Energy Sector", "Information and Communication Services", 
#                 "Coke and Refined Petroleum Products", "Paper, Paperboard and Products",
#                 "Electrical Machinery and Apparatus", "Other Services Activities"
#             ]

#             # Check if only sector=All is passed without other filters
#             only_sector_all = (
#                 sector == 'All' and 
#                 sub_sector == 'All' and 
#                 org_name == 'All' and 
#                 indicator == 'All' and 
#                 sub_indicator is None and 
#                 sub_sub_indicator is None
#             )

#             if only_sector_all:
#                 df = df[df['Sector'].isin(predefined_sectors)]
#                 result = []
                
#                 for sector_name in predefined_sectors:
#                     sector_df = df[df['Sector'] == sector_name]
#                     if not sector_df.empty:
#                         sector_data = sector_df.iloc[0]
                        
#                         sector_result = {
#                             'Sector': sector_data['Sector'],
#                             'Sub-Sector': sector_data['Sub-Sector'],
#                             'Org Name': sector_data['Org Name'],
#                             'Indicator': sector_data['Indicator'],
#                             'Sub Indicator': None if pd.isna(sector_data['Sub Indicator']) else sector_data['Sub Indicator'],
#                             'Sub-Sub Indicator': None if pd.isna(sector_data['Sub-Sub Indicator']) else sector_data['Sub-Sub Indicator']
#                         }
                        
#                         # Handle year values with explicit NaN checking
#                         for year in selected_years:
#                             value = sector_data[year]
#                             if pd.isna(value) or np.isnan(value):
#                                 sector_result[year] = None
#                             else:
#                                 try:
#                                     sector_result[year] = float(value)
#                                 except (ValueError, TypeError):
#                                     sector_result[year] = None
                        
#                         result.append(sector_result)
                
#                 return Response(result, status=status.HTTP_200_OK)

#             if sector == 'All':
#                 df = df[df['Sector'].isin(predefined_sectors)]
#             else:
#                 df = df[df['Sector'] == sector]

#             if sector != 'All' and sub_sector != 'All':
#                 df = df[df['Sub-Sector'] == sub_sector]
            
#             if sector != 'All' and org_name != 'All':
#                 df = df[df['Org Name'] == org_name]
            
#             if indicator != 'All':
#                 df = df[df['Indicator'].str.contains(f"{re.escape(indicator)}", case=False, na=False)]
            
#             if sub_indicator:
#                 df = df[df['Sub Indicator'].str.contains(f"{re.escape(sub_indicator)}", case=False, na=False)]
            
#             if sub_sub_indicator:
#                 df = df[df['Sub-Sub Indicator'].str.contains(f"{re.escape(sub_sub_indicator)}", case=False, na=False)]

#             # Existing indicator-specific request for all sectors
#             if sector == 'All' and indicator != 'All':
#                 indicator_filter = df['Indicator'].str.contains(f"{re.escape(indicator)}", case=False, na=False)
                
#                 if sub_sub_indicator:
#                     df = df[
#                         indicator_filter &
#                         df['Sub Indicator'].str.contains(f"{re.escape(sub_indicator)}", case=False, na=False) &
#                         df['Sub-Sub Indicator'].str.contains(f"{re.escape(sub_sub_indicator)}", case=False, na=False)
#                     ]
#                 elif sub_indicator:
#                     df = df[
#                         indicator_filter &
#                         df['Sub Indicator'].str.contains(f"{re.escape(sub_indicator)}", case=False, na=False) &
#                         (df['Sub-Sub Indicator'].isna())
#                     ]
#                 else:
#                     df = df[
#                         indicator_filter &
#                         (df['Sub Indicator'].isna()) &
#                         (df['Sub-Sub Indicator'].isna())
#                     ]

#                 result = []
                
#                 for sector_name in df['Sector'].unique():
#                     sector_df = df[df['Sector'] == sector_name]
                    
#                     try:
#                         subsector_avgs = sector_df.groupby('Sub-Sector')[selected_years].apply(
#                             lambda x: x.apply(pd.to_numeric, errors='coerce').mean()
#                         ).reset_index()
                        
#                         sector_avg = subsector_avgs[selected_years].mean()
                        
#                         sector_data = {
#                             'Sector': sector_name,
#                             'Indicator': indicator,
#                             'Sub_Indicator': sub_indicator if sub_indicator else None,
#                             'Sub_Sub_Indicator': sub_sub_indicator if sub_sub_indicator else None,
#                             'Subsector_Averages': [],
#                             'Combined Sector Average': {year: float(sector_avg[year]) if pd.notna(sector_avg[year]) else None for year in selected_years}
#                         }
                        
#                         for _, subsector_row in subsector_avgs.iterrows():
#                             subsector_data = {
#                                 'Sub-Sector': subsector_row['Sub-Sector']
#                             }
#                             for year in selected_years:
#                                 value = subsector_row[year]
#                                 subsector_data[year] = round(float(value), 2) if pd.notna(value) else None
                            
#                             subsector_orgs = sector_df[sector_df['Sub-Sector'] == subsector_row['Sub-Sector']]
#                             org_details = []
                            
#                             for _, org in subsector_orgs.iterrows():
#                                 org_entry = {
#                                     'Org_Name': org['Org Name']
#                                 }
#                                 for year in selected_years:
#                                     value = org[year]
#                                     org_entry[year] = round(float(value), 2) if pd.notna(value) else None
#                                 org_details.append(org_entry)
                            
#                             sector_data['Subsector_Averages'].append(subsector_data)
                        
#                         result.append(sector_data)
#                     except Exception as e:
#                         print(f"Error processing sector {sector_name}: {str(e)}")
#                         continue
                
#                 return Response(result, status=status.HTTP_200_OK)

#             # Handle remaining scenarios
#             df = df[['Sector', 'Sub-Sector', 'Org Name', 'Indicator', 'Sub Indicator', 'Sub-Sub Indicator'] + selected_years]

#             if df.empty:
#                 return Response({"message": "No data found matching the criteria."}, status=status.HTTP_404_NOT_FOUND)

#             selected_columns = ['Sector', 'Sub-Sector', 'Org Name', 'Indicator', 
#                               'Sub Indicator', 'Sub-Sub Indicator'] + selected_years

#             # Handle NaN values before converting to dict
#             df = df.replace({np.nan: None})
#             result = df[selected_columns].to_dict(orient='records')

#             return Response(result, status=status.HTTP_200_OK)

#         except Exception as e:
#             return Response({"error": f"Unexpected error: {str(e)}"}, 
#                           status=status.HTTP_500_INTERNAL_SERVER_ERROR)




































import pandas as pd
import numpy as np
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
import re


class FinancialStatementAnalysisView(APIView):
    def get(self, request):
        try:
            print("Request data (GET):", request.query_params)

            sector = request.query_params.get('sector', 'All')
            sub_sector = request.query_params.get('sub_sector', 'All')
            org_name = request.query_params.get('org_name', 'All')
            indicator = request.query_params.get('indicator', 'All')
            sub_indicator = request.query_params.get('sub_indicator', None)
            sub_sub_indicator = request.query_params.get('sub_sub_indicator', None)
            year = request.query_params.get('year', 'All')

            if not year:
                return Response({"error": "Year is required."}, status=status.HTTP_400_BAD_REQUEST)

            columns = ['Sector', 'Sub-Sector', 'Org Name', 'Indicator', 'Sub Indicator', 'Sub-Sub Indicator', 
                       '2017', '2018', '2019', '2020', '2021', '2022']
            try:
                file_path = 'Data/input_data.xlsx'
                df = pd.read_excel(file_path, header=None, names=columns)
            except Exception as e:
                return Response({"error": f"Error loading the Excel file: {str(e)}"}, 
                              status=status.HTTP_500_INTERNAL_SERVER_ERROR)

            df['Indicator'] = df['Indicator'].str.strip()

            year_columns = ['2017', '2018', '2019', '2020', '2021', '2022']
            if year == 'All':
                selected_years = year_columns
            elif year in year_columns:
                selected_years = [year]
            else:
                return Response({"error": "Invalid year specified"}, status=status.HTTP_400_BAD_REQUEST)

            predefined_sectors = [
                "Textile Sector", "Sugar", "Food", "Chemicals, Chemical Products and Pharmaceuticals",
                "Manufacturing", "Mineral products", "Cement", "Motor Vehicles, Trailers & Autoparts",
                "Fuel and Energy Sector", "Information and Communication Services", 
                "Coke and Refined Petroleum Products", "Paper, Paperboard and Products",
                "Electrical Machinery and Apparatus", "Other Services Activities"
            ]

            # for only sector filtering
            only_sector_all = (
                sector == 'All' and 
                sub_sector == 'All' and 
                org_name == 'All' and 
                indicator == 'All' and 
                sub_indicator is None and 
                sub_sub_indicator is None
            )

            if only_sector_all:
                result = []
                filtered_df = df[
                    df['Sector'].isin(predefined_sectors) & 
                    df['Sub Indicator'].isna() & 
                    df['Sub-Sub Indicator'].isna()
                ]
                
                seen_combinations = set()
                
                for _, row in filtered_df.iterrows():
                    key = (row['Sector'], row['Indicator'])
                    
                    if key in seen_combinations:
                        continue
                    
                    seen_combinations.add(key)
                    
                    result_row = {
                        'Sector': row['Sector'],
                        'Sub-Sector': row['Sub-Sector'],
                        'Org Name': row['Org Name'],
                        'Indicator': row['Indicator'],
                        'Sub Indicator': None,
                    }
                    
                    #include Sub-Sub Indicator only if it is given in the query params
                    if sub_sub_indicator is not None:
                        result_row['Sub-Sub Indicator'] = None
                    
                    for year in selected_years:
                        value = row[year]
                        if pd.isna(value) or np.isnan(value):
                            result_row[year] = None
                        else:
                            try:
                                result_row[year] = float(value)
                            except (ValueError, TypeError):
                                result_row[year] = None
                    
                    result.append(result_row)
                
                return Response(result, status=status.HTTP_200_OK)

            
            if sector == 'All':
                df = df[df['Sector'].isin(predefined_sectors)]
            else:
                df = df[df['Sector'] == sector]

            
            if sector != 'All' and sub_sector != 'All':
                df = df[df['Sub-Sector'] == sub_sector]
            
           
            if sector != 'All' and org_name != 'All':
                df = df[df['Org Name'] == org_name]

            
            if indicator == 'All' and not sub_indicator and not sub_sub_indicator:
                df = df[df['Sub Indicator'].isna() & df['Sub-Sub Indicator'].isna()]
            else:
                if indicator != 'All' and not sub_indicator and not sub_sub_indicator:
                    df = df[df['Indicator'].str.contains(f"{re.escape(indicator)}", case=False, na=False)]
                    df = df[df['Sub Indicator'].isna() & df['Sub-Sub Indicator'].isna()]
                if sub_indicator:
                    df = df[df['Sub Indicator'].str.contains(f"{re.escape(sub_indicator)}", case=False, na=False)]
                    if not sub_sub_indicator:
                        df = df[df['Sub-Sub Indicator'].isna()]
                
                if sub_sub_indicator:
                    df = df[df['Sub-Sub Indicator'].str.contains(f"{re.escape(sub_sub_indicator)}", case=False, na=False)]

            if sector == 'All' and indicator != 'All':
                indicator_filter = df['Indicator'].str.contains(f"{re.escape(indicator)}", case=False, na=False)
                
                if sub_sub_indicator:
                    df = df[
                        indicator_filter &
                        df['Sub Indicator'].str.contains(f"{re.escape(sub_indicator)}", case=False, na=False) &
                        df['Sub-Sub Indicator'].str.contains(f"{re.escape(sub_sub_indicator)}", case=False, na=False)
                    ]
                elif sub_indicator:
                    df = df[
                        indicator_filter &
                        df['Sub Indicator'].str.contains(f"{re.escape(sub_indicator)}", case=False, na=False) &
                        (df['Sub-Sub Indicator'].isna())
                    ]
                else:
                    df = df[
                        indicator_filter &
                        (df['Sub Indicator'].isna()) &
                        (df['Sub-Sub Indicator'].isna())
                    ]

                result = []
                
                for sector_name in df['Sector'].unique():
                    sector_df = df[df['Sector'] == sector_name]
                    
                    try:
                        subsector_avgs = sector_df.groupby('Sub-Sector')[selected_years].apply(
                            lambda x: x.apply(pd.to_numeric, errors='coerce').mean()
                        ).reset_index()
                        
                        sector_avg = subsector_avgs[selected_years].mean()
                        
                        sector_data = {
                            'Sector': sector_name,
                            'Indicator': indicator,
                            'Sub_Indicator': sub_indicator if sub_indicator else None,
                            'Sub_Sub_Indicator': sub_sub_indicator if sub_sub_indicator else None,
                        }
                        
                        if sub_sub_indicator is not None:
                            sector_data['Sub_Sub_Indicator'] = sub_sub_indicator
                        
                        sector_data['Subsector_Averages'] = []
                        sector_data['Combined Sector Average'] = {
                            year: float(sector_avg[year]) if pd.notna(sector_avg[year]) else None 
                            for year in selected_years
                        }
                        
                        for _, subsector_row in subsector_avgs.iterrows():
                            subsector_data = {
                                'Sub-Sector': subsector_row['Sub-Sector']
                            }
                            for year in selected_years:
                                value = subsector_row[year]
                                subsector_data[year] = round(float(value), 2) if pd.notna(value) else None
                            
                            subsector_orgs = sector_df[sector_df['Sub-Sector'] == subsector_row['Sub-Sector']]
                            org_details = []
                            
                            for _, org in subsector_orgs.iterrows():
                                org_entry = {
                                    'Org_Name': org['Org Name']
                                }
                                for year in selected_years:
                                    value = org[year]
                                    org_entry[year] = round(float(value), 2) if pd.notna(value) else None
                                org_details.append(org_entry)
                            
                            sector_data['Subsector_Averages'].append(subsector_data)
                        
                        result.append(sector_data)
                    except Exception as e:
                        print(f"Error processing sector {sector_name}: {str(e)}")
                        continue
                
                return Response(result, status=status.HTTP_200_OK)

            selected_columns = ['Sector', 'Sub-Sector', 'Org Name', 'Indicator', 'Sub Indicator', 'Sub-Sub Indicator']
            
            if sub_sub_indicator is not None:
                selected_columns.append('Sub-Sub Indicator')
            
            selected_columns.extend(selected_years)
            
            df = df[selected_columns]

            if df.empty:
                return Response({"message": "No data found matching the criteria."}, status=status.HTTP_404_NOT_FOUND)

            df = df.replace({np.nan: None})
            result = df[selected_columns].to_dict(orient='records')

            return Response(result, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({"error": f"Unexpected error: {str(e)}"}, 
                          status=status.HTTP_500_INTERNAL_SERVER_ERROR)