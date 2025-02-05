# import pandas as pd
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

#             if sector == 'All' and indicator != 'All':
#                 df = df[
#                     (df['Indicator'].str.contains(f"{re.escape(indicator)}", case=False, na=False)) &
#                     (df['Sub Indicator'].isna()) &
#                     (df['Sub-Sub Indicator'].isna())
#                 ]

#                 result = []
                
#                 for sector_name in df['Sector'].unique():
#                     sector_df = df[df['Sector'] == sector_name]
                    
#                     subsector_avgs = sector_df.groupby('Sub-Sector')[selected_years].apply(
#                         lambda x: x.apply(pd.to_numeric, errors='coerce').mean()
#                     ).reset_index()
                    
#                     sector_avg = subsector_avgs[selected_years].mean()
                    
#                     sector_data = {
#                         'Sector': sector_name,
#                         'Indicator': indicator,
#                         'Subsector_Averages': [],
#                         'Combined Sector Average': {
#                             '2017': float(sector_avg['2017']) if pd.notna(sector_avg['2017']) else None,
#                             '2018': float(sector_avg['2018']) if pd.notna(sector_avg['2018']) else None,
#                             '2019': float(sector_avg['2019']) if pd.notna(sector_avg['2019']) else None,
#                             '2020': float(sector_avg['2020']) if pd.notna(sector_avg['2020']) else None,
#                             '2021': float(sector_avg['2021']) if pd.notna(sector_avg['2021']) else None,
#                             '2022': float(sector_avg['2022']) if pd.notna(sector_avg['2022']) else None
#                         }
#                     }
                    
#                     for _, subsector_row in subsector_avgs.iterrows():
#                         subsector_data = {
#                             'Sub-Sector': subsector_row['Sub-Sector']
#                         }
#                         for year in selected_years:
#                             subsector_data[year] = round(float(subsector_row[year]), 2) if pd.notna(subsector_row[year]) else None
                        
#                         subsector_orgs = sector_df[sector_df['Sub-Sector'] == subsector_row['Sub-Sector']]
#                         org_data = []
#                         for _, org_row in subsector_orgs.iterrows():
#                             org_entry = {
#                                 'Org_Name': org_row['Org Name']
#                             }
#                             for year in selected_years:
#                                 org_entry[year] = round(float(org_row[year]), 2) if pd.notna(org_row[year]) else None
#                             org_data.append(org_entry)
                            
#                         subsector_data['Organizations'] = org_data
#                         sector_data['Subsector_Averages'].append(subsector_data)
                    
#                     result.append(sector_data)
                
#                 return Response(result, status=status.HTTP_200_OK)

#             if indicator == 'All':
#                 if sector == 'All':
#                     df = df.drop_duplicates(subset=['Sector', 'Indicator'], keep='first').reset_index(drop=True)
#                 else:
#                     df = df[df['Sector'] == sector].drop_duplicates(subset=['Indicator'], keep='first').reset_index(drop=True)
#                 df = df[['Sector', 'Sub-Sector', 'Org Name', 'Indicator', 'Sub Indicator', 'Sub-Sub Indicator'] + selected_years]
            
#             elif sector == 'All':
#                 df = df[df['Indicator'].str.contains(f"{re.escape(indicator)}", case=False, na=False)]

#                 if sub_indicator:
#                     df = df[df['Sub Indicator'].str.contains(f"{re.escape(sub_indicator)}", case=False, na=False)]
#                 if sub_sub_indicator:
#                     df = df[df['Sub-Sub Indicator'].str.contains(f"{re.escape(sub_sub_indicator)}", case=False, na=False)]

#                 df = df.drop_duplicates(subset=['Sector', 'Indicator'], keep='first')

#                 df = df[['Sector', 'Sub-Sector', 'Org Name', 'Indicator', 'Sub Indicator', 'Sub-Sub Indicator'] + selected_years]

#             else:
#                 if sector == 'All':
#                     df = df[df['Sector'].isin(predefined_sectors)]
#                 else:
#                     df = df[df['Sector'] == sector]

