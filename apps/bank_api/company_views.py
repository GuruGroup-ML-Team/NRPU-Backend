# from django.shortcuts import render
# from rest_framework.views import APIView
# from rest_framework.response import Response
# from rest_framework import status
# from .company_services import CompanyDataService
# from .company_serializers import CompanyComparisonSerializer, CompanyScoreSerializer


# class CompanyListAPIView(APIView):
#     """
#     API endpoint that returns a list of companies.
#     """

#     def get(self, request):
#         companies = CompanyDataService.get_listed_companies()
#         return Response({"companies": companies})


# class CompanyDetailAPIView(APIView):
#     """
#     API endpoint that returns detailed information about a specific company.
#     """

#     def get(self, request, company_name):
#         data = CompanyDataService.get_company_data()

#         # Check if company exists
#         if company_name not in data["Companies"]:
#             return Response(
#                 {"error": f"Company '{company_name}' not found"},
#                 status=status.HTTP_404_NOT_FOUND
#             )

#         company_data = data["Companies"][company_name]
#         return Response(company_data)


# class CompanyComparisonAPIView(APIView):
#     """
#     API endpoint that compares multiple companies based on selected indicators.
#     """

#     def post(self, request):
#         serializer = CompanyComparisonSerializer(data=request.data)
#         if not serializer.is_valid():
#             return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#         companies = serializer.validated_data["companies"]
#         indicators = serializer.validated_data["indicators"]
#         year = serializer.validated_data["year"]

#         comparison_data = CompanyDataService.get_company_comparison_data(companies, indicators, year)
#         return Response(comparison_data)


# class CompanyRankingAPIView(APIView):
#     """
#     API endpoint that returns rankings of companies based on a specific indicator.
#     """

#     def get(self, request):
#         indicator = request.query_params.get("indicator", "F. Operations: - 1. Sales")
#         year = request.query_params.get("year", "2022")

#         data = CompanyDataService.get_company_data()
#         rankings = []

#         for company_name, company_data in data["Companies"].items():
#             # Skip industry averages and aggregates
#             if "average" in company_name.lower() or "all" in company_name.lower():
#                 continue

#             company_indicators = company_data.get("Indicators", {})
#             if indicator in company_indicators and year in company_indicators[indicator]:
#                 rankings.append({
#                     "company": company_name,
#                     "sector": company_data.get("Sector", ""),
#                     "sub_sector": company_data.get("Sub-Sector", ""),
#                     "value": company_indicators[indicator][year]
#                 })

#         # Sort by the indicator value in descending order
#         rankings.sort(key=lambda x: x["value"], reverse=True)

#         # Add rank
#         for i, item in enumerate(rankings):
#             item["rank"] = i + 1

#         return Response(rankings)


# class CompanyFinancialAnalysisAPIView(APIView):
#     """
#     API endpoint that provides financial analysis for a specific company.
#     """

#     def get(self, request, company_name):
#         data = CompanyDataService.get_company_data()

#         # Check if company exists
#         if company_name not in data["Companies"]:
#             return Response(
#                 {"error": f"Company '{company_name}' not found"},
#                 status=status.HTTP_404_NOT_FOUND
#             )

#         company_data = data["Companies"][company_name]
#         company_indicators = company_data.get("Indicators", {})
#         year = request.query_params.get("year", "2022")

#         # Find industry data for comparison
#         industry_data = None
#         for name, info in data["Companies"].items():
#             if "industry average" in name.lower() and info.get("Sub-Sector") == company_data.get("Sub-Sector"):
#                 industry_data = info
#                 break

#         # If no sub-sector match, try sector match
#         if not industry_data:
#             for name, info in data["Companies"].items():
#                 if "industry average" in name.lower() and info.get("Sector") == company_data.get("Sector"):
#                     industry_data = info
#                     break

#         # Calculate financial ratios and metrics
#         analysis = {
#             "company_name": company_name,
#             "sector": company_data.get("Sector"),
#             "sub_sector": company_data.get("Sub-Sector"),
#             "year": year,
#             "metrics": {},
#             "ratios": {},
#             "growth": {},
#             "industry_comparison": {}
#         }

#         # Add key metrics if available
#         key_metrics = [
#             "F. Operations: - 1. Sales",  # Sales/Revenue
#             "Total Assets (A+B) / Equity & Liabilities (C+D+E)",  # Total Assets
#             "C. Shareholders' Equity (C1+C2+C3)",  # Total Equity
#             "F. Operations: - 10. Profit / (loss) after tax (F8-F9)"  # Net Income
#         ]

