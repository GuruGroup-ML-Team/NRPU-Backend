# import pandas as pd
# from rest_framework.response import Response
# from rest_framework.views import APIView
# from rest_framework import status
# import re

# class FinancialStatementAnalysisView(APIView):
#     def get(self, request):
#         try:
#             # Log incoming request data
#             print("Request data (GET):", request.query_params)

#             # Retrieve query parameters
#             sector = request.query_params.get('sector', 'All')
#             sub_sector = request.query_params.get('sub_sector', 'All')
#             org_name = request.query_params.get('org_name', 'All')
#             indicator = request.query_params.get('indicator', 'All')
#             sub_indicator = request.query_params.get('sub_indicator', None)
#             sub_sub_indicator = request.query_params.get('sub_sub_indicator', None)
#             year = request.query_params.get('year', 'All')

#             # Validate input fields
#             if not year:
#                 return Response({"error": "Year is required."}, status=status.HTTP_400_BAD_REQUEST)

#             # Define column names
#             columns = ['Sector', 'Sub-Sector', 'Org Name', 'Indicator', 'Sub Indicator', 'Sub-Sub Indicator', 
#                        '2017', '2018', '2019', '2020', '2021', '2022']

#             # Load Excel data
#             try:
#                 file_path = 'Data/input_data.xlsx'  # Adjust path as needed
#                 df = pd.read_excel(file_path, header=None, names=columns)
#             except Exception as e:
#                 return Response({"error": f"Error loading the Excel file: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

#             # Trim whitespace from relevant columns
#             df['Indicator'] = df['Indicator'].str.strip()

#             # Convert year column to string and handle 'All' selection for year
#             year_columns = ['2017', '2018', '2019', '2020', '2021', '2022']
#             if year == 'All':
#                 selected_years = year_columns
#             elif year in year_columns:
#                 selected_years = [year]
#             else:
#                 return Response({"error": "Invalid year specified"}, status=status.HTTP_400_BAD_REQUEST)

#             # Predefined sectors when 'All' is selected
#             predefined_sectors = [
#                 "Textile Sector", "Sugar", "Food", "Chemicals, Chemical Products and Pharmaceuticals",
#                 "Manufacturing", "Mineral products", "Cement", "Motor Vehicles, Trailers & Autoparts",
#                 "Fuel and Energy Sector", "Information and Communication Services", 
#                 "Coke and Refined Petroleum Products", "Paper, Paperboard and Products",
#                 "Electrical Machinery and Apparatus", "Other Services Activities"
#             ]

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
#             return Response({"error": f"Unexpected error: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)











import pandas as pd
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from urllib.parse import unquote

