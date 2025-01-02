from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import numpy as np
from statsmodels.sandbox.regression.gmm import GMM 
import requests 


class GeneralizedMethodOfMoment(APIView):
    """
    API to predict future Altman Z-scores using Generalized Method of Moments (GMM).
    """

    def fetch_altman_zscore_data(self, sector, sub_sector, org_name):
        """
        Fetch data from the Altman Z-score API for the years 2018-2022.
        """
        altman_api_url = "https://nrpuapi-137b31326fcb.herokuapp.com/api/altman-zscore/"  # Update with the actual API URL
        years = [2018, 2019, 2020, 2021, 2022]
        zscores = []

        for year in years:
            payload = {
                "sector": sector,
                "sub_sector": sub_sector,
                "org_name": org_name,
                "year": str(year),
            }
            response = requests.post(altman_api_url, json=payload)
            if response.status_code == 200:
                data = response.json()
                zscore = data.get("altman_zscore")
                if zscore and isinstance(zscore, (float, int)):
                    zscores.append((year, zscore))
                else:
                    zscores.append((year, None))
            else:
                zscores.append((year, None))

        return zscores

    def fit_gmm(self, data):
        """
        Apply Generalized Method of Moments (GMM) on the Altman Z-score data.
        """
        years = np.array([item[0] for item in data if item[1] is not None])
        zscores = np.array([item[1] for item in data if item[1] is not None])

        if len(years) < 2:
            raise ValueError("Insufficient data for GMM prediction.")

        # Define the instruments as the independent variable (years)
        instruments = np.vstack([np.ones_like(years), years - years.mean()]).T

        class AltmanGMMModel(GMM):
            def momcond(self, params):
                """
                Define moment conditions for GMM.
                """
                alpha, beta = params
                residuals = zscores - (alpha + beta * (years - years.mean()))
                return residuals[:, None] * instruments

        # Initial parameter guesses
        initial_params = [1, 0.1]

        # Fit GMM model
        model = AltmanGMMModel(endog=zscores, exog=instruments, instrument=instruments)
        result = model.fit(start_params=initial_params, optim_method="nm", maxiter=1000)

        return result.params  # Return estimated parameters (alpha, beta)

    def predict_future(self, params, future_years):
        """
        Predict Altman Z-scores for future years based on GMM parameters.
        """
        alpha, beta = params
        return {year: alpha + beta * (year - 2022) for year in future_years}

    def post(self, request):
        """
        POST method to predict future Altman Z-scores using GMM and return actual historical Z-scores.
        """
        try:
            # Get input data
            sector = request.data.get("sector")
            sub_sector = request.data.get("sub_sector")
            org_name = request.data.get("org_name")
            future_years = request.data.get("future_years", [2023, 2024, 2025])

            if not sector or not sub_sector or not org_name:
                return Response(
                    {"error": "Sector, Sub-Sector, and Org Name are required."},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            # Fetch historical data
            historical_data = self.fetch_altman_zscore_data(sector, sub_sector, org_name)

            # Filter valid Z-scores for actual years
            actual_zscores = {year: zscore for year, zscore in historical_data if zscore is not None}

            # Apply GMM to fit data
            params = self.fit_gmm(historical_data)

            # Predict future Z-scores
            predictions = self.predict_future(params, future_years)

            # Combine actual and predicted Z-scores
            return Response(
                {
                    "sector": sector,
                    "sub_sector": sub_sector,
                    "org_name": org_name,
                    "actual_zscores": actual_zscores,  # Historical Z-scores
                    "predicted_zscores": predictions,  # Future Z-scores
                },
                status=status.HTTP_200_OK,
            )

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