#         for metric in key_metrics:
#             if metric in company_indicators and year in company_indicators[metric]:
#                 # Create a more readable name for the metric
#                 readable_name = metric.split(" - ")[-1]
#                 if " (" in readable_name:
#                     readable_name = readable_name.split(" (")[0]

#                 analysis["metrics"][readable_name.lower().replace(" ", "_").replace("/", "_")] = \
#                 company_indicators[metric][year]

#         # Calculate financial ratios
#         financial_ratios = CompanyDataService.calculate_company_financial_ratios(company_data, year)
#         analysis["ratios"] = financial_ratios

#         # Calculate growth rates for key metrics
#         prev_year = str(int(year) - 1)
#         for metric in key_metrics:
#             if (metric in company_indicators and
#                     year in company_indicators[metric] and
#                     prev_year in company_indicators[metric] and
#                     company_indicators[metric][prev_year] != 0):

#                 # Create a more readable name for the metric
#                 readable_name = metric.split(" - ")[-1]
#                 if " (" in readable_name:
#                     readable_name = readable_name.split(" (")[0]

#                 current_year_value = company_indicators[metric][year]
#                 previous_year_value = company_indicators[metric][prev_year]
#                 growth_rate = ((current_year_value - previous_year_value) / previous_year_value) * 100
#                 analysis["growth"][f"{readable_name.lower().replace(' ', '_').replace('/', '_')}_growth"] = round(
#                     growth_rate, 2)

#         # Calculate industry comparison if industry data is available
#         if industry_data:
#             industry_indicators = industry_data.get("Indicators", {})
#             for metric in key_metrics:
#                 if (metric in company_indicators and year in company_indicators[metric] and
#                         metric in industry_indicators and year in industry_indicators[metric] and
#                         industry_indicators[metric][year] != 0):

#                     # Create a more readable name for the metric
#                     readable_name = metric.split(" - ")[-1]
#                     if " (" in readable_name:
#                         readable_name = readable_name.split(" (")[0]

#                     market_share = (company_indicators[metric][year] / industry_indicators[metric][year]) * 100
#                     analysis["industry_comparison"][
#                         f"{readable_name.lower().replace(' ', '_').replace('/', '_')}_vs_industry"] = round(
#                         market_share, 2)

#         return Response(analysis)


# class CompanySectorListAPIView(APIView):
#     """
#     API endpoint that returns a list of all company sectors.
#     """

#     def get(self, request):
#         sectors = CompanyDataService.get_company_sectors()
#         return Response({"sectors": sectors})


# class CompanySubSectorListAPIView(APIView):
#     """
#     API endpoint that returns a list of sub-sectors for a given sector.
#     """

#     def get(self, request):
#         sector = request.query_params.get("sector")
#         if not sector:
#             return Response(
#                 {"error": "Sector parameter is required"},
#                 status=status.HTTP_400_BAD_REQUEST
#             )

#         sub_sectors = CompanyDataService.get_company_sub_sectors(sector)
#         return Response({"sub_sectors": sub_sectors})


# class CompaniesbySubSectorAPIView(APIView):
#     """
#     API endpoint that returns a list of companies for a given sub-sector.
#     """

#     def get(self, request):
#         sub_sector = request.query_params.get("sub_sector")
#         if not sub_sector:
#             return Response(
#                 {"error": "Sub-sector parameter is required"},
#                 status=status.HTTP_400_BAD_REQUEST
#             )

#         companies = CompanyDataService.get_companies_by_sub_sector(sub_sector)
#         return Response({"companies": companies})


# class CompanyIndicatorsListAPIView(APIView):
#     """
#     API endpoint that returns a list of available company indicators.
#     """

#     def get(self, request):
#         indicators = CompanyDataService.get_company_indicators()
#         return Response({"indicators": indicators})


# class CompanySubIndicatorsListAPIView(APIView):
#     """
#     API endpoint that returns a list of sub-indicators for a given indicator.
#     """

#     def get(self, request):
#         indicator = request.query_params.get("indicator")
#         if not indicator:
#             return Response(
#                 {"error": "Indicator parameter is required"},
#                 status=status.HTTP_400_BAD_REQUEST
#             )