class FinancialStatementAnalysisView(APIView):
    def calculate_averages(self, df, query_params):
        filtered_df = df.copy()
        year_columns = ['2017', '2018', '2019', '2020', '2021', '2022']
        selected_year = query_params.get('year', 'All')
        
        #determine the level of hierarchy specified in query params
        hierarchy_level = 0
        if query_params.get('sector') != 'All':
            hierarchy_level = 1
            if query_params.get('sub_sector') != 'All':
                hierarchy_level = 2
                if query_params.get('indicator') != 'All':
                    hierarchy_level = 3
                    if query_params.get('sub_indicator') != 'All':
                        hierarchy_level = 4
                        if query_params.get('sub_sub_indicator') != 'All':
                            hierarchy_level = 5

        print(f"Detected hierarchy level: {hierarchy_level}")
        
        # Apply filters based on hierarchy level
        if hierarchy_level >= 1:
            filtered_df = filtered_df[filtered_df['Sector'].str.lower() == query_params['sector'].lower()]
        
        if hierarchy_level >= 2:
            filtered_df = filtered_df[filtered_df['Sub-Sector'].str.lower() == query_params['sub_sector'].lower()]
        
        if hierarchy_level >= 3:
            query_indicator = query_params['indicator'].replace(' ', '+')
            filtered_df = filtered_df[filtered_df['Indicator'].str.replace(' ', '+').str.lower() == query_indicator.lower()]
            
            # If only sector, sub_sector, and indicator are specified, ensure sub_indicator and sub_sub_indicator are empty
            if hierarchy_level == 3:
                filtered_df = filtered_df[
                    (filtered_df['Sub Indicator'].isna()) | 
                    (filtered_df['Sub Indicator'].str.strip() == '') |
                    (filtered_df['Sub Indicator'].str.lower() == 'nan')
                ]
                filtered_df = filtered_df[
                    (filtered_df['Sub-Sub Indicator'].isna()) | 
                    (filtered_df['Sub-Sub Indicator'].str.strip() == '') |
                    (filtered_df['Sub-Sub Indicator'].str.lower() == 'nan')
                ]
        
        if hierarchy_level >= 4:
            filtered_df = filtered_df[filtered_df['Sub Indicator'].str.lower() == query_params['sub_indicator'].lower()]
            
            # If only up to sub_indicator is specified, ensure sub_sub_indicator is empty
            if hierarchy_level == 4:
                filtered_df = filtered_df[
                    (filtered_df['Sub-Sub Indicator'].isna()) | 
                    (filtered_df['Sub-Sub Indicator'].str.strip() == '') |
                    (filtered_df['Sub-Sub Indicator'].str.lower() == 'nan')
                ]
        
        if hierarchy_level == 5:
            filtered_df = filtered_df[filtered_df['Sub-Sub Indicator'].str.lower() == query_params['sub_sub_indicator'].lower()]

        print(f"Filtered DataFrame shape: {filtered_df.shape}")
        print("Sample of filtered data:")
        print(filtered_df[['Sector', 'Sub-Sector', 'Indicator', 'Sub Indicator', 'Sub-Sub Indicator']].head())
        
        if not filtered_df.empty:
            results = []
            
            # Determine grouping columns based on hierarchy level
            used_columns = []
            if hierarchy_level >= 1:
                used_columns.append('Sector')
            if hierarchy_level >= 2:
                used_columns.append('Sub-Sector')
            if hierarchy_level >= 3:
                used_columns.append('Indicator')
            if hierarchy_level >= 4:
                used_columns.append('Sub Indicator')
            if hierarchy_level == 5:
                used_columns.append('Sub-Sub Indicator')
            
            # If no parameters provided, use all data
            if not used_columns:
                used_columns = ['Sector']
            
            # Group by the used columns
            grouped = filtered_df.groupby(used_columns)
            
            for group_name, group_df in grouped:
                result = {}
                
                # Handle both single string and tuple group names
                if isinstance(group_name, tuple):
                    for col, value in zip(used_columns, group_name):
                        result[col] = value
                else:
                    result[used_columns[0]] = group_name
                
                # Calculate averages based on year selection
                if selected_year.lower() != 'all':
                    year_values = group_df[selected_year].dropna()
                    result[selected_year] = float(year_values.mean()) if not year_values.empty else None
                    result['sample_size'] = len(year_values)
                else:
                    for year in year_columns:
                        year_values = group_df[year].dropna()
                        result[year] = float(year_values.mean()) if not year_values.empty else None
                    result['sample_size'] = len(group_df)
                
                results.append(result)
            
            return results
        return []
    def get(self, request):
        try:
            columns = ['Sector', 'Sub-Sector', 'Org Name', 'Indicator', 'Sub Indicator', 
                      'Sub-Sub Indicator', '2017', '2018', '2019', '2020', '2021', '2022']
            try:
                df = pd.read_excel('Data/input_data 5.xlsx', header=None, names=columns)
                # Clean the data by stripping whitespace
                for col in ['Sector', 'Sub-Sector', 'Indicator', 'Sub Indicator', 'Sub-Sub Indicator']:
                    df[col] = df[col].astype(str).str.strip()
                print("Successfully loaded data with shape:", df.shape)
            except Exception as e:
                return Response(
                    {"error": f"Error loading Excel file: {str(e)}"}, 
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR
                )

            year_columns = ['2017', '2018', '2019', '2020', '2021', '2022']
            for year_col in year_columns:
                df[year_col] = pd.to_numeric(df[year_col], errors='coerce')


            query_params = {
                'sector': unquote(request.query_params.get('sector', 'All')),
                'sub_sector': unquote(request.query_params.get('sub_sector', 'All')),
                'indicator': unquote(request.query_params.get('indicator', 'All')),
                'sub_indicator': unquote(request.query_params.get('sub_indicator', 'All')),
                'sub_sub_indicator': unquote(request.query_params.get('sub_sub_indicator', 'All')),
                'year': request.query_params.get('year', 'All')
            }

            
            print("\nReceived query parameters:")
            for key, value in query_params.items():
                print(f"{key}: {value}")

            # Calculate results
            results = self.calculate_averages(df, query_params)

            if not results:
                return Response(
                    {
                        "message": "No data found matching the criteria.",
                        "query_params": query_params,
                        "debug_info": {
                            "total_rows": len(df),
                            "available_values": {
                                "sectors": df['Sector'].unique().tolist(),
                                "sub_sectors": df['Sub-Sector'].unique().tolist(),
                                "indicators": df['Indicator'].unique().tolist(),
                                "sub_indicators": df['Sub Indicator'].unique().tolist(),
                                "sub_sub_indicators": df['Sub-Sub Indicator'].unique().tolist()
                            }
                        }
                    }, 
                    status=status.HTTP_404_NOT_FOUND
                )

            return Response(results, status=status.HTTP_200_OK)

        except Exception as e:
            return Response(
                {"error": f"Unexpected error: {str(e)}"}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
