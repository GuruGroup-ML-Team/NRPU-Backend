import pandas as pd
from rest_framework.response import Response
from rest_framework.decorators import api_view
import re
from rest_framework import status

@api_view(['POST','GET'])
def financial_market_data(request):
    try:
        # Log incoming request data
        print("Request method:", request.method)
        print("Request data (POST):", request.data)
        print("Request data (GET):", request.GET)

        # Retrieve query parameters
        sector = request.data.get('sector', request.GET.get('sector', 'All'))
        sub_sector = request.data.get('sub_sector', request.GET.get('sub_sector', 'All'))
        org_name = request.data.get('org_name', request.GET.get('org_name', 'All'))
        indicator = request.data.get('indicator', request.GET.get('indicator', 'All'))
        sub_indicator = request.data.get('sub_indicator', request.GET.get('sub_indicator', 'All'))
        sub_sub_indicator = request.data.get('sub_sub_indicator', request.GET.get('sub_sub_indicator', 'All'))
        year = request.data.get('year', request.GET.get('year', 'All'))

        # Validate input fields
        if not (sector and indicator and year):
            return Response({"error": "Sector, indicator, and year are required."}, status=status.HTTP_400_BAD_REQUEST)

        # Define column names
        columns = ['Sector', 'Sub-Sector', 'Org Name', 'Indicator', 'Sub Indicator', 'Sub-Sub Indicator', '2017', '2018', '2019', '2020', '2021', '2022']

        # Load Excel data
        try:
            file_path = 'Data/input_data.xlsx'  # Make sure this file is in your project directory
            df = pd.read_excel(file_path, header=None, names=columns)
        except Exception as e:
            return Response({"error": f"Error loading the Excel file: {str(e)}"}, status=500)

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

        # Apply filters based on query parameters
        filters = []
        if sector != 'All':
            filters.append(df['Sector'] == sector)
        if sub_sector != 'All':
            filters.append(df['Sub-Sector'] == sub_sector)
        if org_name != 'All':
            filters.append(df['Org Name'] == org_name)
        if indicator != 'All':
            filters.append(df['Indicator'].str.contains(f"{re.escape(indicator)}", case=False, na=False))
        if sub_indicator != 'All':
            filters.append(df['Sub Indicator'].str.contains(f"{re.escape(sub_indicator)}", case=False, na=False))
        if sub_sub_indicator != 'All':
            filters.append(df['Sub-Sub Indicator'].str.contains(f"{re.escape(sub_sub_indicator)}", case=False, na=False))

        # Filter data based on selected criteria
        try:
            data = df.loc[pd.concat(filters, axis=1).all(axis=1)] if filters else df  # No filters applied selects all data
        except Exception as e:
            return Response({"error": f"Error filtering the data: {str(e)}"}, status=500)

        # Calculate sum and average for each selected year
        result = {
            "sector": sector,
            "sub_sector": sub_sector,
            "org_name": org_name,
            "indicator": indicator,
            "sub_indicator": sub_indicator,
            "sub_sub_indicator": sub_sub_indicator,
            "year": year
        }

        year_results = {}
        for year in selected_years:
            try:
                data[year] = pd.to_numeric(data[year], errors='coerce')
                total_sum = data[year].sum()
                count = data[year].count()
                average = total_sum / count if count != 0 else None
                year_results[year] = {
                    "sum": total_sum,
                    "average": average
                }
            except Exception as e:
                return Response({"error": f"Error calculating sum/average for year {year}: {str(e)}"}, status=500)

        result["year_data"] = year_results

        return Response(result, status=status.HTTP_200_OK)

    except Exception as e:
        return Response({"error": f"Unexpected error: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
