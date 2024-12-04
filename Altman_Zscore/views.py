

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
        Method to calculate Altman Z-Score based on the available financial indicators.
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

        # Initialize the components dictionary
        components = {key: 0 for key in zscore_components.values()}

        # Iterate over the filtered DataFrame and populate components
        for _, row in df_filtered.iterrows():
            sub_indicator = row['Sub Indicator'].strip().lower()
            if sub_indicator in zscore_components:
                component_key = zscore_components[sub_indicator]
                components[component_key] = row['2020']

        print("Components after extraction:")
        print(components)

        # Check if any key has a value of zero to avoid division by zero
        if components['ta'] == 0 or components['tl'] == 0:
            return {"error": "Division by zero error: 'Total Assets' or 'Total Liabilities' is zero."}

        # Calculate ratios
        try:
            x1 = components['wc'] / components['ta']
            x2 = components['re'] / components['ta']
            x3 = components['ebit'] / components['ta']
            x4 = components['mve'] / components['tl']

            # Calculate the Altman Z-Score using the given formula
            altman_zscore = (
                (6.56 * x1) +  # Working Capital / Total Assets
                (3.26 * x2) +  # Retained Earnings / Total Assets
                (6.72 * x3) +  # EBIT / Total Assets
                (1.05 * x4)    # Market Value of Equity / Total Liabilities
            )

            return altman_zscore
        except Exception as e:
            print(f"Error in calculating Altman Z-Score: {str(e)}")
            return {"error": f"Error calculating Altman Z-Score: {str(e)}"}
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

            # Filter the DataFrame based on sector, sub-sector, org_name, and year
            filtered_df = self.df_pivot

            # Debugging: Check if DataFrame is loaded correctly
            print("Before filtering:")
            print(filtered_df.head())

            # Apply filters
            if sector:
                filtered_df = filtered_df[filtered_df['Sector'] == sector]
            if sub_sector:
                filtered_df = filtered_df[filtered_df['Sub-Sector'] == sub_sector]
            if org_name:
                filtered_df = filtered_df[filtered_df['Org Name'] == org_name]

            # Filter based on predefined sub-indicators
            filtered_df = filtered_df[filtered_df['Sub Indicator'].isin(predefined_sub_indicators)]

            # Apply year filter if specified
            if year:
                filtered_df = filtered_df[['Sector', 'Sub-Sector', 'Org Name', 'Indicator', 'Sub Indicator', year]]

            # Clean up the "Sub Indicator" column
            filtered_df['Sub Indicator'] = filtered_df['Sub Indicator'].str.strip().str.lower()

            # Drop duplicate sub-indicators and keep only the first occurrence
            filtered_df = filtered_df.drop_duplicates(subset=['Sub Indicator'], keep='first')

            # Debugging: Check the DataFrame after dropping duplicates
            print("After Filtering duplicates:")
            print(filtered_df)

            # If no data found after filtering
            if filtered_df.empty:
                return Response({"message": "No data found for the selected filters."}, status=status.HTTP_404_NOT_FOUND)

           # Calculate Altman Z-Score
            altman_zscore = self.calculate_altman_score(filtered_df)

            # If no valid Altman Z-Score can be calculated, return an error
            if isinstance(altman_zscore, dict) and "error" in altman_zscore:
                return Response({"message": altman_zscore["error"]}, status=status.HTTP_400_BAD_REQUEST)

            # Return the Altman Z-Score in the response
            return Response({"altman_zscore": altman_zscore}, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
