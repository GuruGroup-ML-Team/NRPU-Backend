# from django.shortcuts import render
# from rest_framework.views import APIView
# from rest_framework.response import Response
# from rest_framework import status
# from .services.bank_services import BankDataService
# from .serializers import BankComparisonSerializer

# class BankAPIView(APIView):
#     """
#     Consolidated API endpoint for all bank-related operations.
#     Similar structure to AltmanZScoreView where endpoints are determined by query parameters.
#     """
    
#     def __init__(self, **kwargs):
#         super().__init__(**kwargs)
#         self.bank_service = BankDataService()

#     def get(self, request):
#         """
#         Handle all GET requests based on query parameters.
#         """
#         # Bank listing endpoint
#         if 'listed_banks' in request.query_params:
#             banks = self.bank_service.get_listed_banks()
#             return Response({"banks": banks})

#         # Bank detail endpoint
#         bank_name = request.query_params.get('bank_name')
#         if bank_name:
#             data = self.bank_service.get_bank_data()
#             if bank_name not in data["Banks"]:
#                 return Response(
#                     {"error": f"Bank '{bank_name}' not found"},
#                     status=status.HTTP_404_NOT_FOUND
#                 )
#             return Response(data["Banks"][bank_name])

#         # Bank ranking endpoint
#         if 'ranking' in request.query_params:
#             metric = request.query_params.get("metric", "Assets")
#             year = request.query_params.get("year", "2023")

#             data = self.bank_service.get_bank_data()
#             rankings = []

#             for bank_name, bank_data in data["Banks"].items():
#                 if bank_name != "All Banks" and metric in bank_data and year in bank_data[metric]:
#                     rankings.append({
#                         "bank": bank_name,
#                         "value": bank_data[metric][year]
#                     })

#             rankings.sort(key=lambda x: x["value"], reverse=True)
#             for i, item in enumerate(rankings):
#                 item["rank"] = i + 1

#             return Response(rankings)

#         # Financial analysis endpoint
#         if 'financial_analysis' in request.query_params and bank_name:
#             data = self.bank_service.get_bank_data()
#             if bank_name not in data["Banks"]:
#                 return Response(
#                     {"error": f"Bank '{bank_name}' not found"},
#                     status=status.HTTP_404_NOT_FOUND
#                 )

#             bank_data = data["Banks"][bank_name]
#             all_banks_data = data["Banks"]["All Banks"]

#             analysis = {
#                 "bank_name": bank_name,
#                 "year": "2023",
#                 "metrics": {},
#                 "ratios": {},
#                 "growth": {},
#                 "industry_comparison": {}
#             }

#             if "Assets" in bank_data and "2023" in bank_data["Assets"]:
#                 analysis["metrics"]["total_assets"] = bank_data["Assets"]["2023"]

#             if "Revenue" in bank_data and "2023" in bank_data["Revenue"]:
#                 analysis["metrics"]["revenue"] = bank_data["Revenue"]["2023"]

#             if "A. Total equity (A1 to A3)" in bank_data and "2023" in bank_data["A. Total equity (A1 to A3)"]:
#                 analysis["metrics"]["total_equity"] = bank_data["A. Total equity (A1 to A3)"]["2023"]

#             for metric in ["Assets", "Revenue", "A. Total equity (A1 to A3)"]:
#                 if metric in bank_data and "2022" in bank_data[metric] and "2023" in bank_data[metric]:
#                     current_year = bank_data[metric]["2023"]
#                     previous_year = bank_data[metric]["2022"]
#                     growth_rate = ((current_year - previous_year) / previous_year) * 100
#                     analysis["growth"][f"{metric.lower()}_growth"] = round(growth_rate, 2)

#             if "Assets" in bank_data and "2023" in bank_data["Assets"]:
#                 if "Assets" in all_banks_data and "2023" in all_banks_data["Assets"]:
#                     market_share = (bank_data["Assets"]["2023"] / all_banks_data["Assets"]["2023"]) * 100
#                     analysis["industry_comparison"]["asset_market_share"] = round(market_share, 2)

#             return Response(analysis)

#         # Sector list endpoint
#         if 'sectors' in request.query_params:
#             sectors = self.bank_service.get_sectors()
#             return Response({"sectors": sectors})

#         # Sub-sector list endpoint
#         sector = request.query_params.get('sector')
#         if 'sub_sectors' in request.query_params:
#             if not sector:
#                 return Response(
#                     {"error": "Sector parameter is required"},
#                     status=status.HTTP_400_BAD_REQUEST
#                 )
#             sub_sectors = self.bank_service.get_sub_sectors(sector)
#             return Response({"sub_sectors": sub_sectors})

#         # Banks by sub-sector endpoint
#         sub_sector = request.query_params.get('sub_sector')
#         if 'banks_by_sub_sector' in request.query_params:
#             if not sub_sector:
#                 return Response(
#                     {"error": "Sub-sector parameter is required"},
#                     status=status.HTTP_400_BAD_REQUEST
#                 )
#             banks = self.bank_service.get_banks_by_sub_sector(sub_sector)
#             return Response({"banks": banks})

#         # Metrics list endpoint
#         if 'metrics' in request.query_params:
#             metrics = self.bank_service.get_metrics()
#             return Response({"metrics": metrics})

#         # Years list endpoint
#         if 'years' in request.query_params:
#             years = self.bank_service.get_years()
#             return Response({"years": years})

#         # Comparative analysis endpoint
#         if 'comparative_analysis' in request.query_params:
#             banks_param = request.query_params.get("banks", "")
#             banks = banks_param.split(",") if banks_param else []
#             year = request.query_params.get("year", "2023")

#             if not banks:
#                 return Response(
#                     {"error": "Please provide a list of banks to compare using the 'banks' query parameter"},
#                     status=status.HTTP_400_BAD_REQUEST
#                 )

#             data = self.bank_service.get_bank_data()
#             all_banks_data = data["Banks"].get("All Banks", {})

#             for bank in banks:
#                 if bank not in data["Banks"]:
#                     return Response(
#                         {"error": f"Bank '{bank}' not found"},
#                         status=status.HTTP_404_NOT_FOUND
#                     )

#             results = {}
#             for bank in banks:
#                 bank_data = data["Banks"][bank]
#                 results[bank] = {
#                     "basic_info": {"name": bank, "year": year},
#                     "efficiency_ratios": {},
#                     "liquidity_ratios": {},
#                     "asset_quality_ratios": {},
#                     "capital_ratios": {}
#                 }

