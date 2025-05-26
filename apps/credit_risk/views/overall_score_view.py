# project_root/credit_risk/views/overall_score_views.py

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from apps.credit_risk.services.OverallScoreService import overall_score_service_instance
import json 

class OverallScoreView(APIView):
    """
    API endpoint to calculate the overall weighted financial score for an organization.
    Supports default or custom weightages.
    """
    def get(self, request, *args, **kwargs):
        # Extract query parameters
        entity_type = request.query_params.get('entity_type')
        sector = request.query_params.get('sector')
        sub_sector = request.query_params.get('sub_sector')
        org_name = request.query_params.get('org_name')
        year = request.query_params.get('year') 
        weight_type = request.query_params.get('weight_type') 
        user_type = request.query_params.get('user_type')     

        custom_weights_str = request.query_params.get('custom_weights')
        custom_weights = None
        if weight_type and weight_type.lower() == 'custom':
            if not custom_weights_str:
                return Response(
                    {"error": "For 'custom' weight_type, 'custom_weights' JSON string is required."},
                    status=status.HTTP_400_BAD_REQUEST
                )
            try:
                custom_weights = json.loads(custom_weights_str)
                if not isinstance(custom_weights, dict):
                    raise ValueError("Custom weights must be a JSON object (dictionary).")
            except json.JSONDecodeError:
                return Response(
                    {"error": "Invalid JSON format for 'custom_weights'."},
                    status=status.HTTP_400_BAD_REQUEST
                )
            except ValueError as e:
                return Response(
                    {"error": f"Invalid 'custom_weights' format: {e}"},
                    status=status.HTTP_400_BAD_REQUEST
                )

        # Validate core parameters
        if not all([entity_type, sector, org_name, year, weight_type]):
            return Response(
                {"error": "Missing required parameters: 'entity_type', 'sector', 'org_name', 'year', 'weight_type'."},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Validate 'year' parameter to allow either a valid integer or the string 'all'
        year_to_pass = None
        if year is None:
            year_to_pass = 'all' 
        elif year.lower() == 'all':
            year_to_pass = 'all'
        else:
            try:
                year_to_pass = int(year) 
            except ValueError:
                return Response(
                    {"error": "Invalid 'year' parameter. Must be a valid integer or 'all'."},
                    status=status.HTTP_400_BAD_REQUEST
                )

        # Validate weight_type and user_type combination
        if weight_type.lower() == 'default' and not user_type:
            return Response(
                {"error": "For 'default' weight_type, 'user_type' ('Lender' or 'Investor') is required."},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        if weight_type.lower() not in ['default', 'custom']:
            return Response(
                {"error": "Invalid 'weight_type'. Must be 'default' or 'custom'."},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Call the service layer function and capture all returned elements
        overall_score, weights_applied, calculation_breakdown, overall_score_interpretation = \
            overall_score_service_instance.calculate_overall_score(
                entity_type=entity_type,
                sector=sector,
                sub_sector=sub_sector,
                org_name=org_name,
                year=year_to_pass,
                weight_type=weight_type,
                user_type=user_type,
                custom_weights=custom_weights
            )

        response_data = {
            "query_inputs": {
                "entity_type": entity_type,
                "sector": sector,
                "sub_sector": sub_sector,
                "org_name": org_name,
                "year": year, 
                "weight_type": weight_type,
                "user_type": user_type,
                "custom_weights": custom_weights_str 
            },
            "processed_data": {
                "overall_score": overall_score,
                "overall_score_interpretation": overall_score_interpretation, # New: Interpretation
                "weights_applied": weights_applied, 
                "calculation_breakdown": calculation_breakdown 
            }
        }

        if overall_score is not None and (not isinstance(overall_score, dict) or bool(overall_score)):
            return Response(response_data, status=status.HTTP_200_OK)
        else:
            response_data["message"] = "Could not calculate overall score for the given criteria. Check inputs, data availability, and if any valid category scores were found for weighting."
            return Response(response_data, status=status.HTTP_200_OK)