#         sub_indicators = CompanyDataService.get_company_sub_indicators(indicator)
#         return Response({"sub_indicators": sub_indicators})


# class CompanyYearsListAPIView(APIView):
#     """
#     API endpoint that returns a list of available years for company data.
#     """

#     def get(self, request):
#         years = CompanyDataService.get_company_years()
#         return Response({"years": years})


# class CompanyComparativeAnalysisAPIView(APIView):
#     """
#     API endpoint that provides comparative financial ratio analysis between companies.
#     """

#     def get(self, request):
#         # Get parameters from query parameters
#         companies_param = request.query_params.get("companies", "")
#         companies = companies_param.split(",") if companies_param else []
#         year = request.query_params.get("year", "2022")  # Default to 2022 if not specified

#         # Validate parameters
#         if not companies:
#             return Response(
#                 {"error": "Please provide a list of companies to compare using the 'companies' query parameter"},
#                 status=status.HTTP_400_BAD_REQUEST
#             )

#         # Get company data
#         data = CompanyDataService.get_company_data()

#         # Check if all companies exist
#         for company in companies:
#             if company not in data["Companies"]:
#                 return Response(
#                     {"error": f"Company '{company}' not found"},
#                     status=status.HTTP_404_NOT_FOUND
#                 )

#         # Calculate ratios for each company
#         results = {}
#         for company in companies:
#             company_data = data["Companies"][company]

#             # Initialize company result with basic information
#             results[company] = {
#                 "basic_info": {
#                     "name": company,
#                     "sector": company_data.get("Sector"),
#                     "sub_sector": company_data.get("Sub-Sector"),
#                     "year": year
#                 },
#                 "profitability_ratios": {},
#                 "liquidity_ratios": {},
#                 "efficiency_ratios": {},
#                 "solvency_ratios": {},
#                 "cash_flow_ratios": {},
#                 "valuation_ratios": {}
#             }

#             # Get basic metrics if available
#             company_indicators = company_data.get("Indicators", {})

#             # Total Assets
#             if "Total Assets (A+B) / Equity & Liabilities (C+D+E)" in company_indicators and year in company_indicators[
#                 "Total Assets (A+B) / Equity & Liabilities (C+D+E)"]:
#                 results[company]["basic_info"]["total_assets"] = \
#                 company_indicators["Total Assets (A+B) / Equity & Liabilities (C+D+E)"][year]

#             # Revenue/Sales
#             if "F. Operations: - 1. Sales" in company_indicators and year in company_indicators[
#                 "F. Operations: - 1. Sales"]:
#                 results[company]["basic_info"]["revenue"] = company_indicators["F. Operations: - 1. Sales"][year]

#             # Calculate all financial ratios using the service
#             calculated_ratios = CompanyDataService.calculate_company_financial_ratios(company_data, year)

#             # Copy calculated ratios to our results with standard names
#             from bank_api.company_constants import (
#                 COMPANY_PROFITABILITY_RATIOS, COMPANY_LIQUIDITY_RATIOS, COMPANY_EFFICIENCY_RATIOS,
#                 COMPANY_SOLVENCY_RATIOS, COMPANY_CASH_FLOW_RATIOS, COMPANY_VALUATION_RATIOS
#             )

#             # Map the internal ratio categories to output keys
#             ratio_mapping = {
#                 COMPANY_PROFITABILITY_RATIOS: "profitability_ratios",
#                 COMPANY_LIQUIDITY_RATIOS: "liquidity_ratios",
#                 COMPANY_EFFICIENCY_RATIOS: "efficiency_ratios",
#                 COMPANY_SOLVENCY_RATIOS: "solvency_ratios",
#                 COMPANY_CASH_FLOW_RATIOS: "cash_flow_ratios",
#                 COMPANY_VALUATION_RATIOS: "valuation_ratios"
#             }

#             for category_key, output_key in ratio_mapping.items():
#                 if category_key in calculated_ratios:
#                     results[company][output_key] = calculated_ratios[category_key]

#         # Try to add industry average if available
#         industry_data = None

#         # First try to find industry average for the specific sub-sector
#         company_sub_sector = data["Companies"][companies[0]].get("Sub-Sector")
#         for name, info in data["Companies"].items():
#             if "industry average" in name.lower() and info.get("Sub-Sector") == company_sub_sector:
#                 industry_data = info
#                 break

