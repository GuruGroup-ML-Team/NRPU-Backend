# # project_root/credit_risk/views/organization_data_views.py

# from rest_framework.views import APIView
# from rest_framework.response import Response
# from rest_framework import status
# from credit_risk.services.OrganizationDataService import organization_data_service_instance
# import pandas as pd # Import pandas to use its NaN handling capabilities

# class FetchSpecificOrgDataView(APIView):
#     """
#     API endpoint to fetch all variables data for a particular organization
#     based on entity type, sector, sub-sector, or organization name.
#     """
#     def get(self, request, *args, **kwargs):
#         # Extract query parameters
#         entity_type = request.query_params.get('entity_type')
#         sector = request.query_params.get('sector')
#         sub_sector = request.query_params.get('sub_sector')
#         org_name = request.query_params.get('org_name')

#         # Validate entity_type
#         if not entity_type or entity_type.lower() not in ['company', 'bank']:
#             return Response(
#                 {"error": "Invalid or missing 'entity_type'. Must be 'company' or 'bank'."},
#                 status=status.HTTP_400_BAD_REQUEST
#             )

#         # Call the service layer function
#         result_df = organization_data_service_instance.fetch_data_for_specific_org(
#             entity_type=entity_type,
#             sector=sector,
#             sub_sector=sub_sector,
#             org_name=org_name
#         )

#         # --- FIX FOR NaN VALUES ---
#         # Replace NaN values with None, which is JSON compliant (becomes 'null' in JSON)
#         # This handles NaN across all data types in the DataFrame.
#         result_df = result_df.where(pd.notna(result_df), None)
#         # --- END FIX ---

#         # Convert DataFrame to a list of dictionaries for JSON response
#         processed_data = result_df.to_dict(orient='records')

#         # Return the original filter inputs along with processed data
#         response_data = {
#             "query_inputs": {
#                 "entity_type": entity_type,
#                 "sector": sector,
#                 "sub_sector": sub_sector,
#                 "org_name": org_name,
#             },
#             "processed_data": processed_data
#         }

#         # Check if data was found
#         if not result_df.empty:
#             return Response(response_data, status=status.HTTP_200_OK)
#         else:
#             # If no data found, still return 200 OK but with an empty processed_data list
#             # and a message, as per the requirement "Return the original filter inputs"
#             response_data["message"] = "No data found matching the specified criteria."
#             return Response(response_data, status=status.HTTP_200_OK)


# class FetchSectorDataView(APIView):
#     """
#     API endpoint to fetch complete data for all organizations in a given sector.
#     """
#     def get(self, request, *args, **kwargs):
#         # Extract query parameters
#         entity_type = request.query_params.get('entity_type')
#         sector = request.query_params.get('sector')

#         # Validate entity_type
#         if not entity_type or entity_type.lower() not in ['company', 'bank']:
#             return Response(
#                 {"error": "Invalid or missing 'entity_type'. Must be 'company' or 'bank'."},
#                 status=status.HTTP_400_BAD_REQUEST
#             )

#         # Validate sector
#         if not sector:
#             return Response(
#                 {"error": "Missing 'sector' parameter. Please provide a sector to fetch data."},
#                 status=status.HTTP_400_BAD_REQUEST
#             )

#         # Call the service layer function
#         result_df = organization_data_service_instance.fetch_data_by_sector(
#             entity_type=entity_type,
#             sector=sector
#         )

#         # --- FIX FOR NaN VALUES ---
#         # Replace NaN values with None, which is JSON compliant (becomes 'null' in JSON)
#         result_df = result_df.where(pd.notna(result_df), None)
#         # --- END FIX ---

#         # Convert DataFrame to a list of dictionaries for JSON response
#         processed_data = result_df.to_dict(orient='records')

#         # Return the original filter inputs along with processed data
#         response_data = {
#             "query_inputs": {
#                 "entity_type": entity_type,
#                 "sector": sector,
#             },
#             "processed_data": processed_data
#         }

#         if not result_df.empty:
#             return Response(response_data, status=status.HTTP_200_OK)
#         else:
#             response_data["message"] = f"No data found for the sector: '{sector}'."
#             return Response(response_data, status=status.HTTP_200_OK)

