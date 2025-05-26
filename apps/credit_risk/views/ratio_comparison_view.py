# # project_root/credit_risk/views/ratio_comparison_views.py

# from rest_framework.views import APIView
# from rest_framework.response import Response
# from rest_framework import status
# from credit_risk.services.RatioComparisonService import ratio_comparison_service_instance

# class RatioComparisonView(APIView):
#     """
#     API endpoint to compare an organization's financial ratios against
#     its industry average and provide scores.
#     """
#     def get(self, request, *args, **kwargs):
#         # Extract query parameters
#         entity_type = request.query_params.get('entity_type')
#         sector = request.query_params.get('sector')
#         sub_sector = request.query_params.get('sub_sector')
#         org_name = request.query_params.get('org_name')
#         year = request.query_params.get('year')

#         # Validate entity_type
#         if not entity_type or entity_type.lower() not in ['company', 'bank']:
#             return Response(
#                 {"error": "Invalid or missing 'entity_type'. Must be 'company' or 'bank'."},
#                 status=status.HTTP_400_BAD_REQUEST
#             )
        
#         # Validate required parameters for comparison
#         if not (sector and org_name and year):
#             return Response(
#                 {"error": "Missing required parameters: 'sector', 'org_name', and 'year' are mandatory for ratio comparison."},
#                 status=status.HTTP_400_BAD_REQUEST
#             )
        
#         try:
#             year_int = int(year)
#         except ValueError:
#             return Response(
#                 {"error": "Invalid 'year' parameter. Must be a valid integer."},
#                 status=status.HTTP_400_BAD_REQUEST
#             )

#         # Call the service layer function
#         comparison_results = ratio_comparison_service_instance.compare_financial_ratios(
#             entity_type=entity_type,
#             sector=sector,
#             sub_sector=sub_sector, # sub_sector is optional for comparison, but passed through
#             org_name=org_name,
#             year=year_int
#         )

#         # Return the original filter inputs along with processed data
#         response_data = {
#             "query_inputs": {
#                 "entity_type": entity_type,
#                 "sector": sector,
#                 "sub_sector": sub_sector,
#                 "org_name": org_name,
#                 "year": year,
#             },
#             "processed_data": comparison_results
#         }

#         if comparison_results: # Check if the dictionary is not empty
#             return Response(response_data, status=status.HTTP_200_OK)
#         else:
#             response_data["message"] = "No ratio comparison results found for the given criteria. Ensure data exists for both the organization and its industry for the specified year."
#             return Response(response_data, status=status.HTTP_200_OK)


# project_root/credit_risk/views/ratio_comparison_views.py

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from apps.credit_risk.services.RatioComparisonService import ratio_comparison_service_instance

class RatioComparisonView(APIView):
    """
    API endpoint to compare an organization's financial ratios against
    its industry average and provide scores.
    """
    def get(self, request, *args, **kwargs):
        # Extract query parameters
        entity_type = request.query_params.get('entity_type')
        sector = request.query_params.get('sector')
        sub_sector = request.query_params.get('sub_sector')
        org_name = request.query_params.get('org_name')
        year = request.query_params.get('year')

        # Validate entity_type
        if not entity_type or entity_type.lower() not in ['company', 'bank']:
            return Response(
                {"error": "Invalid or missing 'entity_type'. Must be 'company' or 'bank'."},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Validate required parameters for comparison
        # Note: year is handled separately below to allow 'all'
        if not (sector and org_name): # Removed 'year' from this check
            return Response(
                {"error": "Missing required parameters: 'sector' and 'org_name' are mandatory for ratio comparison."},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # --- START OF FIX ---
        # Validate 'year' parameter to allow either a valid integer or the string 'all'
        year_to_pass = None
        if year is None:
            # If year is not provided, treat it as 'all' by default, as per FinancialRatiosCalculator's behavior
            year_to_pass = 'all' 
        elif year.lower() == 'all':
            year_to_pass = 'all'
        else:
            try:
                # Attempt to convert to int if it's not 'all'
                year_to_pass = int(year) 
            except ValueError:
                return Response(
                    {"error": "Invalid 'year' parameter. Must be a valid integer or 'all'."},
                    status=status.HTTP_400_BAD_REQUEST
                )
        # --- END OF FIX ---

        # Call the service layer function
        comparison_results = ratio_comparison_service_instance.compare_financial_ratios(
            entity_type=entity_type,
            sector=sector,
            sub_sector=sub_sector, # sub_sector is optional for comparison, but passed through
            org_name=org_name,
            year=year_to_pass # Pass the validated year_to_pass (int or 'all')
        )

        # Return the original filter inputs along with processed data
        response_data = {
            "query_inputs": {
                "entity_type": entity_type,
                "sector": sector,
                "sub_sector": sub_sector,
                "org_name": org_name,
                "year": year, # Echo the original year string from query params
            },
            "processed_data": comparison_results
        }

        if comparison_results: # Check if the dictionary is not empty
            return Response(response_data, status=status.HTTP_200_OK)
        else:
            response_data["message"] = "No ratio comparison results found for the given criteria. Ensure data exists for both the organization and its industry for the specified year."
            return Response(response_data, status=status.HTTP_200_OK)