# project_root/credit_risk/services/file_loader_service.py

import pandas as pd
from pathlib import Path
from django.conf import settings # Import settings to access BASE_DIR

class FileLoaderService:
    """
    Service responsible for loading data from Excel files into Pandas DataFrames.
    This service ensures that data loading is centralized and reusable across
    different logic services. It now dynamically loads data based on entity type.
    """

    def _get_excel_path(self, entity_type: str) -> Path:
        """
        Determines the absolute path to the Excel file based on the entity type.
        """
        # Construct the absolute path to the 'data' directory
        data_dir = settings.BASE_DIR / 'Data'

        if entity_type.lower() == 'company':
            return data_dir / "company_data.xlsx"
        elif entity_type.lower() == 'bank':
            return data_dir / "bank_data.xlsx"
        else:
            # This case should ideally be handled by input validation upstream
            # but included for robustness.
            raise ValueError(f"Invalid entity type '{entity_type}'. Please specify 'company' or 'bank'.")

    def load_data(self, entity_type: str) -> pd.DataFrame | None:
        """
        Loads data from the specified Excel file into a Pandas DataFrame.

        Args:
            entity_type (str): The type of entity to load data for ('company' or 'bank').

        Returns:
            pd.DataFrame | None: The loaded DataFrame, or None if an error occurred.
        """
        try:
            excel_path = self._get_excel_path(entity_type)
        except ValueError as e:
            print(f"❌ Error: {e}")
            return None

        try:
            if excel_path.exists():
                df = pd.read_excel(excel_path)
                print(f"✅ Successfully loaded {entity_type.capitalize()} data from: {excel_path}")
                return df
            else:
                print(f"❌ Error: Excel file not found at path: {excel_path}")
                # For development, return a dummy DataFrame if the file is not found
                if entity_type.lower() == 'company':
                    print("Using dummy DataFrame for company data.")
                    return pd.DataFrame({'company_id': [1, 2, 3], 'company_name': ['CompA', 'CompB', 'CompC']})
                elif entity_type.lower() == 'bank':
                    print("Using dummy DataFrame for bank data.")
                    return pd.DataFrame({'bank_id': [101, 102, 103], 'bank_name': ['BankX', 'BankY', 'BankZ']})
                return None
        except Exception as e:
            print(f"❌ An error occurred while reading the Excel file: {str(e)}")
            return None

    def get_company_data(self) -> pd.DataFrame | None:
        """
        Convenience method to get the company data.
        """
        return self.load_data('company')

    def get_bank_data(self) -> pd.DataFrame | None:
        """
        Convenience method to get the bank data.
        """
        return self.load_data('bank')

# Instantiate the service. Data will be loaded via its methods when called.
file_loader_service_instance = FileLoaderService()