# project_root/credit_risk/views/organization_data_view.py
# project_root/credit_risk/views/organization_data_view.py










# project_root/credit_risk/views/organization_data_view.py

# from rest_framework.views import APIView
# from rest_framework.response import Response
# from rest_framework import status
# from credit_risk.services.OrganizationDataService import organization_data_service_instance
# import pandas as pd # Import pandas for data manipulation
# import numpy as np # Import numpy for np.nan

# class FetchSpecificOrgDataView(APIView):
#     """
#     API endpoint to fetch all variables data for a particular organization
#     based on entity type, sector, sub-sector, or organization name.
#     """
#     def get(self, request, *args, **kwargs):
#         # Extract query parameters
#         entity_type = request.query_params.get('entity_type')
#         sector = request.query_params.get('sector')
#         sub_sector = request.query_params.get('sub_sector')
#         org_name = request.query_params.get('org_name')

#         # Validate entity_type
#         if not entity_type or entity_type.lower() not in ['company', 'bank']:
#             return Response(
#                 {"error": "Invalid or missing 'entity_type'. Must be 'company' or 'bank'."},
#                 status=status.HTTP_400_BAD_REQUEST
#             )

#         # Call the service layer function
#         result_df = organization_data_service_instance.fetch_data_for_specific_org(
#             entity_type=entity_type,
#             sector=sector,
#             sub_sector=sub_sector,
#             org_name=org_name
#         )

#         # Handle cases where no data is found by the service
#         if result_df is None or result_df.empty:
#             response_data = {
#                 "query_inputs": {
#                     "entity_type": entity_type,
#                     "sector": sector,
#                     "sub_sector": sub_sector,
#                     "org_name": org_name,
#                 },
#                 "processed_data": [] # Return empty list if no data
#             }
#             response_data["message"] = "No data found matching the specified criteria."
#             return Response(response_data, status=status.HTTP_200_OK)

#         # --- REFINED ROBUST FIX FOR NON-JSON COMPLIANT VALUES ---
#         # Create a copy to ensure operations don't modify the original DataFrame
#         # directly, which can sometimes lead to SettingWithCopyWarning.
#         cleaned_df = result_df.copy()

#         # Identify columns that are expected to contain numerical year data.
#         # These are columns whose names are integers or string representations of integers.
#         year_columns = [col for col in cleaned_df.columns if isinstance(col, int) or (isinstance(col, str) and str(col).isdigit())]

#         for col in cleaned_df.columns:
#             if col in year_columns:
#                 # For year columns, attempt to convert values to numeric.
#                 # 'errors='coerce'' will turn any non-numeric values into NaN (numpy.nan).
#                 cleaned_df[col] = pd.to_numeric(cleaned_df[col], errors='coerce')
#             # For non-year columns, we don't apply pd.to_numeric.
#             # Their original dtypes (likely 'object' for strings) will be preserved.
#             # Any existing NaN in these columns will be handled by the final replace.
        
#         # FINAL AND MOST RELIABLE PASS: Explicitly replace all remaining NaN (numpy.nan) with None.
#         # This is applied to the entire DataFrame after all numeric coercions.
#         # This handles NaNs introduced by pd.to_numeric and any existing NaNs in string columns.
#         cleaned_df = cleaned_df.replace({np.nan: None})

#         # Assign the fully cleaned DataFrame back
#         result_df = cleaned_df
#         # --- END REFINED ROBUST FIX ---

#         # --- DEBUG PRINTS ---
#         print("\n--- DEBUG: DataFrame Info before JSON conversion (FetchSpecificOrgDataView) ---")
#         result_df.info(verbose=True, show_counts=True) # Shows column dtypes and non-null counts
#         print("\n--- DEBUG: DataFrame Content before JSON conversion (FetchSpecificOrgDataView) ---")
#         print(result_df.to_string()) # Print the entire DataFrame content
#         print("----------------------------------------------------------------------------------\n")
#         # --- END DEBUG PRINTS ---

#         # Convert DataFrame to a list of dictionaries for JSON response
#         processed_data = result_df.to_dict(orient='records')

