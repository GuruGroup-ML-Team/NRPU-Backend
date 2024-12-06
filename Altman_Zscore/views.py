from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import pandas as pd
import numpy as np


class Altman_Zscore(APIView):
    """
    API to calculate Altman Z-Score and return filtered data based on
    Sector, Sub-Sector, Org Name, and Year.
    """

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        try:
            # Load the initial dataset
            self.df_pivot = pd.read_excel("Data/input_data.xlsx")
            print("Dataset loaded successfully.")
            print(self.df_pivot.columns)  # Print the columns of the dataframe
        except Exception as e:
            print(f"Error loading dataset: {str(e)}")
            self.df_pivot = pd.DataFrame()  # Set an empty DataFrame if loading fails

    def calculate_altman_score(self, df_filtered):
        """
        Method to calculate Altman Z-Scores for all available years in the dataset.
        """
        print("Inside calculate_altman_score method")

        # Define the mapping of Sub Indicators to components
        zscore_components = {
            '1. capital work in progress': 'wc',
            'total assets (a+b) / equity & liabilities (c+d+e)': 'ta',
            '2. retention in business (f10-f11-f12)': 're',
            '6. ebit (f3-f4+f5)': 'ebit',
            '2. cost of sales': 'mve',
            '5. total fixed liabilities (d1+d3)': 'tl'
        }

        # Extract all year columns
        year_columns = [col for col in df_filtered.columns if col.isdigit()]
        altman_scores = {}

        for year in year_columns:
            components = {key: None for key in zscore_components.values()}

            # Populate components for the current year
            for _, row in df_filtered.iterrows():
                sub_indicator = row['Sub Indicator'].strip().lower()
                if sub_indicator in zscore_components:
                    component_key = zscore_components[sub_indicator]
                    components[component_key] = row.get(year, None)

            print(f"Components for year {year}:")
            print(components)

            # Remove components with None or zero values
            valid_components = {key: value for key, value in components.items() if value not in (None, 0)}

            if not all(key in valid_components for key in ['ta', 'tl']):
                altman_scores[year] = "Insufficient data"
                continue

            # Calculate ratios and Altman Z-Score
            try:
                x1 = valid_components.get('wc', 0) / valid_components['ta'] if 'wc' in valid_components else 0
                x2 = valid_components.get('re', 0) / valid_components['ta'] if 're' in valid_components else 0
                x3 = valid_components.get('ebit', 0) / valid_components['ta'] if 'ebit' in valid_components else 0
                x4 = valid_components.get('mve', 0) / valid_components['tl'] if 'mve' in valid_components else 0

                altman_zscore = (
                    (6.56 * x1) + 
                    (3.26 * x2) + 
                    (6.72 * x3) + 
                    (1.05 * x4)
                )
                altman_scores[year] = altman_zscore
            except Exception as e:
                print(f"Error in calculating Altman Z-Score for year {year}: {str(e)}")
                altman_scores[year] = f"Error: {str(e)}"

        return altman_scores

    def post(self, request):
        """
        POST method to filter data and calculate Altman Z-Score using predefined sub-indicators,
        returning only the first occurrence of each sub-indicator, including handling repeated sub-indicators like 'Cost of Sales'.
        """
        try:
            # Get filter criteria from the request
            filters = request.data
            sector = filters.get('sector', None)
            sub_sector = filters.get('sub_sector', None)
            org_name = filters.get('org_name', None)
            year = filters.get('year', None)

            # Predefined list of sub-indicators
            predefined_sub_indicators = [
                "    1. Capital work in progress",
                " Total Assets (A+B) / Equity & Liabilities (C+D+E)",
                "    2. Retention in business (F10-F11-F12)",
                "    6. EBIT (F3-F4+F5)",
                "    2. Cost of sales",
                "    5. Total fixed liabilities (D1+D3)"
            ]

            # Predefined list of sectors
            predefined_sectors = [
                "Textile Sector", "Sugar", "Food", "Chemicals, Chemical Products and Pharmaceuticals",
                "Manufacturing", "Mineral products", "Cement", "Motor Vehicles, Trailers & Autoparts",
                "Fuel and Energy Sector", "Information and Communication Services", 
                "Coke and Refined Petroleum Products", "Paper, Paperboard and Products",
                "Electrical Machinery and Apparatus", "Other Services Activities"
            ]

            # Debugging: Check if DataFrame is loaded correctly
            filtered_df = self.df_pivot
            print("Before filtering:")
            print(filtered_df.head())

            if sector and sector.lower() == "all":
                if not year or year.lower() == "all":
                    return Response(
                        {"error": "Year must be specified when sector is 'All'."},
                        status=status.HTTP_400_BAD_REQUEST
                    )

                # Calculate Altman Z-Score for all predefined sectors
                zscore_results = {}
                for sec in predefined_sectors:
                    sector_df = filtered_df[filtered_df['Sector'] == sec]
                    sector_df = sector_df[sector_df['Sub Indicator'].isin(predefined_sub_indicators)]
                    sector_df['Sub Indicator'] = sector_df['Sub Indicator'].str.strip().str.lower()
                    sector_df = sector_df.drop_duplicates(subset=['Sub Indicator'], keep='first')
                    zscore = self.calculate_altman_score(sector_df)
                    zscore_results[sec] = zscore.get(year, "Insufficient data or error in calculation")

                response_data = {
                    "sector": "All",
                    "year": year,
                    "altman_zscore": zscore_results
                }
                return Response(response_data, status=status.HTTP_200_OK)

            # Apply filters for specific sector, sub-sector, and org_name
            if sector:
                filtered_df = filtered_df[filtered_df['Sector'] == sector]
            if sub_sector:
                filtered_df = filtered_df[filtered_df['Sub-Sector'] == sub_sector]
            if org_name:
                filtered_df = filtered_df[filtered_df['Org Name'] == org_name]

            # Filter based on predefined sub-indicators
            filtered_df = filtered_df[filtered_df['Sub Indicator'].isin(predefined_sub_indicators)]
            filtered_df['Sub Indicator'] = filtered_df['Sub Indicator'].str.strip().str.lower()
            filtered_df = filtered_df.drop_duplicates(subset=['Sub Indicator'], keep='first')

            # Apply year filter if specified
            if year and year != "all":
                filtered_df = filtered_df[['Sector', 'Sub-Sector', 'Org Name', 'Indicator', 'Sub Indicator', year]]
                if filtered_df.empty:
                    return Response(
                        {"message": f"No data found for the year {year} with the selected filters."},
                        status=status.HTTP_404_NOT_FOUND
                    )

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
                    "year": year,
                    "altman_zscore": altman_zscore
                }

            return Response(response_data, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
