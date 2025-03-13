# bank_api/views.py
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .services import BankDataService
from .serializers import BankComparisonSerializer


class BankListAPIView(APIView):
    """
    API endpoint that returns a list of banks listed in the stock exchange.
    """

    def get(self, request):
        banks = BankDataService.get_listed_banks()
        return Response({"banks": banks})


class BankDetailAPIView(APIView):
    """
    API endpoint that returns detailed information about a specific bank.
    """

    def get(self, request, bank_name):
        data = BankDataService.get_bank_data()

        # Check if bank exists
        if bank_name not in data["Banks"]:
            return Response(
                {"error": f"Bank '{bank_name}' not found"},
                status=status.HTTP_404_NOT_FOUND
            )

        bank_data = data["Banks"][bank_name]
        return Response(bank_data)


class BankComparisonAPIView(APIView):
    """
    API endpoint that compares multiple banks based on selected metrics.
    """

    def post(self, request):
        serializer = BankComparisonSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        banks = serializer.validated_data["banks"]
        metrics = serializer.validated_data["metrics"]
        year = serializer.validated_data["year"]

        data = BankDataService.get_bank_data()
        result = {}

        for bank in banks:
            if bank not in data["Banks"]:
                return Response(
                    {"error": f"Bank '{bank}' not found"},
                    status=status.HTTP_404_NOT_FOUND
                )

            bank_data = data["Banks"][bank]
            result[bank] = {}

            for metric in metrics:
                if metric in bank_data and year in bank_data[metric]:
                    result[bank][metric] = bank_data[metric][year]
                else:
                    result[bank][metric] = None

        return Response(result)


class BankRankingAPIView(APIView):
    """
    API endpoint that returns rankings of banks based on a specific metric.
    """

    def get(self, request):
        metric = request.query_params.get("metric", "Assets")
        year = request.query_params.get("year", "2023")

        data = BankDataService.get_bank_data()
        rankings = []

        for bank_name, bank_data in data["Banks"].items():
            if bank_name != "All Banks" and metric in bank_data and year in bank_data[metric]:
                rankings.append({
                    "bank": bank_name,
                    "value": bank_data[metric][year]
                })

        # Sort by the metric value in descending order
        rankings.sort(key=lambda x: x["value"], reverse=True)

        # Add rank
        for i, item in enumerate(rankings):
            item["rank"] = i + 1

        return Response(rankings)


class BankFinancialAnalysisAPIView(APIView):
    """
    API endpoint that provides financial analysis for a specific bank.
    """

    def get(self, request, bank_name):
        data = BankDataService.get_bank_data()

        # Check if bank exists
        if bank_name not in data["Banks"]:
            return Response(
                {"error": f"Bank '{bank_name}' not found"},
                status=status.HTTP_404_NOT_FOUND
            )

        bank_data = data["Banks"][bank_name]
        all_banks_data = data["Banks"]["All Banks"]

        # Calculate financial ratios and metrics
        analysis = {
            "bank_name": bank_name,
            "year": "2023",
            "metrics": {},
            "ratios": {},
            "growth": {},
            "industry_comparison": {}
        }

        # Add key metrics
        if "Assets" in bank_data and "2023" in bank_data["Assets"]:
            analysis["metrics"]["total_assets"] = bank_data["Assets"]["2023"]

        if "Revenue" in bank_data and "2023" in bank_data["Revenue"]:
            analysis["metrics"]["revenue"] = bank_data["Revenue"]["2023"]

        if "A. Total equity (A1 to A3)" in bank_data and "2023" in bank_data["A. Total equity (A1 to A3)"]:
            analysis["metrics"]["total_equity"] = bank_data["A. Total equity (A1 to A3)"]["2023"]

        # Calculate growth rates
        for metric in ["Assets", "Revenue", "A. Total equity (A1 to A3)"]:
            if metric in bank_data and "2022" in bank_data[metric] and "2023" in bank_data[metric]:
                current_year = bank_data[metric]["2023"]
                previous_year = bank_data[metric]["2022"]
                growth_rate = ((current_year - previous_year) / previous_year) * 100
                analysis["growth"][f"{metric.lower()}_growth"] = round(growth_rate, 2)

        # Calculate industry comparison (market share)
        if "Assets" in bank_data and "2023" in bank_data["Assets"]:
            if "Assets" in all_banks_data and "2023" in all_banks_data["Assets"]:
                market_share = (bank_data["Assets"]["2023"] / all_banks_data["Assets"]["2023"]) * 100
                analysis["industry_comparison"]["asset_market_share"] = round(market_share, 2)

        return Response(analysis)