#                 if "C. Total assets (C1 to C4 + C8 to C10)" in bank_data and year in bank_data["C. Total assets (C1 to C4 + C8 to C10)"]:
#                     results[bank]["basic_info"]["total_assets"] = bank_data["C. Total assets (C1 to C4 + C8 to C10)"][year]

#                 if "1. Markup/interest earned" in bank_data and year in bank_data["1. Markup/interest earned"]:
#                     results[bank]["basic_info"]["revenue"] = bank_data["1. Markup/interest earned"][year]

#                 calculated_ratios = self.bank_service.calculate_financial_ratios(bank_data, year)
#                 results[bank]["efficiency_ratios"] = calculated_ratios["efficiency_ratios"]
#                 results[bank]["liquidity_ratios"] = calculated_ratios["liquidity_ratios"]
#                 results[bank]["asset_quality_ratios"] = calculated_ratios["asset_quality_ratios"]
#                 results[bank]["capital_ratios"] = calculated_ratios["capital_ratios"]

#             if all_banks_data:
#                 industry_ratios = self.bank_service.calculate_financial_ratios(all_banks_data, year)
#                 results["industry_averages"] = {
#                     "basic_info": {"name": "Industry Average", "year": year},
#                     "efficiency_ratios": industry_ratios["efficiency_ratios"],
#                     "liquidity_ratios": industry_ratios["liquidity_ratios"],
#                     "asset_quality_ratios": industry_ratios["asset_quality_ratios"],
#                     "capital_ratios": industry_ratios["capital_ratios"]
#                 }

#                 if "C. Total assets (C1 to C4 + C8 to C10)" in all_banks_data and year in all_banks_data["C. Total assets (C1 to C4 + C8 to C10)"]:
#                     results["industry_averages"]["basic_info"]["total_assets"] = all_banks_data["C. Total assets (C1 to C4 + C8 to C10)"][year]

#                 if "1. Markup/interest earned" in all_banks_data and year in all_banks_data["1. Markup/interest earned"]:
#                     results["industry_averages"]["basic_info"]["revenue"] = all_banks_data["1. Markup/interest earned"][year]

#             return Response(results)

#         # Bank score endpoint
#         if 'bank_score' in request.query_params:
#             banks_param = request.query_params.get("banks", "")
#             banks = banks_param.split(",") if banks_param else []
#             year = request.query_params.get("year", "2023")

#             efficiency_weight = float(request.query_params.get("efficiency_weight", "0.60"))
#             liquidity_weight = float(request.query_params.get("liquidity_weight", "0.25"))
#             asset_quality_weight = float(request.query_params.get("asset_quality_weight", "0.15"))
#             capital_weight = float(request.query_params.get("capital_weight", "0.10"))

#             weights = {
#                 "efficiency": efficiency_weight,
#                 "liquidity": liquidity_weight,
#                 "asset_quality": asset_quality_weight,
#                 "capital": capital_weight
#             }

#             if not banks:
#                 return Response(
#                     {"error": "Please provide a list of banks to score using the 'banks' query parameter"},
#                     status=status.HTTP_400_BAD_REQUEST
#                 )

#             data = self.bank_service.get_bank_data()
#             results = {}

#             for bank in banks:
#                 if bank not in data["Banks"]:
#                     return Response(
#                         {"error": f"Bank '{bank}' not found"},
#                         status=status.HTTP_404_NOT_FOUND
#                     )

#                 bank_data = data["Banks"][bank]
#                 bank_score = self.bank_service.calculate_bank_score(bank_data, weights, year)
#                 results[bank] = bank_score

#             return Response(results)

#         # Trend analysis endpoint
#         if 'trend_analysis' in request.query_params:
#             bank = request.query_params.get("bank", "")
#             years_param = request.query_params.get("years", "2019,2020,2021,2022,2023")
#             years = years_param.split(",") if years_param else self.bank_service.get_years()

#             if not bank:
#                 return Response(
#                     {"error": "Please provide a bank to analyze using the 'bank' query parameter"},
#                     status=status.HTTP_400_BAD_REQUEST
#                 )

#             data = self.bank_service.get_bank_data()
#             if bank not in data["Banks"]:
#                 return Response(
#                     {"error": f"Bank '{bank}' not found"},
#                     status=status.HTTP_404_NOT_FOUND
#                 )

#             bank_data = data["Banks"][bank]
#             results = {
#                 "bank": bank,
#                 "years": years,
#                 "efficiency_trends": {},
#                 "liquidity_trends": {},
#                 "asset_quality_trends": {},
#                 "capital_trends": {}
#             }

#             # Calculate efficiency trends
#             if "3. Net markup/interest income" in bank_data and "1. Markup/interest earned" in bank_data:
#                 spread_ratio_trend = self.bank_service.calculate_ratio_trend(
#                     bank_data, "Spread Ratio",
#                     "3. Net markup/interest income", "1. Markup/interest earned",
#                     factor=100, years=years
#                 )
#                 results["efficiency_trends"]["spread_ratio"] = spread_ratio_trend

#             if "3. Net markup/interest income" in bank_data and "C. Total assets (C1 to C4 + C8 to C10)" in bank_data:
#                 nim_trend = self.bank_service.calculate_ratio_trend(
#                     bank_data, "Net Interest Margin",
#                     "3. Net markup/interest income", "C. Total assets (C1 to C4 + C8 to C10)",
#                     factor=100, years=years
#                 )
#                 results["efficiency_trends"]["net_interest_margin"] = nim_trend
            
#                 # Calculate trend for ROE
#             if "10. Profit/(loss) after taxation" in bank_data and "A. Total equity (A1 to A3)" in bank_data:
#                 roe_trend = BankDataService.calculate_ratio_trend(
#                     bank_data, "Return on Equity",
#                     "10. Profit/(loss) after taxation", "A. Total equity (A1 to A3)",
#                     factor=100, years=years
#                 )
#                 results["efficiency_trends"]["return_on_equity"] = roe_trend

#             # Calculate trend for ROA
#             if "10. Profit/(loss) after taxation" in bank_data and "C. Total assets (C1 to C4 + C8 to C10)" in bank_data:
#                 roa_trend = BankDataService.calculate_ratio_trend(
#                     bank_data, "Return on Assets",
#                     "10. Profit/(loss) after taxation", "C. Total assets (C1 to C4 + C8 to C10)",
#                     factor=100, years=years
#                 )
#                 results["efficiency_trends"]["return_on_assets"] = roa_trend