#         # If not found, try sector level
#         if not industry_data:
#             company_sector = data["Companies"][companies[0]].get("Sector")
#             for name, info in data["Companies"].items():
#                 if "industry average" in name.lower() and info.get("Sector") == company_sector:
#                     industry_data = info
#                     break

#         # If still not found, try any industry average
#         if not industry_data:
#             for name, info in data["Companies"].items():
#                 if "industry average" in name.lower():
#                     industry_data = info
#                     break

#         if industry_data:
#             # Calculate all financial ratios for the industry averages
#             industry_ratios = CompanyDataService.calculate_company_financial_ratios(industry_data, year)

#             # Add industry basic info
#             results["Industry Average"] = {
#                 "basic_info": {
#                     "name": "Industry Average",
#                     "sector": industry_data.get("Sector"),
#                     "sub_sector": industry_data.get("Sub-Sector"),
#                     "year": year
#                 },
#                 "profitability_ratios": {},
#                 "liquidity_ratios": {},
#                 "efficiency_ratios": {},
#                 "solvency_ratios": {},
#                 "cash_flow_ratios": {},
#                 "valuation_ratios": {}
#             }

#             # Copy industry ratios to the results
#             for category_key, output_key in ratio_mapping.items():
#                 if category_key in industry_ratios:
#                     results["Industry Average"][output_key] = industry_ratios[category_key]

#             # Add some basic industry metrics
#             industry_indicators = industry_data.get("Indicators", {})

#             # Total Assets
#             if "Total Assets (A+B) / Equity & Liabilities (C+D+E)" in industry_indicators and year in \
#                     industry_indicators["Total Assets (A+B) / Equity & Liabilities (C+D+E)"]:
#                 results["Industry Average"]["basic_info"]["total_assets"] = \
#                 industry_indicators["Total Assets (A+B) / Equity & Liabilities (C+D+E)"][year]

#             # Revenue/Sales
#             if "F. Operations: - 1. Sales" in industry_indicators and year in industry_indicators[
#                 "F. Operations: - 1. Sales"]:
#                 results["Industry Average"]["basic_info"]["revenue"] = industry_indicators["F. Operations: - 1. Sales"][
#                     year]

#         return Response(results)

#     # Keep the POST method for backward compatibility
#     def post(self, request):
#         companies = request.data.get("companies", [])
#         year = request.data.get("year", "2022")

#         # Validate incoming data
#         if not companies or not isinstance(companies, list):
#             return Response(
#                 {"error": "Please provide a list of companies to compare"},
#                 status=status.HTTP_400_BAD_REQUEST
#             )

#         # Create a mock request with query parameters
#         mock_request = request._request
#         mock_request.GET = {
#             "companies": ",".join(companies),
#             "year": year
#         }

#         # Call the GET method with the mock request
#         return self.get(mock_request)


# class CompanyScoreAPIView(APIView):
#     """
#     API endpoint that calculates an overall financial score for companies.
#     """

#     def get(self, request):
#         # Get parameters from query parameters
#         companies_param = request.query_params.get("companies", "")
#         companies = companies_param.split(",") if companies_param else []
#         year = request.query_params.get("year", "2022")

#         # Get weights from query parameters
#         profitability_weight = float(request.query_params.get("profitability_weight", "0.50"))
#         liquidity_weight = float(request.query_params.get("liquidity_weight", "0.25"))
#         activity_weight = float(request.query_params.get("activity_weight", "0.15"))
#         solvency_weight = float(request.query_params.get("solvency_weight", "0.10"))

#         weights = {
#             "profitability": profitability_weight,
#             "liquidity": liquidity_weight,
#             "activity": activity_weight,
#             "solvency": solvency_weight
#         }

#         # Validate parameters
#         if not companies:
#             return Response(
#                 {"error": "Please provide a list of companies to score using the 'companies' query parameter"},
#                 status=status.HTTP_400_BAD_REQUEST
#             )

#         # Get company data
#         data = CompanyDataService.get_company_data()

#         # Calculate scores for each company
#         results = {}
#         for company in companies:
#             if company not in data["Companies"]:
#                 return Response(
#                     {"error": f"Company '{company}' not found"},
#                     status=status.HTTP_404_NOT_FOUND
#                 )

#             company_data = data["Companies"][company]

#             # Use the calculate_company_score method from CompanyDataService
#             company_score = CompanyDataService.calculate_company_score(company_data, weights, year)
#             results[company] = company_score