# New API endpoints for dropdown functionality

class SectorListAPIView(APIView):
    """
    API endpoint that returns a list of all sectors.
    """

    def get(self, request):
        sectors = BankDataService.get_sectors()
        return Response({"sectors": sectors})


class SubSectorListAPIView(APIView):
    """
    API endpoint that returns a list of sub-sectors for a given sector.
    """

    def get(self, request):
        sector = request.query_params.get("sector")
        if not sector:
            return Response(
                {"error": "Sector parameter is required"},
                status=status.HTTP_400_BAD_REQUEST
            )

        sub_sectors = BankDataService.get_sub_sectors(sector)
        return Response({"sub_sectors": sub_sectors})


class BanksBySubSectorAPIView(APIView):
    """
    API endpoint that returns a list of banks for a given sub-sector.
    """

    def get(self, request):
        sub_sector = request.query_params.get("sub_sector")
        if not sub_sector:
            return Response(
                {"error": "Sub-sector parameter is required"},
                status=status.HTTP_400_BAD_REQUEST
            )

        banks = BankDataService.get_banks_by_sub_sector(sub_sector)
        return Response({"banks": banks})


class MetricsListAPIView(APIView):
    """
    API endpoint that returns a list of available metrics.
    """

    def get(self, request):
        metrics = BankDataService.get_metrics()
        return Response({"metrics": metrics})


class YearsListAPIView(APIView):
    """
    API endpoint that returns a list of available years.
    """

    def get(self, request):
        years = BankDataService.get_years()
        return Response({"years": years})