#         # Return the original filter inputs along with processed data
#         response_data = {
#             "query_inputs": {
#                 "entity_type": entity_type,
#                 "sector": sector,
#                 "sub_sector": sub_sector,
#                 "org_name": org_name,
#             },
#             "processed_data": processed_data
#         }
#         # If data was found, return 200 OK with the processed data
#         return Response(response_data, status=status.HTTP_200_OK)


# class FetchSectorDataView(APIView):
#     """
#     API endpoint to fetch complete data for all organizations in a given sector.
#     """
#     def get(self, request, *args, **kwargs):
#         # Extract query parameters
#         entity_type = request.query_params.get('entity_type')
#         sector = request.query_params.get('sector')

#         # Validate entity_type
#         if not entity_type or entity_type.lower() not in ['company', 'bank']:
#             return Response(
#                 {"error": "Invalid or missing 'entity_type'. Must be 'company' or 'bank'."},
#                 status=status.HTTP_400_BAD_REQUEST
#             )

#         # Validate sector
#         if not sector:
#             return Response(
#                 {"error": "Missing 'sector' parameter. Please provide a sector to fetch data."},
#                 status=status.HTTP_400_BAD_REQUEST
#             )

#         # Call the service layer function
#         result_df = organization_data_service_instance.fetch_data_by_sector(
#             entity_type=entity_type,
#             sector=sector
#         )

#         # Handle cases where no data is found by the service
#         if result_df is None or result_df.empty:
#             response_data = {
#                 "query_inputs": {
#                     "entity_type": entity_type,
#                     "sector": sector,
#                 },
#                 "processed_data": []
#             }
#             response_data["message"] = f"No data found for the sector: '{sector}'."
#             return Response(response_data, status=status.HTTP_200_OK)

#         # --- REFINED ROBUST FIX FOR NON-JSON COMPLIANT VALUES ---
#         cleaned_df = result_df.copy()

#         year_columns = [col for col in cleaned_df.columns if isinstance(col, int) or (isinstance(col, str) and str(col).isdigit())]

#         for col in cleaned_df.columns:
#             if col in year_columns:
#                 cleaned_df[col] = pd.to_numeric(cleaned_df[col], errors='coerce')
#             # No 'else' branch for non-year columns here.
#             # Their original dtypes (likely 'object' for strings) will be preserved.
#             # Any existing NaN in these columns will be handled by the final replace.
        
#         cleaned_df = cleaned_df.replace({np.nan: None})

#         result_df = cleaned_df
#         # --- END REFINED ROBUST FIX ---

#         # --- DEBUG PRINTS ---
#         print("\n--- DEBUG: DataFrame Info before JSON conversion (FetchSectorDataView) ---")
#         result_df.info(verbose=True, show_counts=True) # Shows column dtypes and non-null counts
#         print("\n--- DEBUG: DataFrame Content before JSON conversion (FetchSectorDataView) ---")
#         print(result_df.to_string()) # Print the entire DataFrame content
#         print("----------------------------------------------------------------------------------\n")
#         # --- END DEBUG PRINTS ---

#         # Convert DataFrame to a list of dictionaries for JSON response
#         processed_data = result_df.to_dict(orient='records')

#         # Return the original filter inputs along with processed data
#         response_data = {
#             "query_inputs": {
#                 "entity_type": entity_type,
#                 "sector": sector,
#             },
#             "processed_data": processed_data
#         }
#         # If data was found, return 200 OK with the processed data
#         return Response(response_data, status=status.HTTP_200_OK)