#                 if sector != 'All' and sub_sector != 'All':
#                     df = df[df['Sub-Sector'] == sub_sector]
#                 if sector != 'All' and org_name != 'All':
#                     df = df[df['Org Name'] == org_name]
#                 if indicator != 'All':
#                     df = df[df['Indicator'].str.contains(f"{re.escape(indicator)}", case=False, na=False)]
#                 if sub_indicator:
#                     df = df[df['Sub Indicator'].str.contains(f"{re.escape(sub_indicator)}", case=False, na=False)]
#                 if sub_sub_indicator:
#                     df = df[df['Sub-Sub Indicator'].str.contains(f"{re.escape(sub_sub_indicator)}", case=False, na=False)]

#                 df = df.drop_duplicates(subset=['Indicator'], keep='first')

#                 df = df[['Sector', 'Sub-Sector', 'Org Name', 'Indicator', 'Sub Indicator', 'Sub-Sub Indicator'] + selected_years]

#             if df.empty:
#                 return Response({"message": "No data found matching the criteria."}, status=status.HTTP_404_NOT_FOUND)

#             selected_columns = ['Sector', 'Sub-Sector', 'Org Name', 'Indicator', 
#                                 'Sub Indicator', 'Sub-Sub Indicator'] + selected_years

#             df.fillna("N/A", inplace=True)
#             result = df[selected_columns].to_dict(orient='records')

#             return Response(result, status=status.HTTP_200_OK)

#         except Exception as e:
#             return Response({"error": f"Unexpected error: {str(e)}"}, 
#                           status=status.HTTP_500_INTERNAL_SERVER_ERROR)













