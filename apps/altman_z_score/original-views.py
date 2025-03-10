from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import pandas as pd
import numpy as np

class AltmanZScoreView(APIView):
    """
    API to calculate Altman Z-Score and return filtered data based on
    Sector, Sub-Sector, Org Name, and Year.
    """
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        try:
            # Load the primary dataset
            self.df_pivot = pd.read_excel("Data/input_data.xlsx")
            # Load sector-wise average dataset (if available)
            self.df_sector_avg = pd.read_excel("Data/altman_sector_averages.xlsx")  # Example file
            print("Datasets loaded successfully.")
        except Exception as e:
            print(f"Error loading datasets: {str(e)}")
            self.df_pivot = pd.DataFrame()  # Fallback to empty DataFrame
            self.df_sector_avg = pd.DataFrame()  # Fallback for averages

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

    def get_sector_averages(self, sector, year):
        """
        Retrieve the sector-wise average Altman Z-Score for a specific year or all years.
        """
        try:
            # Filter the dataset for the given sector
            if sector != "all":
                averages_df = self.df_sector_avg[self.df_sector_avg['Sector'] == sector]
            else:
                averages_df = self.df_sector_avg

            # Filter by year if specified
            if year and year.lower() != "all":
                year_column = f"AltmanZscore {year}"
                if year_column not in self.df_sector_avg.columns:
                    return {"error": f"Year {year} is not available in the dataset."}

                # Select only the relevant year column and average row
                averages_df = averages_df[averages_df['Org Name'] == 'Sector Average'][['Sector', year_column]]
                return averages_df.rename(columns={year_column: "AltmanZscore"}).to_dict(orient="records")
            else:
                # Return all year columns for the averages row
                averages_df = averages_df[averages_df['Org Name'] == 'Sector Average']
                averages_df = averages_df.drop(columns=['Sub-Sector', 'Org Name'], errors='ignore')
                return averages_df.to_dict(orient="records")

        except Exception as e:
            print(f"Error retrieving sector averages: {str(e)}")
            return {"error": str(e)}


    def get(self, request):
        """
        GET method to return Altman Z-Scores or sector-wise averages based on filters.
        """
        try:
            # Get filter criteria from the query parameters
            sector = request.query_params.get('sector', None)
            sub_sector = request.query_params.get('sub_sector', None)
            org_name = request.query_params.get('org_name', None)
            year = request.query_params.get('year', None)

            # Predefined list of sub-indicators
            predefined_sub_indicators = [
                "    1. Capital work in progress",
                " Total Assets (A+B) / Equity & Liabilities (C+D+E)",
                "    2. Retention in business (F10-F11-F12)",
                "    6. EBIT (F3-F4+F5)",
                "    2. Cost of sales",
                "    5. Total fixed liabilities (D1+D3)"
            ]

            if sector and sector.lower() == "all":
                # Fetch pre-calculated sector-wise averages
                sector_avg_scores = self.get_sector_averages("all", year)
                return Response(
                    {
                        "sector": "All",
                        "year": year,
                        "sector_avg_scores": sector_avg_scores
                    },
                    status=status.HTTP_200_OK
                )

            # Filter the primary dataset for specific sector, sub-sector, and org_name
            filtered_df = self.df_pivot
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