from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from services.OrganizationDataService import organization_data_service_instance
import pandas as pd
import numpy as np

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
        cleaned_df = result_df.copy()

        # Identify columns that are numeric or can be coerced to numeric (including year columns)
        # Using a set to avoid duplicates and allow efficient lookup
        numeric_like_columns = set()
        for col in cleaned_df.columns:
            # Check if column name looks like a year (integer or string of digits)
            if isinstance(col, int) or (isinstance(col, str) and str(col).isdigit()):
                numeric_like_columns.add(col)
            # Also check if the column itself is numeric (e.g., float64, int64)
            elif pd.api.types.is_numeric_dtype(cleaned_df[col]):
                numeric_like_columns.add(col)

        for col in numeric_like_columns:
            print(f"\n--- DEBUG: Processing numeric-like column: '{col}' for {entity_type} data ---")
            print(f"--- DEBUG: Dtype BEFORE pd.to_numeric for '{col}': {cleaned_df[col].dtype}")
            print(f"--- DEBUG: Sample values BEFORE pd.to_numeric for '{col}':\n{cleaned_df[col].value_counts(dropna=False).head(10).to_string()}")

            # Coerce all non-numeric and problematic values to np.nan
            temp_series = pd.to_numeric(cleaned_df[col], errors='coerce')
            print(f"--- DEBUG: Dtype AFTER pd.to_numeric (coerce) for '{col}': {temp_series.dtype}")
            print(f"--- DEBUG: Sample values AFTER pd.to_numeric (coerced) for '{col}':\n{temp_series.value_counts(dropna=False).head(10).to_string()}")
            
            # Replace np.nan, np.inf, -np.inf, and pd.NA with None
            # This will force the column to 'object' dtype if it contains None
            cleaned_df[col] = temp_series.replace([np.nan, np.inf, -np.inf, pd.NA], None)
            
            # It's important to explicitly convert to object if it's still numeric but should contain None
            # This is a belt-and-suspenders approach to ensure type compatibility for JSON
            if pd.api.types.is_numeric_dtype(cleaned_df[col]) and cleaned_df[col].isnull().any():
                cleaned_df[col] = cleaned_df[col].astype(object)

            print(f"--- DEBUG: Dtype AFTER robust cleaning for '{col}': {cleaned_df[col].dtype}")
            print(f"--- DEBUG: Sample values AFTER robust cleaning for '{col}':\n{cleaned_df[col].value_counts(dropna=False).head(10).to_string()}")
        
        # For any remaining non-numeric columns that might have problematic float values
        # (e.g., if they were object before and contained float('nan'))
        for col in cleaned_df.columns:
            if cleaned_df[col].dtype == 'object':
                # Check for float('nan'), float('inf'), float('-inf') within object columns
                cleaned_df[col] = cleaned_df[col].apply(lambda x: None if (isinstance(x, float) and (np.isnan(x) or np.isinf(x))) else x)

        # Assign the fully cleaned DataFrame back
        result_df = cleaned_df
        # --- END REFINED ROBUST FIX ---

        # --- DEBUG PRINTS ---
        print("\n--- FINAL DEBUG: DataFrame Info before JSON conversion (FetchSpecificOrgDataView) ---")
        result_df.info(verbose=True, show_counts=True) # Shows column dtypes and non-null counts
        print("\n--- FINAL DEBUG: DataFrame Content before JSON conversion (FetchSpecificOrgDataView) ---")
        print(result_df.to_string()) # Print the entire DataFrame content
        print("----------------------------------------------------------------------------------\n")
        # --- END DEBUG PRINTS ---

        # Convert DataFrame to a list of dictionaries for JSON response
        # With np.nan already replaced by None, this conversion will be JSON compliant.
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

        # Identify columns that are numeric or can be coerced to numeric (including year columns)
        numeric_like_columns = set()
        for col in cleaned_df.columns:
            # Check if column name looks like a year (integer or string of digits)
            if isinstance(col, int) or (isinstance(col, str) and str(col).isdigit()):
                numeric_like_columns.add(col)
            # Also check if the column itself is numeric (e.g., float64, int64)
            elif pd.api.types.is_numeric_dtype(cleaned_df[col]):
                numeric_like_columns.add(col)

        for col in numeric_like_columns:
            print(f"\n--- DEBUG: Processing numeric-like column: '{col}' for {entity_type} data ---")
            print(f"--- DEBUG: Dtype BEFORE pd.to_numeric for '{col}': {cleaned_df[col].dtype}")
            print(f"--- DEBUG: Sample values BEFORE pd.to_numeric for '{col}':\n{cleaned_df[col].value_counts(dropna=False).head(10).to_string()}")

            # Coerce all non-numeric and problematic values to np.nan
            temp_series = pd.to_numeric(cleaned_df[col], errors='coerce')
            print(f"--- DEBUG: Dtype AFTER pd.to_numeric (coerce) for '{col}': {temp_series.dtype}")
            print(f"--- DEBUG: Sample values AFTER pd.to_numeric (coerced) for '{col}':\n{temp_series.value_counts(dropna=False).head(10).to_string()}")
            
            # Replace np.nan, np.inf, -np.inf, and pd.NA with None
            # This will force the column to 'object' dtype if it contains None
            cleaned_df[col] = temp_series.replace([np.nan, np.inf, -np.inf, pd.NA], None)
            
            # It's important to explicitly convert to object if it's still numeric but should contain None
            # This is a belt-and-suspenders approach to ensure type compatibility for JSON
            if pd.api.types.is_numeric_dtype(cleaned_df[col]) and cleaned_df[col].isnull().any():
                cleaned_df[col] = cleaned_df[col].astype(object)

            print(f"--- DEBUG: Dtype AFTER robust cleaning for '{col}': {cleaned_df[col].dtype}")
            print(f"--- DEBUG: Sample values AFTER robust cleaning for '{col}':\n{cleaned_df[col].value_counts(dropna=False).head(10).to_string()}")
        
        # For any remaining non-numeric columns that might have problematic float values
        for col in cleaned_df.columns:
            if cleaned_df[col].dtype == 'object':
                cleaned_df[col] = cleaned_df[col].apply(lambda x: None if (isinstance(x, float) and (np.isnan(x) or np.isinf(x))) else x)

        result_df = cleaned_df
        # --- END REFINED ROBUST FIX ---

        # --- DEBUG PRINTS ---
        print("\n--- FINAL DEBUG: DataFrame Info before JSON conversion (FetchSectorDataView) ---")
        result_df.info(verbose=True, show_counts=True) # Shows column dtypes and non-null counts
        print("\n--- FINAL DEBUG: DataFrame Content before JSON conversion (FetchSectorDataView) ---")
        print(result_df.to_string()) # Print the entire DataFrame content
        print("----------------------------------------------------------------------------------\n")
        # --- END DEBUG PRINTS ---

        # Convert DataFrame to a list of dictionaries for JSON response
        # With np.nan already replaced by None, this conversion will be JSON compliant.
        processed_data = result_df.to_dict(orient='records')

        # Return the original filter inputs along with processed data
        response_data = {
            "query_inputs": {
                "entity_type": entity_type,
                "sector": sector,
            },
            "processed_data": processed_data
        }
        return Response(response_data, status=status.HTTP_200_OK)