#             # Calculate trend for Non-Interest Income Ratio
#             if "6. Non-markup/interest income" in bank_data and "C. Total assets (C1 to C4 + C8 to C10)" in bank_data:
#                 non_interest_income_trend = BankDataService.calculate_ratio_trend(
#                     bank_data, "Non-Interest Income Ratio",
#                     "6. Non-markup/interest income", "C. Total assets (C1 to C4 + C8 to C10)",
#                     factor=100, years=years
#                 )
#                 results["efficiency_trends"]["non_interest_income_ratio"] = non_interest_income_trend

#             # Add liquidity ratios trends
#             # Cash to Total Assets trend
#             # We need to calculate this differently since it's a combined ratio
#             cash_to_assets_trend = {}
#             for year in years:
#                 try:
#                     if ("1. Cash and balances with treasury banks" in bank_data and year in bank_data[
#                         "1. Cash and balances with treasury banks"] and
#                             "2. Balances with other banks" in bank_data and year in bank_data[
#                                 "2. Balances with other banks"] and
#                             "C. Total assets (C1 to C4 + C8 to C10)" in bank_data and year in bank_data[
#                                 "C. Total assets (C1 to C4 + C8 to C10)"] and
#                             bank_data["C. Total assets (C1 to C4 + C8 to C10)"][year] > 0):
#                         cash = bank_data["1. Cash and balances with treasury banks"][year]
#                         balances = bank_data["2. Balances with other banks"][year]
#                         total_assets = bank_data["C. Total assets (C1 to C4 + C8 to C10)"][year]
#                         cash_ratio = ((cash + balances) / total_assets) * 100
#                         cash_to_assets_trend[year] = round(cash_ratio, 2)
#                     else:
#                         cash_to_assets_trend[year] = None
#                 except (KeyError, TypeError, ZeroDivisionError):
#                     cash_to_assets_trend[year] = None

#             results["liquidity_trends"]["cash_to_total_assets"] = cash_to_assets_trend

#             # Calculate other liquidity trend ratios
#             # Investments to Total Assets
#             if "4. Investments" in bank_data and "C. Total assets (C1 to C4 + C8 to C10)" in bank_data:
#                 inv_to_assets_trend = BankDataService.calculate_ratio_trend(
#                     bank_data, "Investments to Total Assets",
#                     "4. Investments", "C. Total assets (C1 to C4 + C8 to C10)",
#                     factor=100, years=years
#                 )
#                 results["liquidity_trends"]["investments_to_total_assets"] = inv_to_assets_trend

#             # Advances to Total Assets
#             if "8. Advances net of provision (C5-C7)" in bank_data and "C. Total assets (C1 to C4 + C8 to C10)" in bank_data:
#                 adv_to_assets_trend = BankDataService.calculate_ratio_trend(
#                     bank_data, "Advances to Total Assets",
#                     "8. Advances net of provision (C5-C7)", "C. Total assets (C1 to C4 + C8 to C10)",
#                     factor=100, years=years
#                 )
#                 results["liquidity_trends"]["advances_to_total_assets"] = adv_to_assets_trend

#             # Deposits to Total Assets
#             if "3. Deposits and other accounts" in bank_data and "C. Total assets (C1 to C4 + C8 to C10)" in bank_data:
#                 dep_to_assets_trend = BankDataService.calculate_ratio_trend(
#                     bank_data, "Deposits to Total Assets",
#                     "3. Deposits and other accounts", "C. Total assets (C1 to C4 + C8 to C10)",
#                     factor=100, years=years
#                 )
#                 results["liquidity_trends"]["deposits_to_total_assets"] = dep_to_assets_trend

#             # Total Liabilities to Total Assets
#             if "B. Total liabilities (B1 to B4)" in bank_data and "C. Total assets (C1 to C4 + C8 to C10)" in bank_data:
#                 liab_to_assets_trend = BankDataService.calculate_ratio_trend(
#                     bank_data, "Total Liabilities to Total Assets",
#                     "B. Total liabilities (B1 to B4)", "C. Total assets (C1 to C4 + C8 to C10)",
#                     factor=100, years=years
#                 )
#                 results["liquidity_trends"]["liabilities_to_total_assets"] = liab_to_assets_trend

#             # Advances to Deposits
#             if "8. Advances net of provision (C5-C7)" in bank_data and "3. Deposits and other accounts" in bank_data:
#                 adv_to_dep_trend = BankDataService.calculate_ratio_trend(
#                     bank_data, "Advances to Deposits",
#                     "8. Advances net of provision (C5-C7)", "3. Deposits and other accounts",
#                     factor=100, years=years
#                 )
#                 results["liquidity_trends"]["advances_to_deposits"] = adv_to_dep_trend

#             # Gross Advances to Deposits
#             if "5. Gross advances" in bank_data and "3. Deposits and other accounts" in bank_data:
#                 gross_adv_to_dep_trend = BankDataService.calculate_ratio_trend(
#                     bank_data, "Gross Advances to Deposits",
#                     "5. Gross advances", "3. Deposits and other accounts",
#                     factor=100, years=years
#                 )
#                 results["liquidity_trends"]["gross_advances_to_deposits"] = gross_adv_to_dep_trend

#             # Calculate asset quality trend ratios
#             # NPL to Gross Advances
#             if "6. Advances-non-performing/classified" in bank_data and "5. Gross advances" in bank_data:
#                 npl_to_adv_trend = BankDataService.calculate_ratio_trend(
#                     bank_data, "NPL to Gross Advances",
#                     "6. Advances-non-performing/classified", "5. Gross advances",
#                     factor=100, years=years
#                 )
#                 results["asset_quality_trends"]["npl_to_gross_advances"] = npl_to_adv_trend

#             # Provisions against NPLs to Gross Advances
#             if "7. Provision against advances" in bank_data and "5. Gross advances" in bank_data:
#                 prov_to_adv_trend = BankDataService.calculate_ratio_trend(
#                     bank_data, "Provisions against NPLs to Gross Advances",
#                     "7. Provision against advances", "5. Gross advances",
#                     factor=100, years=years
#                 )
#                 results["asset_quality_trends"]["provisions_to_gross_advances"] = prov_to_adv_trend

