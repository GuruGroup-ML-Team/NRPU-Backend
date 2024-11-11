# indicators/views.py
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

        # Validate that at least year or indicator is provided
        if year == 'All' and indicator == 'All':
            return Response({"error": "Year or indicator is required."}, status=status.HTTP_400_BAD_REQUEST)

        # Load the Excel file
        file_path = 'Data/Economic_Data.xlsx'
        if not os.path.exists(file_path):
            return Response({"error": "Data file not found."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        # Load the Excel sheet and skip any initial rows if necessary
        df = pd.read_excel(file_path, skiprows=1)

        # Rename 'Unnamed: 0' to 'Years' for easier access
        df.rename(columns={'Unnamed: 0': 'Years'}, inplace=True)

        # Debugging: Print the column names to confirm renaming
        print("Updated Excel Columns:", df.columns)

        # Filter data based on input
        data = df  # Start with the full data set

        # Apply year filter if provided
        if year != 'All':
            data = data[data['Years'] == int(year)]
            if data.empty:
                return Response({"error": f"No data found for the year {year}."}, status=status.HTTP_404_NOT_FOUND)

        # Apply indicator filter if provided
        if indicator != 'All':
            if indicator not in df.columns:
                return Response({"error": f"Indicator '{indicator}' not found."}, status=status.HTTP_400_BAD_REQUEST)
            data = data[['Years', indicator]]

        # Prepare the response in the required format
        result = {
            "year": year,
            "indicator": indicator,
            "data": data.to_dict(orient='records')
        }

        # Check if any data was found
        if not result["data"]:
            return Response({"error": "No data found for the provided criteria."}, status=status.HTTP_404_NOT_FOUND)

        return Response(result, status=status.HTTP_200_OK)

    except Exception as e:
        return Response({"error": f"Unexpected error: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