# from rest_framework.views import APIView
# from rest_framework.response import Response
# from rest_framework import status
# from credit_risk.services.OrganizationDataService import organization_data_service_instance
# import pandas as pd # Import pandas for data manipulation
# import numpy as np # Import numpy for np.nan

# class FetchSpecificOrgDataView(APIView):
#     """
#     API endpoint to fetch all variables data for a particular organization
#     based on entity type, sector, sub-sector, or organization name.
#     """
#     def get(self, request, *args, **kwargs):
#         # Extract query parameters
#         entity_type = request.query_params.get('entity_type')
#         sector = request.query_params.get('sector')
#         sub_sector = request.query_params.get('sub_sector')
#         org_name = request.query_params.get('org_name')

#         # Validate entity_type
#         if not entity_type or entity_type.lower() not in ['company', 'bank']:
#             return Response(
#                 {"error": "Invalid or missing 'entity_type'. Must be 'company' or 'bank'."},
#                 status=status.HTTP_400_BAD_REQUEST
#             )

#         # Call the service layer function
#         result_df = organization_data_service_instance.fetch_data_for_specific_org(
#             entity_type=entity_type,
#             sector=sector,
#             sub_sector=sub_sector,
#             org_name=org_name
#         )

#         # Handle cases where no data is found by the service
#         if result_df is None or result_df.empty:
#             response_data = {
#                 "query_inputs": {
#                     "entity_type": entity_type,
#                     "sector": sector,
#                     "sub_sector": sub_sector,
#                     "org_name": org_name,
#                 },
#                 "processed_data": [] # Return empty list if no data
#             }
#             response_data["message"] = "No data found matching the specified criteria."
#             return Response(response_data, status=status.HTTP_200_OK)