#         return Response(results)

#     def post(self, request):
#         """
#         Handle POST requests for company scoring
#         """
#         serializer = CompanyScoreSerializer(data=request.data)
#         if not serializer.is_valid():
#             return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#         companies = serializer.validated_data["companies"]
#         year = serializer.validated_data["year"]
#         weights = serializer.validated_data["weights"]

#         # Get company data
#         data = CompanyDataService.get_company_data()

#         # Calculate scores for each company
#         results = {}
#         for company in companies:
#             if company not in data["Companies"]:
#                 return Response(
#                     {"error": f"Company '{company}' not found"},
#                     status=status.HTTP_404_NOT_FOUND
#                 )

#             company_data = data["Companies"][company]

#             # Calculate company score
#             company_score = CompanyDataService.calculate_company_score(company_data, weights, year)
#             results[company] = company_score

#         return Response(results)


# class CompanyTrendAnalysisAPIView(APIView):
#     """
#     API endpoint that provides trend analysis for company financial ratios over multiple years.
#     """

#     def get(self, request):
#         # Get parameters from query parameters
#         company = request.query_params.get("company", "")
#         years_param = request.query_params.get("years", "")
#         years = years_param.split(",") if years_param else CompanyDataService.get_company_years()

#         # Validate parameters
#         if not company:
#             return Response(
#                 {"error": "Please provide a company to analyze using the 'company' query parameter"},
#                 status=status.HTTP_400_BAD_REQUEST
#             )

#         # Get company data
#         data = CompanyDataService.get_company_data()

#         # Check if company exists
#         if company not in data["Companies"]:
#             return Response(
#                 {"error": f"Company '{company}' not found"},
#                 status=status.HTTP_404_NOT_FOUND
#             )

#         company_data = data["Companies"][company]
#         indicators = company_data.get("Indicators", {})

#         # Initialize result structure
#         results = {
#             "company": company,
#             "sector": company_data.get("Sector"),
#             "sub_sector": company_data.get("Sub-Sector"),
#             "years": years,
#             "profitability_trends": {},
#             "liquidity_trends": {},
#             "efficiency_trends": {},
#             "solvency_trends": {},
#             "cash_flow_trends": {}
#         }

#         # Map our internal ratio categories to output categories
#         from bank_api.company_constants import (
#             COMPANY_PROFITABILITY_RATIOS, COMPANY_LIQUIDITY_RATIOS, COMPANY_EFFICIENCY_RATIOS,
#             COMPANY_SOLVENCY_RATIOS, COMPANY_CASH_FLOW_RATIOS, COMPANY_FINANCIAL_FIELDS
#         )

#         # Check for pre-calculated ratios first in the Key Performance Indicators
#         # If present, use those directly for trend analysis
#         kpi_prefixes = {
#             "I. Key Performance Indicators - Profitability Ratios": "profitability_trends",
#             "I. Key Performance Indicators - Liquidity Ratios": "liquidity_trends",
#             "I. Key Performance Indicators - Activity Ratios": "efficiency_trends",
#             "I. Key Performance Indicators - Solvency Ratios": "solvency_trends",
#             "I. Key Performance Indicators - Cash Flow Ratios": "cash_flow_trends"
#         }

#         # Collect pre-calculated ratio trends
#         for kpi_prefix, trend_key in kpi_prefixes.items():
#             for indicator_key in indicators:
#                 if indicator_key.startswith(kpi_prefix):
#                     ratio_name = indicator_key.replace(kpi_prefix + " - ", "").lower().replace(" ", "_")
#                     ratio_trend = {}
#                     for year in years:
#                         if year in indicators[indicator_key]:
#                             ratio_trend[year] = indicators[indicator_key][year]
#                         else:
#                             ratio_trend[year] = None
#                     results[trend_key][ratio_name] = ratio_trend

#         # If we don't have pre-calculated ratios, calculate them from raw data
#         if not any(list(category.values()) for category in [
#             results["profitability_trends"],
#             results["liquidity_trends"],
#             results["efficiency_trends"],
#             results["solvency_trends"],
#             results["cash_flow_trends"]
#         ]):
#             # Calculate trend for ROE
#             results["profitability_trends"]["return_on_equity"] = CompanyDataService.calculate_company_ratio_trend(
#                 company_data, "Return on Equity",
#                 "NET_PROFIT", "TOTAL_EQUITY",
#                 factor=100, years=years
#             )

