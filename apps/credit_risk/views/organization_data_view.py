
# project_root/credit_risk/views/organization_data_view.py

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
# from OrganizationDataService import organization_data_service_instance
# from apps.credit_risk.OrganizationDataService import organization_data_service_instance
# from apps.credit_risk.services.OrganizationDataService import organization_data_service_instance
from apps.credit_risk.services.OrganizationDataService import organization_data_service_instance

import pandas as pd # Import pandas for data manipulation
import numpy as np # Import numpy for np.nan

class FetchSpecificOrgDataView(APIView):
    """
    API endpoint to fetch all variables data for a particular organization
    based on entity type, sector, sub-sector, or organization name.
    """
    def get(self, request, *args, **kwargs):
        # Extract query parameters
        entity_type = request.query_params.get('entity_type')
        sector = request.query_params.get('sector')
        sub_sector = request.query_params.get('sub_sector')
        org_name = request.query_params.get('org_name')

        # Validate entity_type
        if not entity_type or entity_type.lower() not in ['company', 'bank']:
            return Response(
                {"error": "Invalid or missing 'entity_type'. Must be 'company' or 'bank'."},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Call the service layer function
        result_df = organization_data_service_instance.fetch_data_for_specific_org(
            entity_type=entity_type,
            sector=sector,
            sub_sector=sub_sector,
            org_name=org_name
        )

        # Handle cases where no data is found by the service
        if result_df is None or result_df.empty:
            response_data = {
                "query_inputs": {
                    "entity_type": entity_type,
                    "sector": sector,
                    "sub_sector": sub_sector,
                    "org_name": org_name,
                },
                "processed_data": [] # Return empty list if no data
            }
            response_data["message"] = "No data found matching the specified criteria."
            return Response(response_data, status=status.HTTP_200_OK)

        # --- REFINED ROBUST FIX FOR NON-JSON COMPLIANT VALUES ---
        # Create a copy to ensure operations don't modify the original DataFrame
        # directly, which can sometimes lead to SettingWithCopyWarning.
        cleaned_df = result_df.copy()

        # Identify columns that are expected to contain numerical year data.
        # These are columns whose names are integers or string representations of integers.
        year_columns = [col for col in cleaned_df.columns if isinstance(col, int) or (isinstance(col, str) and str(col).isdigit())]

        for col in cleaned_df.columns:
            if col in year_columns:
                # For year columns, attempt to convert values to numeric.
                # 'errors='coerce'' will turn any non-numeric values into NaN (numpy.nan).
                cleaned_df[col] = pd.to_numeric(cleaned_df[col], errors='coerce')
            # For non-year columns, we don't apply pd.to_numeric.
            # Their original dtypes (likely 'object' for strings) will be preserved.
            # Any existing NaN in these columns will be handled by the final replace.
        
        # FINAL AND MOST RELIABLE PASS: Explicitly replace all remaining NaN (numpy.nan) with None.
        # This is applied to the entire DataFrame after all numeric coercions.
        # This handles NaNs introduced by pd.to_numeric and any existing NaNs in string columns.
        cleaned_df = cleaned_df.replace({np.nan: None})

        # Assign the fully cleaned DataFrame back
        result_df = cleaned_df
        # --- END REFINED ROBUST FIX ---

        # --- DEBUG PRINTS ---
        print("\n--- DEBUG: DataFrame Info before JSON conversion (FetchSpecificOrgDataView) ---")
        result_df.info(verbose=True, show_counts=True) # Shows column dtypes and non-null counts
        print("\n--- DEBUG: DataFrame Content before JSON conversion (FetchSpecificOrgDataView) ---")
        print(result_df.to_string()) # Print the entire DataFrame content
        print("----------------------------------------------------------------------------------\n")
        # --- END DEBUG PRINTS ---

        # Convert DataFrame to a list of dictionaries for JSON response
        processed_data = result_df.to_dict(orient='records')

        # Return the original filter inputs along with processed data
        response_data = {
            "query_inputs": {
                "entity_type": entity_type,
                "sector": sector,
                "sub_sector": sub_sector,
                "org_name": org_name,
            },
            "processed_data": processed_data
        }
        # If data was found, return 200 OK with the processed data
        return Response(response_data, status=status.HTTP_200_OK)


class FetchSectorDataView(APIView):
    """
    API endpoint to fetch complete data for all organizations in a given sector.
    """
    def get(self, request, *args, **kwargs):
        # Extract query parameters
        entity_type = request.query_params.get('entity_type')
        sector = request.query_params.get('sector')

        # Validate entity_type
        if not entity_type or entity_type.lower() not in ['company', 'bank']:
            return Response(
                {"error": "Invalid or missing 'entity_type'. Must be 'company' or 'bank'."},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Validate sector
        if not sector:
            return Response(
                {"error": "Missing 'sector' parameter. Please provide a sector to fetch data."},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Call the service layer function
        result_df = organization_data_service_instance.fetch_data_by_sector(
            entity_type=entity_type,
            sector=sector
        )

        # Handle cases where no data is found by the service
        if result_df is None or result_df.empty:
            response_data = {
                "query_inputs": {
                    "entity_type": entity_type,
                    "sector": sector,
                },
                "processed_data": []
            }
            response_data["message"] = f"No data found for the sector: '{sector}'."
            return Response(response_data, status=status.HTTP_200_OK)

        # --- REFINED ROBUST FIX FOR NON-JSON COMPLIANT VALUES ---
        cleaned_df = result_df.copy()

        year_columns = [col for col in cleaned_df.columns if isinstance(col, int) or (isinstance(col, str) and str(col).isdigit())]

        for col in cleaned_df.columns:
            if col in year_columns:
                cleaned_df[col] = pd.to_numeric(cleaned_df[col], errors='coerce')
            # No 'else' branch for non-year columns here.
            # Their original dtypes (likely 'object' for strings) will be preserved.
            # Any existing NaN in these columns will be handled by the final replace.
        
        cleaned_df = cleaned_df.replace({np.nan: None})

        result_df = cleaned_df
        # --- END REFINED ROBUST FIX ---

        # --- DEBUG PRINTS ---
        print("\n--- DEBUG: DataFrame Info before JSON conversion (FetchSectorDataView) ---")
        result_df.info(verbose=True, show_counts=True) # Shows column dtypes and non-null counts
        print("\n--- DEBUG: DataFrame Content before JSON conversion (FetchSectorDataView) ---")
        print(result_df.to_string()) # Print the entire DataFrame content
        print("----------------------------------------------------------------------------------\n")
        # --- END DEBUG PRINTS ---

        # Convert DataFrame to a list of dictionaries for JSON response
        processed_data = result_df.to_dict(orient='records')

        # Return the original filter inputs along with processed data
        response_data = {
            "query_inputs": {
                "entity_type": entity_type,
                "sector": sector,
            },
            "processed_data": processed_data
        }
        # If data was found, return 200 OK with the processed data
        return Response(response_data, status=status.HTTP_200_OK)