#         # --- REFINED ROBUST FIX FOR NON-JSON COMPLIANT VALUES (INCLUDING EXPLICIT FLOAT CASTING) ---
#         cleaned_df = result_df.copy()

#         # Identify columns that *might* contain year data (integers or strings of digits)
#         year_columns = [col for col in cleaned_df.columns if isinstance(col, int) or (isinstance(col, str) and str(col).isdigit())]

#         for col in cleaned_df.columns:
#             if col in year_columns:
#                 print(f"\n--- DEBUG: Processing year column: '{col}' for {entity_type} data ---")
#                 print(f"--- DEBUG: Dtype BEFORE pd.to_numeric for '{col}': {cleaned_df[col].dtype}")
#                 # Print sample of the raw data before conversion
#                 print(f"--- DEBUG: Sample values BEFORE pd.to_numeric for '{col}':\n{cleaned_df[col].value_counts(dropna=False).head(10).to_string()}")

#                 temp_series = pd.to_numeric(cleaned_df[col], errors='coerce')
#                 print(f"--- DEBUG: Dtype AFTER pd.to_numeric (coerce) for '{col}': {temp_series.dtype}")
#                 # Print sample of data after coercion
#                 print(f"--- DEBUG: Sample values AFTER pd.to_numeric (coerced) for '{col}':\n{temp_series.value_counts(dropna=False).head(10).to_string()}")
                
#                 try:
#                     # Explicitly cast the series to float64 to ensure correct dtype
#                     cleaned_df[col] = temp_series.astype(float)
#                     print(f"--- DEBUG: Dtype AFTER .astype(float) for '{col}': {cleaned_df[col].dtype}")
#                     # Print sample of data after explicit cast
#                     print(f"--- DEBUG: Sample values AFTER .astype(float) for '{col}':\n{cleaned_df[col].value_counts(dropna=False).head(10).to_string()}")
#                 except Exception as e:
#                     print(f"--- ERROR: Failed to cast column '{col}' to float: {e} ---")
#                     print(f"--- DEBUG: Column '{col}' will remain {cleaned_df[col].dtype} ---")
        
#         # Explicitly replace np.nan with None to ensure JSON compliance
#         # This is re-added because the previous attempt to rely solely on .to_dict() was not sufficient.
#         cleaned_df = cleaned_df.replace({np.nan: None})

#         # Assign the fully cleaned DataFrame back
#         result_df = cleaned_df
#         # --- END REFINED ROBUST FIX ---

#         # --- DEBUG PRINTS ---
#         print("\n--- FINAL DEBUG: DataFrame Info before JSON conversion (FetchSpecificOrgDataView) ---")
#         result_df.info(verbose=True, show_counts=True) # Shows column dtypes and non-null counts
#         print("\n--- FINAL DEBUG: DataFrame Content before JSON conversion (FetchSpecificOrgDataView) ---")
#         print(result_df.to_string()) # Print the entire DataFrame content
#         print("----------------------------------------------------------------------------------\n")
#         # --- END DEBUG PRINTS ---

#         # Convert DataFrame to a list of dictionaries for JSON response
#         # With np.nan already replaced by None, this conversion will be JSON compliant.
#         processed_data = result_df.to_dict(orient='records')

#         # Return the original filter inputs along with processed data
#         response_data = {
#             "query_inputs": {
#                 "entity_type": entity_type,
#                 "sector": sector,
#                 "sub_sector": sub_sector,
#                 "org_name": org_name,
#             },
#             "processed_data": processed_data
#         }
#         return Response(response_data, status=status.HTTP_200_OK)


# class FetchSectorDataView(APIView):
#     """
#     API endpoint to fetch complete data for all organizations in a given sector.
#     """
#     def get(self, request, *args, **kwargs):
#         # Extract query parameters
#         entity_type = request.query_params.get('entity_type')
#         sector = request.query_params.get('sector')

#         # Validate entity_type
#         if not entity_type or entity_type.lower() not in ['company', 'bank']:
#             return Response(
#                 {"error": "Invalid or missing 'entity_type'. Must be 'company' or 'bank'."},
#                 status=status.HTTP_400_BAD_REQUEST
#             )

