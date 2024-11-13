import pandas as pd
import os
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status

@api_view(['POST'])
def economic_data(request):
    try:
        # Retrieve query parameters from POST data
        year = request.data.get('year', 'All')
        indicator = request.data.get('indicator', 'All')

        # Load the Excel file
        file_path = 'Data/Economic_Data.xlsx'
        if not os.path.exists(file_path):
            return Response({"error": "Data file not found."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        # Load the Excel sheet and skip any initial rows if necessary
        df = pd.read_excel(file_path, skiprows=1)

        # Rename 'Unnamed: 0' to 'Years' for easier access
        df.rename(columns={'Unnamed: 0': 'Years'}, inplace=True)

        # Handle filtering based on input
        data = df  # Start with the full dataset

        # If a specific year is requested, filter by that year
        if year != 'All':
            data = data[data['Years'] == int(year)]
            if data.empty:
                return Response({"error": f"No data found for the year {year}."}, status=status.HTTP_404_NOT_FOUND)

        # If a specific indicator is requested, filter by that indicator column
        if indicator != 'All':
            if indicator not in df.columns:
                return Response({"error": f"Indicator '{indicator}' not found."}, status=status.HTTP_400_BAD_REQUEST)
            data = data[['Years', indicator]]  # Keep only the year and requested indicator

        # Prepare the response in the required format, replacing missing values
        result_data = []
        for _, row in data.iterrows():
            # Ensure each indicator has a value, replacing NaN with `null` or "Data not available"
            row_data = {key: (value if pd.notna(value) else None) for key, value in row.items()}
            result_data.append(row_data)

        result = {
            "year": year,
            "indicator": indicator,
            "data": result_data
        }

        # Check if any data was found
        if not result["data"]:
            return Response({"error": "No data found for the provided criteria."}, status=status.HTTP_404_NOT_FOUND)

        return Response(result, status=status.HTTP_200_OK)

    except Exception as e:
        return Response({"error": f"Unexpected error: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
