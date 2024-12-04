import pandas as pd
import os
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from datetime import datetime

@api_view(['POST'])
def economic_data(request):
    try:
        # Retrieve query parameters from POST data
        year = request.data.get('year')  # Can be None, a single value, or a list
        indicator = request.data.get('indicator')  # No default; will be None if not provided

        # Load the Excel file
        file_path = 'Data/Economic_Data.xlsx'
        if not os.path.exists(file_path):
            return Response({"error": "Data file not found."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        df = pd.read_excel(file_path, skiprows=1)
        df.rename(columns={'Unnamed: 0': 'Years'}, inplace=True)

        # Start with the full dataset
        data = df

        # Handle year filtering
        if year:
            if isinstance(year, list):
                # Filter data for all years in the list
                year = [int(y) for y in year if str(y).isdigit()]
                data = data[data['Years'].isin(year)]
                if data.empty:
                    return Response({"error": f"No data found for the years {year}."}, status=status.HTTP_404_NOT_FOUND)
            else:
                # Handle single year
                year = int(year)
                data = data[data['Years'] == year]
                if data.empty:
                    return Response({"error": f"No data found for the year {year}."}, status=status.HTTP_404_NOT_FOUND)

        # Handle indicator filtering
        if indicator:
            if indicator not in df.columns:
                return Response({"error": f"Indicator '{indicator}' not found."}, status=status.HTTP_400_BAD_REQUEST)
            data = data[['Years', indicator]]  # Keep only the year and requested indicator
        else:
            # If no specific indicator, include all indicators
            data = data

        # Prepare the response data, replacing missing values with None
        result_data = []
        for _, row in data.iterrows():
            row_data = {key: (value if pd.notna(value) else None) for key, value in row.items()}
            result_data.append(row_data)

        # Construct the response
        result = {
            "years": year if year else "All",
            "indicator": indicator if indicator else "All",
            "data": result_data,
        }

        # If no data was found after filtering, return a 404 response
        if not result["data"]:
            return Response({"error": "No data found for the provided criteria."}, status=status.HTTP_404_NOT_FOUND)

        return Response(result, status=status.HTTP_200_OK)

    except Exception as e:
        return Response({"error": f"Unexpected error: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
