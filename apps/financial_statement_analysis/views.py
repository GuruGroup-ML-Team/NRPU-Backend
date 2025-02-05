import pandas as pd
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
import re


class FinancialStatementAnalysisView(APIView):
    def get(self, request):
        try:
            # Log incoming request data
            print("Request data (GET):", request.query_params)

            # Retrieve query parameters
            sector = request.query_params.get('sector', 'All')
            sub_sector = request.query_params.get('sub_sector', 'All')
            org_name = request.query_params.get('org_name', 'All')
            indicator = request.query_params.get('indicator', 'All')
            sub_indicator = request.query_params.get('sub_indicator', None)
            sub_sub_indicator = request.query_params.get('sub_sub_indicator', None)
            year = request.query_params.get('year', 'All')

            # Validate input fields
            if not year:
                return Response({"error": "Year is required."}, status=status.HTTP_400_BAD_REQUEST)

            # Define column names
            columns = ['Sector', 'Sub-Sector', 'Org Name', 'Indicator', 'Sub Indicator', 'Sub-Sub Indicator', 
                       '2017', '2018', '2019', '2020', '2021', '2022']

            # Load Excel data
            try:
                file_path = 'Data/input_data.xlsx'  # Adjust path as needed
                df = pd.read_excel(file_path, header=None, names=columns)
            except Exception as e:
                return Response({"error": f"Error loading the Excel file: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

            # Trim whitespace from relevant columns
            df['Indicator'] = df['Indicator'].str.strip()

            # Convert year column to string and handle 'All' selection for year
            year_columns = ['2017', '2018', '2019', '2020', '2021', '2022']
            if year == 'All':
                selected_years = year_columns
            elif year in year_columns:
                selected_years = [year]
            else:
                return Response({"error": "Invalid year specified"}, status=status.HTTP_400_BAD_REQUEST)

            # Predefined sectors when 'All' is selected
            predefined_sectors = [
                "Textile Sector", "Sugar", "Food", "Chemicals, Chemical Products and Pharmaceuticals",
                "Manufacturing", "Mineral products", "Cement", "Motor Vehicles, Trailers & Autoparts",
                "Fuel and Energy Sector", "Information and Communication Services", 
                "Coke and Refined Petroleum Products", "Paper, Paperboard and Products",
                "Electrical Machinery and Apparatus", "Other Services Activities"
            ]

            if indicator == 'All':
                if sector == 'All':
                    df = df.drop_duplicates(subset=['Sector', 'Indicator'], keep='first').reset_index(drop=True)
                else:
                    df = df[df['Sector'] == sector].drop_duplicates(subset=['Indicator'], keep='first').reset_index(drop=True)
                df = df[['Sector', 'Sub-Sector', 'Org Name', 'Indicator', 'Sub Indicator', 'Sub-Sub Indicator'] + selected_years]
            
            elif sector == 'All':
                df = df[df['Indicator'].str.contains(f"{re.escape(indicator)}", case=False, na=False)]

                if sub_indicator:
                    df = df[df['Sub Indicator'].str.contains(f"{re.escape(sub_indicator)}", case=False, na=False)]
                if sub_sub_indicator:
                    df = df[df['Sub-Sub Indicator'].str.contains(f"{re.escape(sub_sub_indicator)}", case=False, na=False)]

                df = df.drop_duplicates(subset=['Sector', 'Indicator'], keep='first')

                df = df[['Sector', 'Sub-Sector', 'Org Name', 'Indicator', 'Sub Indicator', 'Sub-Sub Indicator'] + selected_years]

            else:
                if sector == 'All':
                    df = df[df['Sector'].isin(predefined_sectors)]
                else:
                    df = df[df['Sector'] == sector]

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

                df = df.drop_duplicates(subset=['Indicator'], keep='first')

                df = df[['Sector', 'Sub-Sector', 'Org Name', 'Indicator', 'Sub Indicator', 'Sub-Sub Indicator'] + selected_years]

            if df.empty:
                return Response({"message": "No data found matching the criteria."}, status=status.HTTP_404_NOT_FOUND)

            selected_columns = ['Sector', 'Sub-Sector', 'Org Name', 'Indicator', 
                                'Sub Indicator', 'Sub-Sub Indicator'] + selected_years

            df.fillna("N/A", inplace=True)
            result = df[selected_columns].to_dict(orient='records')

            return Response(result, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({"error": f"Unexpected error: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