#             # Calculate trend for ROA
#             results["profitability_trends"]["return_on_assets"] = CompanyDataService.calculate_company_ratio_trend(
#                 company_data, "Return on Assets",
#                 "NET_PROFIT", "TOTAL_ASSETS",
#                 factor=100, years=years
#             )

#             # Calculate trend for Net Profit Margin
#             results["profitability_trends"]["net_profit_margin"] = CompanyDataService.calculate_company_ratio_trend(
#                 company_data, "Net Profit Margin",
#                 "NET_PROFIT", "SALES",
#                 factor=100, years=years
#             )

#             # Calculate trend for Gross Profit Margin
#             results["profitability_trends"]["gross_profit_margin"] = CompanyDataService.calculate_company_ratio_trend(
#                 company_data, "Gross Profit Margin",
#                 "GROSS_PROFIT", "SALES",
#                 factor=100, years=years
#             )

#             # Calculate trend for Current Ratio
#             results["liquidity_trends"]["current_ratio"] = CompanyDataService.calculate_company_ratio_trend(
#                 company_data, "Current Ratio",
#                 "TOTAL_CURRENT_ASSETS", "TOTAL_CURRENT_LIABILITIES",
#                 factor=1, years=years
#             )

#             # Quick Ratio Trend - requires special calculation
#             quick_ratio_trend = {}
#             for year in years:
#                 try:
#                     current_assets_key = COMPANY_FINANCIAL_FIELDS["TOTAL_CURRENT_ASSETS"]
#                     inventory_key = COMPANY_FINANCIAL_FIELDS["INVENTORIES"]
#                     current_liabilities_key = COMPANY_FINANCIAL_FIELDS["TOTAL_CURRENT_LIABILITIES"]

#                     if (current_assets_key in indicators and year in indicators[current_assets_key] and
#                             inventory_key in indicators and year in indicators[inventory_key] and
#                             current_liabilities_key in indicators and year in indicators[current_liabilities_key] and
#                             indicators[current_liabilities_key][year] > 0):

#                         current_assets = indicators[current_assets_key][year]
#                         inventory = indicators[inventory_key][year]
#                         current_liabilities = indicators[current_liabilities_key][year]

#                         quick_ratio = (current_assets - inventory) / current_liabilities
#                         quick_ratio_trend[year] = round(quick_ratio, 2)
#                     else:
#                         quick_ratio_trend[year] = None
#                 except (KeyError, TypeError, ZeroDivisionError):
#                     quick_ratio_trend[year] = None

#             results["liquidity_trends"]["quick_ratio"] = quick_ratio_trend

#             # Calculate trend for Asset Turnover
#             results["efficiency_trends"]["asset_turnover"] = CompanyDataService.calculate_company_ratio_trend(
#                 company_data, "Asset Turnover",
#                 "SALES", "TOTAL_ASSETS",
#                 factor=1, years=years
#             )

#             # Calculate trend for Inventory Turnover
#             results["efficiency_trends"]["inventory_turnover"] = CompanyDataService.calculate_company_ratio_trend(
#                 company_data, "Inventory Turnover",
#                 "COST_OF_SALES", "INVENTORIES",
#                 factor=1, years=years
#             )

#             # Calculate trend for Debt-to-Equity ratio
#             # This requires special handling as we need to combine long-term and short-term debt
#             debt_to_equity_trend = {}
#             for year in years:
#                 try:
#                     long_term_debt_key = COMPANY_FINANCIAL_FIELDS["LONG_TERM_BORROWINGS"]
#                     short_term_debt_key = COMPANY_FINANCIAL_FIELDS["SHORT_TERM_BORROWINGS"]
#                     equity_key = COMPANY_FINANCIAL_FIELDS["TOTAL_EQUITY"]

#                     long_term_debt = indicators.get(long_term_debt_key, {}).get(year, 0) or 0
#                     short_term_debt = indicators.get(short_term_debt_key, {}).get(year, 0) or 0
#                     equity = indicators.get(equity_key, {}).get(year)

#                     if equity and equity > 0:
#                         total_debt = long_term_debt + short_term_debt
#                         debt_to_equity = total_debt / equity
#                         debt_to_equity_trend[year] = round(debt_to_equity, 2)
#                     else:
#                         debt_to_equity_trend[year] = None
#                 except (KeyError, TypeError, ZeroDivisionError):
#                     debt_to_equity_trend[year] = None

