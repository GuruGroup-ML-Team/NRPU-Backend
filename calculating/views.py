# calculations/views.py
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
import pandas as pd
import re

@api_view(['POST'])
def calculate_indicator(request):
    try:
        # Get parameters from the request data
        sector = request.data.get('sector')
        year = request.data.get('year')
        indicator = request.data.get('indicator')
        sub_indicator = request.data.get('sub_indicator')
        file_path = 'Data/Dummy-Data.xlsx'  # Update with actual path to your Excel file

        # Validate input fields
        if not (sector and year and indicator and sub_indicator):
            return Response({"error": "All fields (sector, year, indicator, sub_indicator) are required."},
                            status=status.HTTP_400_BAD_REQUEST)

        # Load Excel data
        columns = ['Sector', 'Item Name', '2017', '2018', '2019', '2020', '2021', '2022']
        df = pd.read_excel(file_path, header=None, names=columns)
        
        # Trim whitespace from 'Item Name'
        df['Item Name'] = df['Item Name'].str.strip()

        # Ensure the year is valid
        year_str = str(year)
        if year_str not in df.columns:
            return Response({"error": "Year must be between 2017 and 2022."}, status=status.HTTP_400_BAD_REQUEST)

        # Step 1: Filter by sector
        sector_data = df[df['Sector'] == sector]

        # Step 2: Filter within the sector for the indicator
        indicator_data = sector_data[sector_data['Item Name'].str.contains(f"^{re.escape(indicator)}$", case=False, na=False)]

        # Step 3: Further filter for the sub-indicator
        sub_indicator_data = sector_data[sector_data['Item Name'].str.contains(rf"^\s*[\d.]*\s*{re.escape(sub_indicator)}", case=False, na=False)]

        # Convert to numeric and handle errors
        indicator_data[year_str] = pd.to_numeric(indicator_data[year_str], errors='coerce')
        sub_indicator_data[year_str] = pd.to_numeric(sub_indicator_data[year_str], errors='coerce')

        # Calculate Sum and Average
        total_sum = indicator_data[year_str].sum() + sub_indicator_data[year_str].sum()
        count = indicator_data[year_str].count() + sub_indicator_data[year_str].count()
        average = total_sum / count if count != 0 else None

        # Prepare result
        result = {
            "sector": sector,
            "indicator": indicator,
            "sub_indicator": sub_indicator,
            "year": year,
            "sum": total_sum,
            "average": average
        }

        return Response(result, status=status.HTTP_200_OK)
    
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)