#             # Provision Coverage
#             if "7. Provision against advances" in bank_data and "6. Advances-non-performing/classified" in bank_data:
#                 prov_coverage_trend = BankDataService.calculate_ratio_trend(
#                     bank_data, "Provision Coverage",
#                     "7. Provision against advances", "6. Advances-non-performing/classified",
#                     factor=100, years=years
#                 )
#                 results["asset_quality_trends"]["provision_coverage"] = prov_coverage_trend

#             # NPL to Equity
#             if "6. Advances-non-performing/classified" in bank_data and "A. Total equity (A1 to A3)" in bank_data:
#                 npl_to_equity_trend = BankDataService.calculate_ratio_trend(
#                     bank_data, "NPL to Equity",
#                     "6. Advances-non-performing/classified", "A. Total equity (A1 to A3)",
#                     factor=100, years=years
#                 )
#                 results["asset_quality_trends"]["npl_to_equity"] = npl_to_equity_trend

#             # Calculate capital trend ratios
#             # Capital to Assets
#             if "A. Total equity (A1 to A3)" in bank_data and "C. Total assets (C1 to C4 + C8 to C10)" in bank_data:
#                 capital_ratio_trend = BankDataService.calculate_ratio_trend(
#                     bank_data, "Capital to Assets",
#                     "A. Total equity (A1 to A3)", "C. Total assets (C1 to C4 + C8 to C10)",
#                     factor=100, years=years
#                 )
#                 results["capital_trends"]["capital_to_assets"] = capital_ratio_trend

#             # Deposits to Equity
#             if "3. Deposits and other accounts" in bank_data and "A. Total equity (A1 to A3)" in bank_data:
#                 dep_to_equity_trend = BankDataService.calculate_ratio_trend(
#                     bank_data, "Deposits to Equity",
#                     "3. Deposits and other accounts", "A. Total equity (A1 to A3)",
#                     factor=1, years=years  # No percentage for this ratio
#                 )
#                 results["capital_trends"]["deposits_to_equity"] = dep_to_equity_trend
                

#             return Response(results)

#         return Response(
#             {"error": "No valid endpoint specified in query parameters"},
#             status=status.HTTP_400_BAD_REQUEST
#         )

#     def post(self, request):
#         """
#         Handle POST requests for endpoints that need request body data.
#         """
#         # Bank comparison endpoint
#         if 'bank_comparison' in request.data:
#             serializer = BankComparisonSerializer(data=request.data)
#             if not serializer.is_valid():
#                 return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#             banks = serializer.validated_data["banks"]
#             metrics = serializer.validated_data["metrics"]
#             year = serializer.validated_data["year"]

#             data = self.bank_service.get_bank_data()
#             result = {}

#             for bank in banks:
#                 if bank not in data["Banks"]:
#                     return Response(
#                         {"error": f"Bank '{bank}' not found"},
#                         status=status.HTTP_404_NOT_FOUND
#                     )

#                 bank_data = data["Banks"][bank]
#                 result[bank] = {}

#                 for metric in metrics:
#                     if metric in bank_data and year in bank_data[metric]:
#                         result[bank][metric] = bank_data[metric][year]
#                     else:
#                         result[bank][metric] = None

#             return Response(result)

#         # Comparative analysis endpoint (POST version)
#         if 'comparative_analysis' in request.data:
#             banks = request.data.get("banks", [])
#             year = request.data.get("year", "2023")

#             if not banks or not isinstance(banks, list):
#                 return Response(
#                     {"error": "Please provide a list of banks to compare"},
#                     status=status.HTTP_400_BAD_REQUEST
#                 )

#             mock_request = request._request
#             mock_request.GET = {
#                 "banks": ",".join(banks),
#                 "year": year,
#                 "comparative_analysis": "true"
#             }
#             return self.get(mock_request)

#         # Bank score endpoint (POST version)
#         if 'bank_score' in request.data:
#             banks = request.data.get("banks", [])
#             year = request.data.get("year", "2023")
#             weights = request.data.get("weights", {
#                 "efficiency": 0.60,
#                 "liquidity": 0.25,
#                 "asset_quality": 0.15,
#                 "capital": 0.10
#             })

#             if not banks or not isinstance(banks, list):
#                 return Response(
#                     {"error": "Please provide a list of banks to score"},
#                     status=status.HTTP_400_BAD_REQUEST
#                 )

#             mock_request = request._request
#             mock_request.GET = {
#                 "banks": ",".join(banks),
#                 "year": year,
#                 "bank_score": "true"
#             }
#             mock_request.GET.update({
#                 f"{k}_weight": str(v) for k, v in weights.items()
#             })
#             return self.get(mock_request)

#         # Trend analysis endpoint (POST version)
#         if 'trend_analysis' in request.data:
#             bank = request.data.get("bank", "")
#             years = request.data.get("years", ["2019", "2020", "2021", "2022", "2023"])

#             if not bank:
#                 return Response(
#                     {"error": "Please provide a bank to analyze"},
#                     status=status.HTTP_400_BAD_REQUEST
#                 )

#             mock_request = request._request
#             mock_request.GET = {
#                 "bank": bank,
#                 "years": ",".join(years) if isinstance(years, list) else years,
#                 "trend_analysis": "true"
#             }
#             return self.get(mock_request)

#         return Response(
#             {"error": "No valid endpoint specified in request data"},
#             status=status.HTTP_400_BAD_REQUEST
#         )



































from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .services.bank_services import BankDataService
from .services.company_services import CompanyDataService
from .serializers import BankComparisonSerializer, CompanyComparisonSerializer, CompanyScoreSerializer
import pandas as pd

