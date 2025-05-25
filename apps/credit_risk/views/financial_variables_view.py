# project_root/credit_risk/views/financial_variables_views.py

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from apps.credit_risk.services.FinancialVariablesService import financial_variables_service_instance
# from services.FinancialVariablesService import financial_variables_service_instance

import pandas as pd # Import pandas for potential NaN handling if needed in views (though service handles it)

class OrgSpecificFinancialVariablesView(APIView):
    """
    API endpoint to extract specific financial variables for a particular organization.
    """
    def get(self, request, *args, **kwargs):
        # Extract query parameters
        entity_type = request.query_params.get('entity_type')
        sector = request.query_params.get('sector')
        sub_sector = request.query_params.get('sub_sector')
        org_name = request.query_params.get('org_name')
        target_year = request.query_params.get('target_year') # Can be a year (e.g., "2023") or "all"

        # Validate entity_type
        if not entity_type or entity_type.lower() not in ['company', 'bank']:
            return Response(
                {"error": "Invalid or missing 'entity_type'. Must be 'company' or 'bank'."},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Validate required parameters for organization-specific data
        if not (sector or sub_sector or org_name):
            return Response(
                {"error": "At least one of 'sector', 'sub_sector', or 'org_name' must be provided for organization-specific data."},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Call the service layer function
        extracted_data = financial_variables_service_instance.get_specific_variables_for_specific_org(
            entity_type=entity_type,
            sector=sector,
            sub_sector=sub_sector,
            org_name=org_name,
            target_year=target_year
        )

        # Return the original filter inputs along with processed data
        response_data = {
            "query_inputs": {
                "entity_type": entity_type,
                "sector": sector,
                "sub_sector": sub_sector,
                "org_name": org_name,
                "target_year": target_year,
            },
            "processed_data": extracted_data
        }

        if extracted_data: # Check if the dictionary is not empty
            return Response(response_data, status=status.HTTP_200_OK)
        else:
            response_data["message"] = "No specific financial variables found for the given criteria."
            return Response(response_data, status=status.HTTP_200_OK)


class SectorAverageFinancialVariablesView(APIView):
    """
    API endpoint to calculate the average of specific financial variables for a given sector.
    """
    def get(self, request, *args, **kwargs):
        # Extract query parameters
        entity_type = request.query_params.get('entity_type')
        sector = request.query_params.get('sector')
        target_year = request.query_params.get('target_year') # Can be a year (e.g., "2023") or "all"

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
        aggregated_data = financial_variables_service_instance.get_specific_variables_by_sector(
            entity_type=entity_type,
            sector=sector,
            target_year=target_year
        )

        # Return the original filter inputs along with processed data
        response_data = {
            "query_inputs": {
                "entity_type": entity_type,
                "sector": sector,
                "target_year": target_year,
            },
            "processed_data": aggregated_data
        }

        if aggregated_data: # Check if the dictionary is not empty
            return Response(response_data, status=status.HTTP_200_OK)
        else:
            response_data["message"] = "No aggregated financial variables found for the given sector and criteria."
            return Response(response_data, status=status.HTTP_200_OK)