#         # Validate sector
#         if not sector:
#             return Response(
#                 {"error": "Missing 'sector' parameter. Please provide a sector to fetch data."},
#                 status=status.HTTP_400_BAD_REQUEST
#             )

#         # Call the service layer function
#         result_df = organization_data_service_instance.fetch_data_by_sector(
#             entity_type=entity_type,
#             sector=sector
#         )

#         # Handle cases where no data is found by the service
#         if result_df is None or result_df.empty:
#             response_data = {
#                 "query_inputs": {
#                     "entity_type": entity_type,
#                     "sector": sector,
#                 },
#                 "processed_data": []
#             }
#             response_data["message"] = f"No data found for the sector: '{sector}'."
#             return Response(response_data, status=status.HTTP_200_OK)

#         # --- REFINED ROBUST FIX FOR NON-JSON COMPLIANT VALUES (INCLUDING EXPLICIT FLOAT CASTING) ---
#         cleaned_df = result_df.copy()

#         # Identify columns that *might* contain year data (integers or strings of digits)
#         year_columns = [col for col in cleaned_df.columns if isinstance(col, int) or (isinstance(col, str) and str(col).isdigit())]

#         for col in cleaned_df.columns:
#             if col in year_columns:
#                 print(f"\n--- DEBUG: Processing year column: '{col}' for {entity_type} data ---")
#                 print(f"--- DEBUG: Dtype BEFORE pd.to_numeric for '{col}': {cleaned_df[col].dtype}")
#                 # Print sample of the raw data before conversion
#                 print(f"--- DEBUG: Sample values BEFORE pd.to_numeric for '{col}':\n{cleaned_df[col].value_counts(dropna=False).head(10).to_string()}")

#                 temp_series = pd.to_numeric(cleaned_df[col], errors='coerce')
#                 print(f"--- DEBUG: Dtype AFTER pd.to_numeric (coerce) for '{col}': {temp_series.dtype}")
#                 # Print sample of data after coercion
#                 print(f"--- DEBUG: Sample values AFTER pd.to_numeric (coerced) for '{col}':\n{temp_series.value_counts(dropna=False).head(10).to_string()}")
                
#                 try:
#                     cleaned_df[col] = temp_series.astype(float)
#                     print(f"--- DEBUG: Dtype AFTER .astype(float) for '{col}': {cleaned_df[col].dtype}")
#                     # Print sample of data after explicit cast
#                     print(f"--- DEBUG: Sample values AFTER .astype(float) for '{col}':\n{cleaned_df[col].value_counts(dropna=False).head(10).to_string()}")
#                 except Exception as e:
#                     print(f"--- ERROR: Failed to cast column '{col}' to float: {e} ---")
#                     print(f"--- DEBUG: Column '{col}' will remain {cleaned_df[col].dtype} ---")
        
#         # Explicitly replace np.nan with None to ensure JSON compliance
#         # This is re-added because the previous attempt to rely solely on .to_dict() was not sufficient.
#         cleaned_df = cleaned_df.replace({np.nan: None})

#         result_df = cleaned_df
#         # --- END REFINED ROBUST FIX ---

#         # --- DEBUG PRINTS ---
#         print("\n--- FINAL DEBUG: DataFrame Info before JSON conversion (FetchSectorDataView) ---")
#         result_df.info(verbose=True, show_counts=True) # Shows column dtypes and non-null counts
#         print("\n--- FINAL DEBUG: DataFrame Content before JSON conversion (FetchSectorDataView) ---")
#         print(result_df.to_string()) # Print the entire DataFrame content
#         print("----------------------------------------------------------------------------------\n")
#         # --- END DEBUG PRINTS ---

#         # Convert DataFrame to a list of dictionaries for JSON response
#         # With np.nan already replaced by None, this conversion will be JSON compliant.
#         processed_data = result_df.to_dict(orient='records')

#         # Return the original filter inputs along with processed data
#         response_data = {
#             "query_inputs": {
#                 "entity_type": entity_type,
#                 "sector": sector,
#             },
#             "processed_data": processed_data
#         }
#         return Response(response_data, status=status.HTTP_200_OK)