import pandas as pd
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

            # Add sector filtering with predefined_sectors
            if sector == 'All':
                df = df[df['Sector'].isin(predefined_sectors)]
            else:
                df = df[df['Sector'] == sector]

            # Add additional filters
            if sector != 'All' and sub_sector != 'All':
                df = df[df['Sub-Sector'] == sub_sector]
            
            if sector != 'All' and org_name != 'All':
                df = df[df['Org Name'] == org_name]
            
            if indicator != 'All':
                df = df[df['Indicator'].str.contains(f"{re.escape(indicator)}", case=False, na=False)]
            
            if sub_indicator:
                df = df[df['Sub Indicator'].str.contains(f"{re.escape(sub_indicator)}", case=False, na=False)]
            
            if sub_sub_indicator:
                df = df[df['Sub-Sub Indicator'].str.contains(f"{re.escape(sub_sub_indicator)}", case=False, na=False)]

            # Existing indicator-specific request for all sectors
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
                    
                    subsector_avgs = sector_df.groupby('Sub-Sector')[selected_years].apply(
                        lambda x: x.apply(pd.to_numeric, errors='coerce').mean()
                    ).reset_index()
                    
                    sector_avg = subsector_avgs[selected_years].mean()
                    
                    sector_data = {
                        'Sector': sector_name,
                        'Indicator': indicator,
                        'Sub_Indicator': sub_indicator if sub_indicator else None,
                        'Sub_Sub_Indicator': sub_sub_indicator if sub_sub_indicator else None,
                        'Subsector_Averages': [],
                        'Combined Sector Average': {
                            '2017': float(sector_avg['2017']) if pd.notna(sector_avg['2017']) else None,
                            '2018': float(sector_avg['2018']) if pd.notna(sector_avg['2018']) else None,
                            '2019': float(sector_avg['2019']) if pd.notna(sector_avg['2019']) else None,
                            '2020': float(sector_avg['2020']) if pd.notna(sector_avg['2020']) else None,
                            '2021': float(sector_avg['2021']) if pd.notna(sector_avg['2021']) else None,
                            '2022': float(sector_avg['2022']) if pd.notna(sector_avg['2022']) else None
                        }
                    }
                    
                    for _, subsector_row in subsector_avgs.iterrows():
                        subsector_data = {
                            'Sub-Sector': subsector_row['Sub-Sector']
                        }
                        for year in selected_years:
                            subsector_data[year] = round(float(subsector_row[year]), 2) if pd.notna(subsector_row[year]) else None
                        
                        subsector_orgs = sector_df[sector_df['Sub-Sector'] == subsector_row['Sub-Sector']]
                        org_details = []
                        for _, org in subsector_orgs.iterrows():
                            org_entry = {
                                'Org_Name': org['Org Name']
                            }
                            for year in selected_years:
                                org_entry[year] = round(float(org[year]), 2) if pd.notna(org[year]) else None
                            org_details.append(org_entry)
                        
                        sector_data['Subsector_Averages'].append(subsector_data)
                    
                    result.append(sector_data)
                
                return Response(result, status=status.HTTP_200_OK)

            # Retain remaining existing code for other scenarios
            df = df[['Sector', 'Sub-Sector', 'Org Name', 'Indicator', 'Sub Indicator', 'Sub-Sub Indicator'] + selected_years]

            if df.empty:
                return Response({"message": "No data found matching the criteria."}, status=status.HTTP_404_NOT_FOUND)

            selected_columns = ['Sector', 'Sub-Sector', 'Org Name', 'Indicator', 
                              'Sub Indicator', 'Sub-Sub Indicator'] + selected_years

            df.fillna("N/A", inplace=True)
            result = df[selected_columns].to_dict(orient='records')

            return Response(result, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({"error": f"Unexpected error: {str(e)}"}, 
                          status=status.HTTP_500_INTERNAL_SERVER_ERROR)

























# import pandas as pd
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

#             # Add sector filtering with predefined_sectors
#             if sector == 'All':
#                 df = df[df['Sector'].isin(predefined_sectors)]
#             else:
#                 df = df[df['Sector'] == sector]

#             # Add additional filters
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
                    
#                     subsector_avgs = sector_df.groupby('Sub-Sector')[selected_years].apply(
#                         lambda x: x.apply(pd.to_numeric, errors='coerce').mean()
#                     ).reset_index()
                    
#                     sector_avg = subsector_avgs[selected_years].mean()
                    
#                     sector_data = {
#                         'Sector': sector_name,
#                         'Indicator': indicator,
#                         'Sub_Indicator': sub_indicator if sub_indicator else None,
#                         'Sub_Sub_Indicator': sub_sub_indicator if sub_sub_indicator else None,
#                         'Subsector_Averages': [],
#                         'Combined Sector Average': {
#                             '2017': float(sector_avg['2017']) if pd.notna(sector_avg['2017']) else None,
#                             '2018': float(sector_avg['2018']) if pd.notna(sector_avg['2018']) else None,
#                             '2019': float(sector_avg['2019']) if pd.notna(sector_avg['2019']) else None,
#                             '2020': float(sector_avg['2020']) if pd.notna(sector_avg['2020']) else None,
#                             '2021': float(sector_avg['2021']) if pd.notna(sector_avg['2021']) else None,
#                             '2022': float(sector_avg['2022']) if pd.notna(sector_avg['2022']) else None
#                         }
#                     }
                    
#                     for _, subsector_row in subsector_avgs.iterrows():
#                         subsector_data = {
#                             'Sub-Sector': subsector_row['Sub-Sector']
#                         }
#                         for year in selected_years:
#                             subsector_data[year] = round(float(subsector_row[year]), 2) if pd.notna(subsector_row[year]) else None
                        
#                         subsector_orgs = sector_df[sector_df['Sub-Sector'] == subsector_row['Sub-Sector']]
#                         org_details = []
#                         for _, org in subsector_orgs.iterrows():
#                             org_entry = {
#                                 'Org_Name': org['Org Name']
#                             }
#                             for year in selected_years:
#                                 org_entry[year] = round(float(org[year]), 2) if pd.notna(org[year]) else None
#                             org_details.append(org_entry)
                        
#                         sector_data['Subsector_Averages'].append(subsector_data)
                    
#                     result.append(sector_data)
                
#                 return Response(result, status=status.HTTP_200_OK)

#             # Retain remaining existing code for other scenarios
#             df = df[['Sector', 'Sub-Sector', 'Org Name', 'Indicator', 'Sub Indicator', 'Sub-Sub Indicator'] + selected_years]

#             if df.empty:
#                 return Response({"message": "No data found matching the criteria."}, status=status.HTTP_404_NOT_FOUND)

#             selected_columns = ['Sector', 'Sub-Sector', 'Org Name', 'Indicator', 
#                               'Sub Indicator', 'Sub-Sub Indicator'] + selected_years

#             df.fillna("N/A", inplace=True)
#             result = df[selected_columns].to_dict(orient='records')

#             return Response(result, status=status.HTTP_200_OK)

#         except Exception as e:
#             return Response({"error": f"Unexpected error: {str(e)}"}, 
#                           status=status.HTTP_500_INTERNAL_SERVER_ERROR)