#             results["solvency_trends"]["debt_to_equity"] = debt_to_equity_trend

#             # Calculate trend for Equity Ratio
#             results["solvency_trends"]["equity_ratio"] = CompanyDataService.calculate_company_ratio_trend(
#                 company_data, "Equity Ratio",
#                 "TOTAL_EQUITY", "TOTAL_ASSETS",
#                 factor=100, years=years
#             )

#             # Calculate trend for Interest Coverage
#             results["solvency_trends"]["interest_coverage"] = CompanyDataService.calculate_company_ratio_trend(
#                 company_data, "Interest Coverage",
#                 "EBIT", "FINANCIAL_EXPENSES",
#                 factor=1, years=years
#             )

#             # Calculate trend for Operating Cash Flow to Sales
#             results["cash_flow_trends"]["ocf_to_sales"] = CompanyDataService.calculate_company_ratio_trend(
#                 company_data, "Operating Cash Flow to Sales",
#                 "OPERATING_CASH_FLOW", "SALES",
#                 factor=100, years=years
#             )

#         return Response(results)

#     # Keep the POST method for backward compatibility
#     def post(self, request):
#         company = request.data.get("company", "")
#         years = request.data.get("years", CompanyDataService.get_company_years())

#         # Validate incoming data
#         if not company:
#             return Response(
#                 {"error": "Please provide a company to analyze"},
#                 status=status.HTTP_400_BAD_REQUEST
#             )

#         # Create a mock request with query parameters
#         mock_request = request._request
#         mock_request.GET = {
#             "company": company,
#             "years": ",".join(years) if isinstance(years, list) else years
#         }

#         # Call the GET method with the mock request
#         return self.get(mock_request)

















from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import pandas as pd
import numpy as np
from .company_constants import COMPANY_FINANCIAL_FIELDS  # Use centralized financial fields
from .company_services import CompanyDataService  # Use reusable services


class CreditRiskAssessmentView(APIView):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        try:
            self.df_financials = pd.read_csv("/mnt/data/company_data.csv")
            self.df_banks = pd.read_csv("/mnt/data/fsabanks.csv")
            self.industry_averages = CompanyDataService.get_industry_averages(self.df_financials)
            print("Datasets loaded successfully.")
        except Exception as e:
            print(f"Error loading datasets: {str(e)}")
            self.df_financials = pd.DataFrame()
            self.df_banks = pd.DataFrame()
            self.industry_averages = {}

    def _calculate_all_ratios(self, df):
        """Calculate key financial ratios using standardized fields."""
        try:
            df_ratios = df.copy()
            df_ratios['ROE'] = df_ratios[COMPANY_FINANCIAL_FIELDS['NET_PROFIT']] / df_ratios[COMPANY_FINANCIAL_FIELDS['TOTAL_EQUITY']]
            df_ratios['ROA'] = df_ratios[COMPANY_FINANCIAL_FIELDS['NET_PROFIT']] / df_ratios[COMPANY_FINANCIAL_FIELDS['TOTAL_ASSETS']]
            df_ratios['Capital_Ratio'] = df_ratios[COMPANY_FINANCIAL_FIELDS['TOTAL_EQUITY']] / df_ratios[COMPANY_FINANCIAL_FIELDS['TOTAL_ASSETS']]
            df_ratios['Total_Liabilities_to_Total_Assets'] = df_ratios[COMPANY_FINANCIAL_FIELDS['TOTAL_LIABILITIES']] / df_ratios[COMPANY_FINANCIAL_FIELDS['TOTAL_ASSETS']]
            return df_ratios
        except Exception as e:
            print(f"Error calculating ratios: {str(e)}")
            return df

    def get(self, request):
        try:
            sector = request.query_params.get('sector')
            year = request.query_params.get('year')
            company_name = request.query_params.get('company')
            include_benchmarking = request.query_params.get('benchmark', 'true').lower() == 'true'

            df_filtered = CompanyDataService.filter_data(self.df_financials, sector, year, company_name)
            if df_filtered.empty:
                return Response({"message": "No data found matching the criteria."}, status=status.HTTP_404_NOT_FOUND)

            credit_scores = CompanyDataService.calculate_credit_score(df_filtered, include_benchmarking)
            return Response({"credit_scores": credit_scores}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
