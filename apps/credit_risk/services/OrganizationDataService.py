# project_root/credit_risk/services/logic_one_service.py

import pandas as pd
# from credit_risk.services.file_loader_service import file_loader_service_instance
from .file_loader_service import file_loader_service_instance

class OrganizationDataService: # Renamed from LogicOneService
    """
    Service containing logic for fetching variables data for specific organizations
    or sectors, utilizing the FileLoaderService to access data.
    """

    def fetch_data_for_specific_org(self, entity_type: str, sector: str = None, sub_sector: str = None, org_name: str = None) -> pd.DataFrame:
        """
        Fetches all variables of a particular organization based on sector and sub-sector.

        Args:
            entity_type (str): The type of entity to load data for ('company' or 'bank').
            sector (str, optional): The sector to filter by. Defaults to None.
            sub_sector (str, optional): The sub-sector to filter by. Defaults to None.
            org_name (str, optional): The organization name to filter by. Defaults to None.

        Returns:
            pd.DataFrame: A DataFrame containing the filtered data. Returns an empty DataFrame
                          if no data matches the criteria or if the base data cannot be loaded.
        """
        # Load data based on entity_type using the file_loader_service_instance
        df = file_loader_service_instance.load_data(entity_type)

        if df is None or df.empty:
            print(f"ℹ️ Could not load data for entity type: {entity_type}. Returning empty DataFrame.")
            return pd.DataFrame()

        query_conditions = []

        # Build query conditions based on provided parameters
        if sector:
            if 'Sector' in df.columns:
                query_conditions.append(df['Sector'] == sector)
            else:
                print(f"Warning: 'Sector' column not found in {entity_type} data.")
        if sub_sector:
            if 'Sub-Sector' in df.columns:
                query_conditions.append(df['Sub-Sector'] == sub_sector)
            else:
                print(f"Warning: 'Sub-Sector' column not found in {entity_type} data.")
        if org_name:
            if 'Org Name' in df.columns:
                query_conditions.append(df['Org Name'] == org_name)
            else:
                print(f"Warning: 'Org Name' column not found in {entity_type} data.")

        if query_conditions:
            # Combine all conditions using bitwise AND
            combined_condition = query_conditions[0]
            for condition in query_conditions[1:]:
                combined_condition &= condition
            
            filtered_df = df[combined_condition]

            if not filtered_df.empty:
                print("✅ Data filtered successfully based on provided criteria.")
                return filtered_df
            else:
                print("ℹ️ No data found matching the specified criteria.")
                return pd.DataFrame()  # Return an empty DataFrame
        else:
            print("ℹ️ No filtering criteria provided. Returning the entire dataset.")
            return df

    def fetch_data_by_sector(self, entity_type: str, sector: str) -> pd.DataFrame:
        """
        Returns complete data for all organizations in a given sector,
        including all sub-sectors if any.

        Args:
            entity_type (str): The type of entity to load data for ('company' or 'bank').
            sector (str): The sector to filter by.

        Returns:
            pd.DataFrame: A DataFrame containing the filtered data. Returns an empty DataFrame
                          if no data matches the criteria or if the base data cannot be loaded.
        """
        # Load data based on entity_type using the file_loader_service_instance
        df = file_loader_service_instance.load_data(entity_type)

        if df is None or df.empty:
            print(f"ℹ️ Could not load data for entity type: {entity_type}. Returning empty DataFrame.")
            return pd.DataFrame()

        if not sector:
            print("❌ Sector not provided. Please provide a sector to fetch data.")
            return pd.DataFrame()

        if 'Sector' in df.columns:
            filtered_df = df[df['Sector'] == sector]
            if not filtered_df.empty:
                print(f"✅ Data for all organizations in '{sector}' sector retrieved successfully.")
                return filtered_df
            else:
                print(f"ℹ️ No data found for the sector: '{sector}'.")
                return pd.DataFrame()
        else:
            print(f"Warning: 'Sector' column not found in {entity_type} data. Cannot filter by sector.")
            return pd.DataFrame()

# Instantiate the service for use in views
# The instance name remains consistent with the file name for import clarity
organization_data_service_instance = OrganizationDataService()