class CreditRiskAPIView(APIView):
    """
    Consolidated API endpoint for all financial operations (banks and companies).
    Similar structure to AltmanZScoreView where endpoints are determined by query parameters.
    """
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.bank_service = BankDataService()
        self.company_service = CompanyDataService()

    def get(self, request):
        """
        Handle all GET requests based on query parameters.
        """
        # Extract common parameters
        entity_name = request.query_params.get('entity_name') or request.query_params.get('bank_name') or request.query_params.get('company_name')
        entity_type = 'bank' if 'bank_name' in request.query_params or 'banks' in request.query_params else 'company'
        sector = request.query_params.get('sector')
        sub_sector = request.query_params.get('sub_sector')
        indicator = request.query_params.get('indicator')
        metric = request.query_params.get('metric')
        year = request.query_params.get('year', '2023' if entity_type == 'bank' else '2022')
        years_param = request.query_params.get('years', '')
        years = years_param.split(',') if years_param else (self.bank_service.get_years() if entity_type == 'bank' else self.company_service.get_company_years())
        
        # Entity listing endpoints
        if 'listed_banks' in request.query_params:
            banks = self.bank_service.get_listed_banks()
            return Response({"banks": banks})
            
        if 'listed_companies' in request.query_params:
            companies = self.company_service.get_listed_companies()
            return Response({"companies": companies})

        # Entity detail endpoint
        if entity_name:
            if entity_type == 'bank':
                data = self.bank_service.get_bank_data()
                if entity_name not in data["Banks"]:
                    return Response({"error": f"Bank '{entity_name}' not found"}, status=status.HTTP_404_NOT_FOUND)
                return Response(data["Banks"][entity_name])
            else:
                data = self.company_service.get_company_data()
                if entity_name not in data["Companies"]:
                    return Response({"error": f"Company '{entity_name}' not found"}, status=status.HTTP_404_NOT_FOUND)
                return Response(data["Companies"][entity_name])

        # Ranking endpoint
        if 'ranking' in request.query_params:
            if entity_type == 'bank':
                metric = metric or "Assets"
                data = self.bank_service.get_bank_data()
                rankings = []
                for bank_name, bank_data in data["Banks"].items():
                    if bank_name != "All Banks" and metric in bank_data and year in bank_data[metric]:
                        rankings.append({"entity": bank_name, "value": bank_data[metric][year]})
            else:
                indicator = indicator or "F. Operations: - 1. Sales"
                data = self.company_service.get_company_data()
                rankings = []
                for comp_name, comp_data in data["Companies"].items():
                    if "average" not in comp_name.lower() and "all" not in comp_name.lower():
                        comp_indicators = comp_data.get("Indicators", {})
                        if indicator in comp_indicators and year in comp_indicators[indicator]:
                            rankings.append({
                                "entity": comp_name,
                                "sector": comp_data.get("Sector", ""),
                                "sub_sector": comp_data.get("Sub-Sector", ""),
                                "value": comp_indicators[indicator][year]
                            })

            rankings.sort(key=lambda x: x["value"], reverse=True)
            for i, item in enumerate(rankings):
                item["rank"] = i + 1
            return Response(rankings)

        # Financial analysis endpoint
        if 'financial_analysis' in request.query_params and entity_name:
            if entity_type == 'bank':
                data = self.bank_service.get_bank_data()
                if entity_name not in data["Banks"]:
                    return Response({"error": f"Bank '{entity_name}' not found"}, status=status.HTTP_404_NOT_FOUND)
                
                entity_data = data["Banks"][entity_name]
                all_entities_data = data["Banks"]["All Banks"]
                analysis = {
                    "entity_name": entity_name,
                    "entity_type": "bank",
                    "year": year,
                    "metrics": {},
                    "ratios": {},
                    "growth": {},
                    "industry_comparison": {}
                }
                
                # Bank-specific metrics
                for m in ["Assets", "Revenue", "A. Total equity (A1 to A3)"]:
                    if m in entity_data and year in entity_data[m]:
                        analysis["metrics"][m.lower()] = entity_data[m][year]
                        if f"{year-1}" in entity_data[m]:
                            growth = ((entity_data[m][year] - entity_data[m][str(int(year)-1)]) / entity_data[m][str(int(year)-1)]) * 100
                            analysis["growth"][f"{m.lower()}_growth"] = round(growth, 2)
                
                if "Assets" in entity_data and year in entity_data["Assets"] and "Assets" in all_entities_data and year in all_entities_data["Assets"]:
                    analysis["industry_comparison"]["asset_market_share"] = round((entity_data["Assets"][year] / all_entities_data["Assets"][year]) * 100, 2)
                
                # Calculate bank ratios
                calculated_ratios = self.bank_service.calculate_financial_ratios(entity_data, year)
                for ratio_category in calculated_ratios:
                    analysis["ratios"][ratio_category] = calculated_ratios[ratio_category]
            else:
                data = self.company_service.get_company_data()
                if entity_name not in data["Companies"]:
                    return Response({"error": f"Company '{entity_name}' not found"}, status=status.HTTP_404_NOT_FOUND)
                
                entity_data = data["Companies"][entity_name]
                indicators = entity_data.get("Indicators", {})
                
                # Find industry data
                industry_data = None
                for name, info in data["Companies"].items():
                    if "industry average" in name.lower():
                        if info.get("Sub-Sector") == entity_data.get("Sub-Sector"):
                            industry_data = info
                            break
                        elif info.get("Sector") == entity_data.get("Sector"):
                            industry_data = info
                
                analysis = {
                    "entity_name": entity_name,
                    "entity_type": "company",
                    "sector": entity_data.get("Sector"),
                    "sub_sector": entity_data.get("Sub-Sector"),
                    "year": year,
                    "metrics": {},
                    "ratios": {},
                    "growth": {},
                    "industry_comparison": {}
                }
                
                # Company-specific metrics
                key_metrics = [
                    "F. Operations: - 1. Sales",
                    "Total Assets (A+B) / Equity & Liabilities (C+D+E)",
                    "C. Shareholders' Equity (C1+C2+C3)",
                    "F. Operations: - 10. Profit / (loss) after tax (F8-F9)"
                ]
                
                for metric in key_metrics:
                    if metric in indicators and year in indicators[metric]:
                        readable_name = metric.split(" - ")[-1].split(" (")[0]
                        analysis["metrics"][readable_name.lower().replace(" ", "_").replace("/", "_")] = indicators[metric][year]
                        prev_year = str(int(year)-1)
                        if prev_year in indicators[metric] and indicators[metric][prev_year] != 0:
                            growth = ((indicators[metric][year] - indicators[metric][prev_year]) / indicators[metric][prev_year]) * 100
                            analysis["growth"][f"{readable_name.lower().replace(' ', '_').replace('/', '_')}_growth"] = round(growth, 2)
                
                # Calculate company ratios
                analysis["ratios"] = self.company_service.calculate_company_financial_ratios(entity_data, year)
                
                # Industry comparison
                if industry_data:
                    industry_indicators = industry_data.get("Indicators", {})
                    for metric in key_metrics:
                        if (metric in indicators and year in indicators[metric] and
                            metric in industry_indicators and year in industry_indicators[metric] and
                            industry_indicators[metric][year] != 0):
                            readable_name = metric.split(" - ")[-1].split(" (")[0]
                            share = (indicators[metric][year] / industry_indicators[metric][year]) * 100
                            analysis["industry_comparison"][f"{readable_name.lower().replace(' ', '_').replace('/', '_')}_vs_industry"] = round(share, 2)
            
            return Response(analysis)

        # Sector/sub-sector endpoints
        if 'sectors' in request.query_params:
            sectors = self.bank_service.get_sectors() if entity_type == 'bank' else self.company_service.get_company_sectors()
            return Response({"sectors": sectors, "entity_type": entity_type})

        if 'sub_sectors' in request.query_params:
            if not sector:
                return Response({"error": "Sector parameter is required"}, status=status.HTTP_400_BAD_REQUEST)
            sub_sectors = self.bank_service.get_sub_sectors(sector) if entity_type == 'bank' else self.company_service.get_company_sub_sectors(sector)
            return Response({"sub_sectors": sub_sectors, "entity_type": entity_type})

        if 'entities_by_sub_sector' in request.query_params:
            if not sub_sector:
                return Response({"error": "Sub-sector parameter is required"}, status=status.HTTP_400_BAD_REQUEST)
            entities = self.bank_service.get_banks_by_sub_sector(sub_sector) if entity_type == 'bank' else self.company_service.get_companies_by_sub_sector(sub_sector)
            return Response({"entities": entities, "entity_type": entity_type})

        # Indicators/metrics endpoints
        if 'indicators' in request.query_params or 'metrics' in request.query_params:
            if entity_type == 'bank':
                metrics = self.bank_service.get_metrics()
                return Response({"metrics": metrics, "entity_type": "bank"})
            else:
                indicators = self.company_service.get_company_indicators()
                return Response({"indicators": indicators, "entity_type": "company"})

        if 'sub_indicators' in request.query_params:
            if not indicator:
                return Response({"error": "Indicator parameter is required"}, status=status.HTTP_400_BAD_REQUEST)
            sub_indicators = self.company_service.get_company_sub_indicators(indicator)
            return Response({"sub_indicators": sub_indicators, "entity_type": "company"})

        # Years endpoint
        if 'years' in request.query_params:
            years = self.bank_service.get_years() if entity_type == 'bank' else self.company_service.get_company_years()
            return Response({"years": years, "entity_type": entity_type})

        # Comparative analysis endpoint
        if 'comparative_analysis' in request.query_params:
            entities_param = request.query_params.get("entities") or request.query_params.get("banks") or request.query_params.get("companies")
            entities = entities_param.split(",") if entities_param else []

            if not entities:
                return Response({"error": "Please provide a list of entities to compare"}, status=status.HTTP_400_BAD_REQUEST)

            if entity_type == 'bank':
                data = self.bank_service.get_bank_data()
                all_entities_data = data["Banks"].get("All Banks", {})
                results = {}
                
                for entity in entities:
                    if entity not in data["Banks"]:
                        return Response({"error": f"Bank '{entity}' not found"}, status=status.HTTP_404_NOT_FOUND)
                    
                    entity_data = data["Banks"][entity]
                    results[entity] = {
                        "basic_info": {"name": entity, "year": year},
                        "efficiency_ratios": {},
                        "liquidity_ratios": {},
                        "asset_quality_ratios": {},
                        "capital_ratios": {}
                    }

                    if "C. Total assets (C1 to C4 + C8 to C10)" in entity_data and year in entity_data["C. Total assets (C1 to C4 + C8 to C10)"]:
                        results[entity]["basic_info"]["total_assets"] = entity_data["C. Total assets (C1 to C4 + C8 to C10)"][year]

                    if "1. Markup/interest earned" in entity_data and year in entity_data["1. Markup/interest earned"]:
                        results[entity]["basic_info"]["revenue"] = entity_data["1. Markup/interest earned"][year]

                    calculated_ratios = self.bank_service.calculate_financial_ratios(entity_data, year)
                    results[entity]["efficiency_ratios"] = calculated_ratios.get("efficiency_ratios", {})
                    results[entity]["liquidity_ratios"] = calculated_ratios.get("liquidity_ratios", {})
                    results[entity]["asset_quality_ratios"] = calculated_ratios.get("asset_quality_ratios", {})
                    results[entity]["capital_ratios"] = calculated_ratios.get("capital_ratios", {})

                if all_entities_data:
                    industry_ratios = self.bank_service.calculate_financial_ratios(all_entities_data, year)
                    results["Industry Average"] = {
                        "basic_info": {"name": "Industry Average", "year": year},
                        "efficiency_ratios": industry_ratios.get("efficiency_ratios", {}),
                        "liquidity_ratios": industry_ratios.get("liquidity_ratios", {}),
                        "asset_quality_ratios": industry_ratios.get("asset_quality_ratios", {}),
                        "capital_ratios": industry_ratios.get("capital_ratios", {})
                    }
            else:
                data = self.company_service.get_company_data()
                results = {}
                
                for entity in entities:
                    if entity not in data["Companies"]:
                        return Response({"error": f"Company '{entity}' not found"}, status=status.HTTP_404_NOT_FOUND)
                    
                    entity_data = data["Companies"][entity]
                    results[entity] = {
                        "basic_info": {
                            "name": entity,
                            "sector": entity_data.get("Sector"),
                            "sub_sector": entity_data.get("Sub-Sector"),
                            "year": year
                        },
                        "profitability_ratios": {},
                        "liquidity_ratios": {},
                        "efficiency_ratios": {},
                        "solvency_ratios": {},
                        "cash_flow_ratios": {},
                        "valuation_ratios": {}
                    }

                    indicators = entity_data.get("Indicators", {})
                    if "Total Assets (A+B) / Equity & Liabilities (C+D+E)" in indicators:
                        results[entity]["basic_info"]["total_assets"] = indicators["Total Assets (A+B) / Equity & Liabilities (C+D+E)"].get(year)
                    if "F. Operations: - 1. Sales" in indicators:
                        results[entity]["basic_info"]["revenue"] = indicators["F. Operations: - 1. Sales"].get(year)

                    calculated_ratios = self.company_service.calculate_company_financial_ratios(entity_data, year)
                    for ratio_type in calculated_ratios:
                        results[entity][f"{ratio_type}_ratios"] = calculated_ratios[ratio_type]

                # Add industry average if available
                industry_data = None
                if entities:
                    first_entity = data["Companies"][entities[0]]
                    for name, info in data["Companies"].items():
                        if "industry average" in name.lower():
                            if info.get("Sub-Sector") == first_entity.get("Sub-Sector"):
                                industry_data = info
                                break
                            elif info.get("Sector") == first_entity.get("Sector"):
                                industry_data = info

                if industry_data:
                    industry_ratios = self.company_service.calculate_company_financial_ratios(industry_data, year)
                    results["Industry Average"] = {
                        "basic_info": {
                            "name": "Industry Average",
                            "sector": industry_data.get("Sector"),
                            "sub_sector": industry_data.get("Sub-Sector"),
                            "year": year
                        }
                    }
                    for ratio_type in industry_ratios:
                        results["Industry Average"][f"{ratio_type}_ratios"] = industry_ratios[ratio_type]

            return Response(results)

        # Entity score endpoint
        if 'entity_score' in request.query_params or 'bank_score' in request.query_params or 'company_score' in request.query_params:
            entities_param = request.query_params.get("entities") or request.query_params.get("banks") or request.query_params.get("companies")
            entities = entities_param.split(",") if entities_param else []

            if entity_type == 'bank':
                weights = {
                    "efficiency": float(request.query_params.get("efficiency_weight", "0.60")),
                    "liquidity": float(request.query_params.get("liquidity_weight", "0.25")),
                    "asset_quality": float(request.query_params.get("asset_quality_weight", "0.15")),
                    "capital": float(request.query_params.get("capital_weight", "0.10"))
                }
            else:
                weights = {
                    "profitability": float(request.query_params.get("profitability_weight", "0.50")),
                    "liquidity": float(request.query_params.get("liquidity_weight", "0.25")),
                    "activity": float(request.query_params.get("activity_weight", "0.15")),
                    "solvency": float(request.query_params.get("solvency_weight", "0.10"))
                }

            if not entities:
                return Response({"error": "Please provide a list of entities to score"}, 
                              status=status.HTTP_400_BAD_REQUEST)

            if entity_type == 'bank':
                data = self.bank_service.get_bank_data()
                results = {}
                for entity in entities:
                    if entity not in data["Banks"]:
                        return Response({"error": f"Bank '{entity}' not found"}, 
                                      status=status.HTTP_404_NOT_FOUND)
                    entity_data = data["Banks"][entity]
                    results[entity] = self.bank_service.calculate_bank_score(entity_data, weights, year)
            else:
                data = self.company_service.get_company_data()
                results = {}
                for entity in entities:
                    if entity not in data["Companies"]:
                        return Response({"error": f"Company '{entity}' not found"}, 
                                      status=status.HTTP_404_NOT_FOUND)
                    entity_data = data["Companies"][entity]
                    results[entity] = self.company_service.calculate_company_score(entity_data, weights, year)

            return Response(results)

        # Trend analysis endpoint
        if 'trend_analysis' in request.query_params:
            entity = entity_name or request.query_params.get("bank") or request.query_params.get("company")
            if not entity:
                return Response({"error": "Please provide an entity to analyze"}, 
                              status=status.HTTP_400_BAD_REQUEST)

            if entity_type == 'bank':
                data = self.bank_service.get_bank_data()
                if entity not in data["Banks"]:
                    return Response({"error": f"Bank '{entity}' not found"}, 
                                  status=status.HTTP_404_NOT_FOUND)
                
                entity_data = data["Banks"][entity]
                results = {
                    "entity": entity,
                    "entity_type": "bank",
                    "years": years,
                    "efficiency_trends": {},
                    "liquidity_trends": {},
                    "asset_quality_trends": {},
                    "capital_trends": {}
                }
                
                # Calculate bank trend ratios
                if "3. Net markup/interest income" in entity_data and "1. Markup/interest earned" in entity_data:
                    spread_ratio = self.bank_service.calculate_ratio_trend(
                        entity_data, "Spread Ratio",
                        "3. Net markup/interest income", "1. Markup/interest earned",
                        factor=100, years=years
                    )
                    results["efficiency_trends"]["spread_ratio"] = spread_ratio
                
                if "3. Net markup/interest income" in bank_data and "C. Total assets (C1 to C4 + C8 to C10)" in bank_data:
                    nim_trend = self.bank_service.calculate_ratio_trend(
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
                    

                # return Response(results)

            
                
            else:
                data = self.company_service.get_company_data()
                if entity not in data["Companies"]:
                    return Response({"error": f"Company '{entity}' not found"}, 
                                  status=status.HTTP_404_NOT_FOUND)
                
                entity_data = data["Companies"][entity]
                indicators = entity_data.get("Indicators", {})
                results = {
                    "entity": entity,
                    "entity_type": "company",
                    "sector": entity_data.get("Sector"),
                    "sub_sector": entity_data.get("Sub-Sector"),
                    "years": years,
                    "profitability_trends": {},
                    "liquidity_trends": {},
                    "efficiency_trends": {},
                    "solvency_trends": {},
                    "cash_flow_trends": {}
                }
                
                # First check for pre-calculated ratios
                kpi_prefixes = {
                    "I. Key Performance Indicators - Profitability Ratios": "profitability_trends",
                    "I. Key Performance Indicators - Liquidity Ratios": "liquidity_trends",
                    "I. Key Performance Indicators - Activity Ratios": "efficiency_trends",
                    "I. Key Performance Indicators - Solvency Ratios": "solvency_trends",
                    "I. Key Performance Indicators - Cash Flow Ratios": "cash_flow_trends"
                }
                
                for kpi_prefix, trend_key in kpi_prefixes.items():
                    for indicator_key in indicators:
                        if indicator_key.startswith(kpi_prefix):
                            ratio_name = indicator_key.replace(kpi_prefix + " - ", "").lower().replace(" ", "_")
                            ratio_trend = {yr: indicators[indicator_key].get(yr) for yr in years}
                            results[trend_key][ratio_name] = ratio_trend
                
                # If no pre-calculated ratios found, calculate them
                if not any(results[trend_key] for trend_key in results if trend_key.endswith('_trends')):
                    # Calculate profitability trends
                    results["profitability_trends"]["return_on_equity"] = self.company_service.calculate_company_ratio_trend(
                        entity_data, "Return on Equity", "NET_PROFIT", "TOTAL_EQUITY", 100, years
                    )
                    results["profitability_trends"]["return_on_assets"] = self.company_service.calculate_company_ratio_trend(
                        entity_data, "Return on Assets", "NET_PROFIT", "TOTAL_ASSETS", 100, years
                    )
                    results["profitability_trends"]["net_profit_margin"] = self.company_service.calculate_company_ratio_trend(
                        entity_data, "Net Profit Margin", "NET_PROFIT", "SALES", 100, years
                    )

                    # Calculate liquidity trends
                    results["liquidity_trends"]["current_ratio"] = self.company_service.calculate_company_ratio_trend(
                        entity_data, "Current Ratio", "TOTAL_CURRENT_ASSETS", "TOTAL_CURRENT_LIABILITIES", 1, years
                    )

                    # Calculate efficiency trends
                    results["efficiency_trends"]["asset_turnover"] = self.company_service.calculate_company_ratio_trend(
                        entity_data, "Asset Turnover", "SALES", "TOTAL_ASSETS", 1, years
                    )

                    # Calculate solvency trends
                    results["solvency_trends"]["debt_to_equity"] = self.company_service.calculate_company_ratio_trend(
                        entity_data, "Debt to Equity", "TOTAL_LIABILITIES", "TOTAL_EQUITY", 1, years
                    )
            
            return Response(results)

        return Response(
            {"error": "No valid endpoint specified in query parameters"},
            status=status.HTTP_400_BAD_REQUEST
        )

    def post(self, request):
        """
        Handle POST requests for endpoints that need request body data.
        """
        # Entity comparison endpoint
        if 'entity_comparison' in request.data or 'bank_comparison' in request.data or 'company_comparison' in request.data:
            entity_type = 'bank' if 'bank_comparison' in request.data else 'company'
            
            if entity_type == 'bank':
                serializer = BankComparisonSerializer(data=request.data)
            else:
                serializer = CompanyComparisonSerializer(data=request.data)
                
            if not serializer.is_valid():
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

            entities = serializer.validated_data["entities"] if 'entities' in serializer.validated_data else (
                serializer.validated_data["banks"] if entity_type == 'bank' else serializer.validated_data["companies"]
            )
            metrics = serializer.validated_data.get("metrics", [])
            indicators = serializer.validated_data.get("indicators", [])
            year = serializer.validated_data["year"]

            if entity_type == 'bank':
                data = self.bank_service.get_bank_data()
                result = {}
                for entity in entities:
                    if entity not in data["Banks"]:
                        return Response({"error": f"Bank '{entity}' not found"}, 
                                      status=status.HTTP_404_NOT_FOUND)
                    entity_data = data["Banks"][entity]
                    result[entity] = {}
                    for metric in metrics:
                        if metric in entity_data and year in entity_data[metric]:
                            result[entity][metric] = entity_data[metric][year]
                        else:
                            result[entity][metric] = None
            else:
                comparison_data = self.company_service.get_company_comparison_data(entities, indicators, year)
                return Response(comparison_data)

            return Response(result)

        # Comparative analysis endpoint (POST version)
        if 'comparative_analysis' in request.data:
            entities = request.data.get("entities") or request.data.get("banks") or request.data.get("companies", [])
            year = request.data.get("year", "2023")
            entity_type = 'bank' if 'banks' in request.data else 'company'

            if not entities or not isinstance(entities, list):
                return Response(
                    {"error": "Please provide a list of entities to compare"},
                    status=status.HTTP_400_BAD_REQUEST
                )

            mock_request = request._request
            mock_request.GET = {
                "entities": ",".join(entities),
                "year": year,
                "comparative_analysis": "true"
            }
            if entity_type == 'bank':
                mock_request.GET["banks"] = ",".join(entities)
            else:
                mock_request.GET["companies"] = ",".join(entities)
                
            return self.get(mock_request)

        # Entity score endpoint (POST version)
        if 'entity_score' in request.data or 'bank_score' in request.data or 'company_score' in request.data:
            entity_type = 'bank' if 'bank_score' in request.data else 'company'
            
            if entity_type == 'company':
                serializer = CompanyScoreSerializer(data=request.data)
                if not serializer.is_valid():
                    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

                entities = serializer.validated_data["companies"]
                year = serializer.validated_data["year"]
                weights = serializer.validated_data["weights"]
            else:
                entities = request.data.get("banks", [])
                year = request.data.get("year", "2023")
                weights = request.data.get("weights", {
                    "efficiency": 0.60,
                    "liquidity": 0.25,
                    "asset_quality": 0.15,
                    "capital": 0.10
                })

            if not entities or not isinstance(entities, list):
                return Response(
                    {"error": "Please provide a list of entities to score"},
                    status=status.HTTP_400_BAD_REQUEST
                )

            mock_request = request._request
            mock_request.GET = {
                "entities": ",".join(entities),
                "year": year,
                "entity_score": "true"
            }
            if entity_type == 'bank':
                mock_request.GET["banks"] = ",".join(entities)
                mock_request.GET["bank_score"] = "true"
                mock_request.GET.update({
                    f"{k}_weight": str(v) for k, v in weights.items()
                })
            else:
                mock_request.GET["companies"] = ",".join(entities)
                mock_request.GET["company_score"] = "true"
                mock_request.GET.update({
                    f"{k}_weight": str(v) for k, v in weights.items()
                })
                
            return self.get(mock_request)

        # Trend analysis endpoint (POST version)
        if 'trend_analysis' in request.data:
            entity = request.data.get("entity") or request.data.get("bank") or request.data.get("company", "")
            years = request.data.get("years", ["2019", "2020", "2021", "2022", "2023"])
            entity_type = 'bank' if 'bank' in request.data else 'company'

            if not entity:
                return Response(
                    {"error": "Please provide an entity to analyze"},
                    status=status.HTTP_400_BAD_REQUEST
                )

            mock_request = request._request
            mock_request.GET = {
                "entity": entity,
                "years": ",".join(years) if isinstance(years, list) else years,
                "trend_analysis": "true"
            }
            if entity_type == 'bank':
                mock_request.GET["bank"] = entity
            else:
                mock_request.GET["company"] = entity
                
            return self.get(mock_request)

        return Response(
            {"error": "No valid endpoint specified in request data"},
            status=status.HTTP_400_BAD_REQUEST
        )