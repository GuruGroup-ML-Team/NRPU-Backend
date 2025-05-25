# project_root/credit_risk/views/financial_ratios_views.py

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from apps.credit_risk.services.FinancialRatiosService import financial_ratios_service_instance
# from services.FinancialRatiosService import financial_ratios_service_instance

class CompanyRatiosView(APIView):
    """
    API endpoint to calculate financial ratios for a specific company.
    """
    def get(self, request, *args, **kwargs):
        # Extract query parameters
        entity_type = request.query_params.get('entity_type')
        sector = request.query_params.get('sector')
        sub_sector = request.query_params.get('sub_sector')
        org_name = request.query_params.get('org_name')
        target_year = request.query_params.get('target_year')

        # Validate entity_type
        if not entity_type or entity_type.lower() not in ['company', 'bank']:
            return Response(
                {"error": "Invalid or missing 'entity_type'. Must be 'company' or 'bank'."},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Validate required parameters for organization-specific data
        if not (sector or sub_sector or org_name):
            return Response(
                {"error": "At least one of 'sector', 'sub_sector', or 'org_name' must be provided for organization-specific ratio calculation."},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Call the service layer function
        calculated_ratios = financial_ratios_service_instance.calculate_financial_ratios_for_specific_entity(
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
            "processed_data": calculated_ratios
        }

        if calculated_ratios: # Check if the dictionary is not empty
            return Response(response_data, status=status.HTTP_200_OK)
        else:
            response_data["message"] = "No financial ratios calculated for the given criteria."
            return Response(response_data, status=status.HTTP_200_OK)


class SectorRatiosView(APIView):
    """
    API endpoint to calculate average financial ratios for a specific sector.
    """
    def get(self, request, *args, **kwargs):
        # Extract query parameters
        entity_type = request.query_params.get('entity_type')
        sector = request.query_params.get('sector')
        target_year = request.query_params.get('target_year')

        # Validate entity_type
        if not entity_type or entity_type.lower() not in ['company', 'bank']:
            return Response(
                {"error": "Invalid or missing 'entity_type'. Must be 'company' or 'bank'."},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Validate sector
        if not sector:
            return Response(
                {"error": "Missing 'sector' parameter. Please provide a sector to calculate ratios."},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Call the service layer function
        calculated_ratios = financial_ratios_service_instance.calculate_financial_ratios_for_specific_sector(
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
            "processed_data": calculated_ratios
        }

        if calculated_ratios: # Check if the dictionary is not empty
            return Response(response_data, status=status.HTTP_200_OK)
        else:
            response_data["message"] = "No average financial ratios calculated for the given sector and criteria."
            return Response(response_data, status=status.HTTP_200_OK)