class BankComparativeAnalysisAPIView(APIView):
    """
    API endpoint that provides comparative financial ratio analysis between banks.
    """

    def get(self, request):
        # Get parameters from query parameters instead of request body
        banks_param = request.query_params.get("banks", "")
        banks = banks_param.split(",") if banks_param else []
        year = request.query_params.get("year", "2023")  # Default to 2023 if not specified

        # Validate parameters
        if not banks:
            return Response(
                {"error": "Please provide a list of banks to compare using the 'banks' query parameter"},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Get bank data
        data = BankDataService.get_bank_data()
        all_banks_data = data["Banks"].get("All Banks", {})

        # Check if all banks exist
        for bank in banks:
            if bank not in data["Banks"]:
                return Response(
                    {"error": f"Bank '{bank}' not found"},
                    status=status.HTTP_404_NOT_FOUND
                )

        # Calculate ratios for each bank
        results = {}
        for bank in banks:
            bank_data = data["Banks"][bank]

            # Initialize bank result with basic information
            results[bank] = {
                "basic_info": {
                    "name": bank,
                    "year": year
                },
                "efficiency_ratios": {},
                "liquidity_ratios": {},
                "asset_quality_ratios": {},
                "capital_ratios": {}
            }

            # Get basic metrics if available
            if "C. Total assets (C1 to C4 + C8 to C10)" in bank_data and year in bank_data[
                "C. Total assets (C1 to C4 + C8 to C10)"]:
                results[bank]["basic_info"]["total_assets"] = bank_data["C. Total assets (C1 to C4 + C8 to C10)"][year]

            if "1. Markup/interest earned" in bank_data and year in bank_data["1. Markup/interest earned"]:
                results[bank]["basic_info"]["revenue"] = bank_data["1. Markup/interest earned"][year]

            # Calculate all financial ratios using the service
            calculated_ratios = BankDataService.calculate_financial_ratios(bank_data, year)

            # Copy all the calculated ratios to our results
            results[bank]["efficiency_ratios"] = calculated_ratios["efficiency_ratios"]
            results[bank]["liquidity_ratios"] = calculated_ratios["liquidity_ratios"]
            results[bank]["asset_quality_ratios"] = calculated_ratios["asset_quality_ratios"]
            results[bank]["capital_ratios"] = calculated_ratios["capital_ratios"]

        # Calculate industry averages for comparison if "All Banks" data is available
        if all_banks_data:
            # Calculate all financial ratios for the industry averages
            industry_ratios = BankDataService.calculate_financial_ratios(all_banks_data, year)

            # Add industry basic info
            results["industry_averages"] = {
                "basic_info": {
                    "name": "Industry Average",
                    "year": year
                }
            }

            # Copy industry ratios to the results
            results["industry_averages"]["efficiency_ratios"] = industry_ratios["efficiency_ratios"]
            results["industry_averages"]["liquidity_ratios"] = industry_ratios["liquidity_ratios"]
            results["industry_averages"]["asset_quality_ratios"] = industry_ratios["asset_quality_ratios"]
            results["industry_averages"]["capital_ratios"] = industry_ratios["capital_ratios"]

            # Add some basic industry metrics
            if "C. Total assets (C1 to C4 + C8 to C10)" in all_banks_data and year in all_banks_data[
                "C. Total assets (C1 to C4 + C8 to C10)"]:
                results["industry_averages"]["basic_info"]["total_assets"] = \
                all_banks_data["C. Total assets (C1 to C4 + C8 to C10)"][year]

            if "1. Markup/interest earned" in all_banks_data and year in all_banks_data["1. Markup/interest earned"]:
                results["industry_averages"]["basic_info"]["revenue"] = all_banks_data["1. Markup/interest earned"][
                    year]

        return Response(results)

    # Keep the POST method for backward compatibility
    def post(self, request):
        banks = request.data.get("banks", [])
        year = request.data.get("year", "2023")

        # Validate incoming data
        if not banks or not isinstance(banks, list):
            return Response(
                {"error": "Please provide a list of banks to compare"},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Create a mock request with query parameters
        mock_request = request._request
        mock_request.GET = {
            "banks": ",".join(banks),
            "year": year
        }

        # Call the GET method with the mock request
        return self.get(mock_request)


class BankScoreAPIView(APIView):
    """
    API endpoint that calculates an overall financial score for banks.
    """

    def get(self, request):
        # Get parameters from query parameters instead of request body
        banks_param = request.query_params.get("banks", "")
        banks = banks_param.split(",") if banks_param else []
        year = request.query_params.get("year", "2023")

        # Get weights from query parameters
        efficiency_weight = float(request.query_params.get("efficiency_weight", "0.60"))
        liquidity_weight = float(request.query_params.get("liquidity_weight", "0.25"))
        asset_quality_weight = float(request.query_params.get("asset_quality_weight", "0.15"))
        capital_weight = float(request.query_params.get("capital_weight", "0.10"))

        weights = {
            "efficiency": efficiency_weight,
            "liquidity": liquidity_weight,
            "asset_quality": asset_quality_weight,
            "capital": capital_weight
        }

        # Validate parameters
        if not banks:
            return Response(
                {"error": "Please provide a list of banks to score using the 'banks' query parameter"},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Get bank data
        data = BankDataService.get_bank_data()

        # Calculate scores for each bank
        results = {}
        for bank in banks:
            if bank not in data["Banks"]:
                return Response(
                    {"error": f"Bank '{bank}' not found"},
                    status=status.HTTP_404_NOT_FOUND
                )

            bank_data = data["Banks"][bank]

            # Use the calculate_bank_score method from BankDataService
            bank_score = BankDataService.calculate_bank_score(bank_data, weights, year)
            results[bank] = bank_score

        return Response(results)

    def post(self, request):
        """
        Handle POST requests for bank scoring
        """
        banks = request.data.get("banks", [])
        year = request.data.get("year", "2023")
        weights = request.data.get("weights", {
            "efficiency": 0.60,
            "liquidity": 0.25,
            "asset_quality": 0.15,
            "capital": 0.10
        })

        # Validate incoming data
        if not banks or not isinstance(banks, list):
            return Response(
                {"error": "Please provide a list of banks to score"},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Get bank data
        data = BankDataService.get_bank_data()

        # Calculate scores for each bank
        results = {}
        for bank in banks:
            if bank not in data["Banks"]:
                return Response(
                    {"error": f"Bank '{bank}' not found"},
                    status=status.HTTP_404_NOT_FOUND
                )

            bank_data = data["Banks"][bank]

            # Calculate bank score
            bank_score = BankDataService.calculate_bank_score(bank_data, weights, year)
            results[bank] = bank_score

        return Response(results)


class BankTrendAnalysisAPIView(APIView):
    """
    API endpoint that provides trend analysis for bank financial ratios over multiple years.
    """

    def get(self, request):
        # Get parameters from query parameters
        bank = request.query_params.get("bank", "")
        years_param = request.query_params.get("years", "2019,2020,2021,2022,2023")
        years = years_param.split(",") if years_param else BankDataService.get_years()

        # Validate parameters
        if not bank:
            return Response(
                {"error": "Please provide a bank to analyze using the 'bank' query parameter"},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Get bank data
        data = BankDataService.get_bank_data()

        # Check if bank exists
        if bank not in data["Banks"]:
            return Response(
                {"error": f"Bank '{bank}' not found"},
                status=status.HTTP_404_NOT_FOUND
            )

        bank_data = data["Banks"][bank]

        # Initialize result structure
        results = {
            "bank": bank,
            "years": years,
            "efficiency_trends": {},
            "liquidity_trends": {},
            "asset_quality_trends": {},
            "capital_trends": {}
        }

        # Calculate trend for Spread Ratio
        if "3. Net markup/interest income" in bank_data and "1. Markup/interest earned" in bank_data:
            spread_ratio_trend = BankDataService.calculate_ratio_trend(
                bank_data, "Spread Ratio",
                "3. Net markup/interest income", "1. Markup/interest earned",
                factor=100, years=years
            )
            results["efficiency_trends"]["spread_ratio"] = spread_ratio_trend

        # Calculate trend for Net Interest Margin
        if "3. Net markup/interest income" in bank_data and "C. Total assets (C1 to C4 + C8 to C10)" in bank_data:
            nim_trend = BankDataService.calculate_ratio_trend(
                bank_data, "Net Interest Margin",
                "3. Net markup/interest income", "C. Total assets (C1 to C4 + C8 to C10)",
                factor=100, years=years
            )
            results["efficiency_trends"]["net_interest_margin"] = nim_trend

        # Calculate trend for ROE
        if "10. Profit/(loss) after taxation" in bank_data and "A. Total equity (A1 to A3)" in bank_data:
            roe_trend = BankDataService.calculate_ratio_trend(
                bank_data, "Return on Equity",
                "10. Profit/(loss) after taxation", "A. Total equity (A1 to A3)",
                factor=100, years=years
            )
            results["efficiency_trends"]["return_on_equity"] = roe_trend

        # Calculate trend for ROA
        if "10. Profit/(loss) after taxation" in bank_data and "C. Total assets (C1 to C4 + C8 to C10)" in bank_data:
            roa_trend = BankDataService.calculate_ratio_trend(
                bank_data, "Return on Assets",
                "10. Profit/(loss) after taxation", "C. Total assets (C1 to C4 + C8 to C10)",
                factor=100, years=years
            )
            results["efficiency_trends"]["return_on_assets"] = roa_trend

        # Calculate trend for Non-Interest Income Ratio
        if "6. Non-markup/interest income" in bank_data and "C. Total assets (C1 to C4 + C8 to C10)" in bank_data:
            non_interest_income_trend = BankDataService.calculate_ratio_trend(
                bank_data, "Non-Interest Income Ratio",
                "6. Non-markup/interest income", "C. Total assets (C1 to C4 + C8 to C10)",
                factor=100, years=years
            )
            results["efficiency_trends"]["non_interest_income_ratio"] = non_interest_income_trend

        # Add liquidity ratios trends
        # Cash to Total Assets trend
        # We need to calculate this differently since it's a combined ratio
        cash_to_assets_trend = {}
        for year in years:
            try:
                if ("1. Cash and balances with treasury banks" in bank_data and year in bank_data[
                    "1. Cash and balances with treasury banks"] and
                        "2. Balances with other banks" in bank_data and year in bank_data[
                            "2. Balances with other banks"] and
                        "C. Total assets (C1 to C4 + C8 to C10)" in bank_data and year in bank_data[
                            "C. Total assets (C1 to C4 + C8 to C10)"] and
                        bank_data["C. Total assets (C1 to C4 + C8 to C10)"][year] > 0):
                    cash = bank_data["1. Cash and balances with treasury banks"][year]
                    balances = bank_data["2. Balances with other banks"][year]
                    total_assets = bank_data["C. Total assets (C1 to C4 + C8 to C10)"][year]
                    cash_ratio = ((cash + balances) / total_assets) * 100
                    cash_to_assets_trend[year] = round(cash_ratio, 2)
                else:
                    cash_to_assets_trend[year] = None
            except (KeyError, TypeError, ZeroDivisionError):
                cash_to_assets_trend[year] = None

        results["liquidity_trends"]["cash_to_total_assets"] = cash_to_assets_trend

        # Calculate other liquidity trend ratios
        # Investments to Total Assets
        if "4. Investments" in bank_data and "C. Total assets (C1 to C4 + C8 to C10)" in bank_data:
            inv_to_assets_trend = BankDataService.calculate_ratio_trend(
                bank_data, "Investments to Total Assets",
                "4. Investments", "C. Total assets (C1 to C4 + C8 to C10)",
                factor=100, years=years
            )
            results["liquidity_trends"]["investments_to_total_assets"] = inv_to_assets_trend

        # Advances to Total Assets
        if "8. Advances net of provision (C5-C7)" in bank_data and "C. Total assets (C1 to C4 + C8 to C10)" in bank_data:
            adv_to_assets_trend = BankDataService.calculate_ratio_trend(
                bank_data, "Advances to Total Assets",
                "8. Advances net of provision (C5-C7)", "C. Total assets (C1 to C4 + C8 to C10)",
                factor=100, years=years
            )
            results["liquidity_trends"]["advances_to_total_assets"] = adv_to_assets_trend

        # Deposits to Total Assets
        if "3. Deposits and other accounts" in bank_data and "C. Total assets (C1 to C4 + C8 to C10)" in bank_data:
            dep_to_assets_trend = BankDataService.calculate_ratio_trend(
                bank_data, "Deposits to Total Assets",
                "3. Deposits and other accounts", "C. Total assets (C1 to C4 + C8 to C10)",
                factor=100, years=years
            )
            results["liquidity_trends"]["deposits_to_total_assets"] = dep_to_assets_trend

        # Total Liabilities to Total Assets
        if "B. Total liabilities (B1 to B4)" in bank_data and "C. Total assets (C1 to C4 + C8 to C10)" in bank_data:
            liab_to_assets_trend = BankDataService.calculate_ratio_trend(
                bank_data, "Total Liabilities to Total Assets",
                "B. Total liabilities (B1 to B4)", "C. Total assets (C1 to C4 + C8 to C10)",
                factor=100, years=years
            )
            results["liquidity_trends"]["liabilities_to_total_assets"] = liab_to_assets_trend

        # Advances to Deposits
        if "8. Advances net of provision (C5-C7)" in bank_data and "3. Deposits and other accounts" in bank_data:
            adv_to_dep_trend = BankDataService.calculate_ratio_trend(
                bank_data, "Advances to Deposits",
                "8. Advances net of provision (C5-C7)", "3. Deposits and other accounts",
                factor=100, years=years
            )
            results["liquidity_trends"]["advances_to_deposits"] = adv_to_dep_trend

        # Gross Advances to Deposits
        if "5. Gross advances" in bank_data and "3. Deposits and other accounts" in bank_data:
            gross_adv_to_dep_trend = BankDataService.calculate_ratio_trend(
                bank_data, "Gross Advances to Deposits",
                "5. Gross advances", "3. Deposits and other accounts",
                factor=100, years=years
            )
            results["liquidity_trends"]["gross_advances_to_deposits"] = gross_adv_to_dep_trend

        # Calculate asset quality trend ratios
        # NPL to Gross Advances
        if "6. Advances-non-performing/classified" in bank_data and "5. Gross advances" in bank_data:
            npl_to_adv_trend = BankDataService.calculate_ratio_trend(
                bank_data, "NPL to Gross Advances",
                "6. Advances-non-performing/classified", "5. Gross advances",
                factor=100, years=years
            )
            results["asset_quality_trends"]["npl_to_gross_advances"] = npl_to_adv_trend

        # Provisions against NPLs to Gross Advances
        if "7. Provision against advances" in bank_data and "5. Gross advances" in bank_data:
            prov_to_adv_trend = BankDataService.calculate_ratio_trend(
                bank_data, "Provisions against NPLs to Gross Advances",
                "7. Provision against advances", "5. Gross advances",
                factor=100, years=years
            )
            results["asset_quality_trends"]["provisions_to_gross_advances"] = prov_to_adv_trend

        # Provision Coverage
        if "7. Provision against advances" in bank_data and "6. Advances-non-performing/classified" in bank_data:
            prov_coverage_trend = BankDataService.calculate_ratio_trend(
                bank_data, "Provision Coverage",
                "7. Provision against advances", "6. Advances-non-performing/classified",
                factor=100, years=years
            )
            results["asset_quality_trends"]["provision_coverage"] = prov_coverage_trend

        # NPL to Equity
        if "6. Advances-non-performing/classified" in bank_data and "A. Total equity (A1 to A3)" in bank_data:
            npl_to_equity_trend = BankDataService.calculate_ratio_trend(
                bank_data, "NPL to Equity",
                "6. Advances-non-performing/classified", "A. Total equity (A1 to A3)",
                factor=100, years=years
            )
            results["asset_quality_trends"]["npl_to_equity"] = npl_to_equity_trend

        # Calculate capital trend ratios
        # Capital to Assets
        if "A. Total equity (A1 to A3)" in bank_data and "C. Total assets (C1 to C4 + C8 to C10)" in bank_data:
            capital_ratio_trend = BankDataService.calculate_ratio_trend(
                bank_data, "Capital to Assets",
                "A. Total equity (A1 to A3)", "C. Total assets (C1 to C4 + C8 to C10)",
                factor=100, years=years
            )
            results["capital_trends"]["capital_to_assets"] = capital_ratio_trend

        # Deposits to Equity
        if "3. Deposits and other accounts" in bank_data and "A. Total equity (A1 to A3)" in bank_data:
            dep_to_equity_trend = BankDataService.calculate_ratio_trend(
                bank_data, "Deposits to Equity",
                "3. Deposits and other accounts", "A. Total equity (A1 to A3)",
                factor=1, years=years  # No percentage for this ratio
            )
            results["capital_trends"]["deposits_to_equity"] = dep_to_equity_trend

        return Response(results)

    # Keep the POST method for backward compatibility
    def post(self, request):
        bank = request.data.get("bank", "")
        years = request.data.get("years", BankDataService.get_years())

        # Validate incoming data
        if not bank:
            return Response(
                {"error": "Please provide a bank to analyze"},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Create a mock request with query parameters
        mock_request = request._request
        mock_request.GET = {
            "bank": bank,
            "years": ",".join(years) if isinstance(years, list) else years
        }

        # Call the GET method with the mock request
        return self.get(mock_request)