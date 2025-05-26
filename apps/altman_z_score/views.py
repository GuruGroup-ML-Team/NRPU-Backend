        
import pandas as pd
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import logging

logger = logging.getLogger(__name__)

class AltmanZScoreView(APIView):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        try:
            self.df_pivot = pd.read_excel("Data/input_data.xlsx")
            self.df_sector_avg = pd.read_excel("Data/altman_sector_averages.xlsx")
            logger.info("Datasets loaded successfully.")
        except Exception as e:
            logger.error(f"Error loading datasets: {str(e)}", exc_info=True)
            self.df_pivot = pd.DataFrame()
            self.df_sector_avg = pd.DataFrame()

    def calculate_altman_score(self, df_filtered):
        logger.debug("Inside calculate_altman_score method")

        zscore_components = {
            '1. Capital work in progress': ('Sub Indicator', 'wc'),
            'Total Assets (A+B) / Equity & Liabilities (C+D+E)': ('Sub Indicator', 'ta'),
            'of which: un-appropriated profit(loss) / retained earnings': ('Sub-Sub Indicator', 're'),
            '6. EBIT (F3-F4+F5)': ('Sub Indicator', 'ebit'),
            "C. Shareholders' Equity (C1+C2+C3)": ('Indicator', 'mve'),
            'D. Non-Current Liabilities (D1+D2+D3+D4+D5)': ('Indicator', 'tl_d'),
            'E. Current Liabilities (E1+E2+E3+E4)': ('Indicator', 'tl_e')
        }
        A_COEF = 6.56
        B_COEF = 3.26
        C_COEF = 6.72
        D_COEF = 1.05
        INTERCEPT = 3.25

        year_columns = []
        for col in df_filtered.columns:
            if str(col).isdigit():
                year_columns.append(str(col))
            elif isinstance(col, str) and col.startswith('AltmanZscore '):
                year_value = col.split(' ')[1]
                if year_value.isdigit():
                    year_columns.append(year_value)
        year_columns = sorted(list(set(year_columns)))

        altman_scores = {}

        for year in year_columns:
            components = {key: None for _, key in zscore_components.values()}

            for col_name, (category, key) in zscore_components.items():
                row = df_filtered[
                    (df_filtered['Indicator'].str.strip().str.lower() == col_name.lower()) |
                    (df_filtered['Sub Indicator'].str.strip().str.lower() == col_name.lower()) |
                    (df_filtered['Sub-Sub Indicator'].str.strip().str.lower() == col_name.lower())
                ]
                if not row.empty:
                    if year in row.columns and pd.notna(row.iloc[0][year]):
                        components[key] = row.iloc[0][year]
                    elif f"AltmanZscore {year}" in row.columns and pd.notna(row.iloc[0][f"AltmanZscore {year}"]):
                        components[key] = row.iloc[0][f"AltmanZscore {year}"]

            if not all(k in components and components[k] is not None for k in ['ta']):
                altman_scores[year] = "Insufficient data (missing TA)"
                continue
            if components['ta'] == 0:
                altman_scores[year] = "Total Assets (TA) is zero, cannot calculate Z-score."
                continue

            try:
                wc = components.get('wc', 0) or 0
                re = components.get('re', 0) or 0
                ebit = components.get('ebit', 0) or 0
                mve = components.get('mve', 0) or 0
                tl_d = components.get('tl_d', 0) or 0
                tl_e = components.get('tl_e', 0) or 0

                tl = tl_d + tl_e

                x1 = wc / components['ta']
                x2 = re / components['ta']
                x3 = ebit / components['ta']

                x4 = 0
                if mve is not None and tl > 0:
                    x4 = mve / tl
                elif mve is not None and tl == 0:
                    altman_scores[year] = "Total Liabilities (TL) is zero, cannot calculate X4."
                    continue

                altman_zscore = INTERCEPT + (A_COEF * x1) + (B_COEF * x2) + (C_COEF * x3) + (D_COEF * x4)
                altman_scores[year] = altman_zscore
            except Exception as e:
                logger.error(f"Error in calculating Altman Z-Score for year {year}: {str(e)}", exc_info=True)
                altman_scores[year] = f"Error: {str(e)}"

        return altman_scores

    def replace_nan(self, data):
        if isinstance(data, dict):
            return {k: self.replace_nan(v) for k, v in data.items()}
        elif isinstance(data, list):
            return [self.replace_nan(item) for item in data]
        elif pd.isna(data):
            return None
        else:
            return data

    def get_sector_averages(self, sector, year):
        # This method is for pre-calculated averages from df_sector_avg.
        # The new use case will calculate from df_pivot.
        try:
            if sector and sector.lower() != "all":
                averages_df = self.df_sector_avg[self.df_sector_avg['Sector'].str.lower() == sector.lower()]
            else:
                averages_df = self.df_sector_avg

            if averages_df.empty:
                logger.warning(f"No data found for sector: {sector} in altman_sector_averages.xlsx")
                return {"error": f"No data found for sector: {sector}"}

            if year and year.lower() != "all":
                year_column = f"AltmanZscore {year}"
                if year_column not in averages_df.columns:
                    return {"error": f"Year {year} is not available in the dataset."}
                averages_df = averages_df[averages_df['Org Name'].str.contains('Average', case=False, na=False)][['Sector', year_column]]
                return averages_df.rename(columns={year_column: "AltmanZscore"}).to_dict(orient="records")
            else:
                averages_df = averages_df[averages_df['Org Name'].str.contains('Average', case=False, na=False)]
                averages_df = averages_df.drop(columns=['Sub-Sector', 'Org Name'], errors='ignore')
                return averages_df.to_dict(orient="records")

        except Exception as e:
            logger.error(f"Error retrieving sector averages: {str(e)}", exc_info=True)
            return {"error": str(e)}

    def _handle_all_orgs_in_sector(self, sector, year):
        """
        Handles the use case: sector given, no sub_sector, org_name="All".
        Returns Altman Z-scores for each organization within the specified sector.
        Includes the count of organizations processed and returned.
        """
        logger.info(f"Handling: sector='{sector}', org_name='All', no sub_sector (all orgs in sector)")

        sector_orgs_df = self.df_pivot[self.df_pivot['Sector'].str.lower() == sector.lower()].copy()

        if sector_orgs_df.empty:
            return Response({"message": f"No organizations found in sector '{sector}'."},
                            status=status.HTTP_404_NOT_FOUND)

        unique_org_names = sector_orgs_df['Org Name'].unique()
        total_orgs_in_sector = len(unique_org_names)

        results = []
        predefined_sub_indicators = [
            '1. Capital work in progress', 'Total Assets (A+B) / Equity & Liabilities (C+D+E)',
            'of which: un-appropriated profit(loss) / retained earnings', '6. EBIT (F3-F4+F5)',
            "C. Shareholders' Equity (C1+C2+C3)", 'D. Non-Current Liabilities (D1+D2+D3+D4+D5)',
            'E. Current Liabilities (E1+E2+E3+E4)'
        ]

        for org_name in unique_org_names:
            org_data = sector_orgs_df[sector_orgs_df['Org Name'].str.lower() == org_name.lower()].copy()

            org_data_filtered = org_data[
                (org_data['Sub Indicator'].str.strip().str.lower().isin([s.lower() for s in predefined_sub_indicators])) |
                (org_data['Indicator'].str.strip().str.lower().isin([s.lower() for s in predefined_sub_indicators])) |
                (org_data['Sub-Sub Indicator'].str.strip().str.lower().isin([s.lower() for s in predefined_sub_indicators]))
            ].copy()

            org_data_filtered.drop_duplicates(subset=['Indicator', 'Sub Indicator', 'Sub-Sub Indicator'], keep='first', inplace=True)

            altman_scores = {}
            if org_data_filtered.empty:
                logger.warning(f"No sufficient data to calculate Altman Z-score for organization: {org_name} in sector {sector}")
                # We don't append to results if there's no data at all
            else:
                altman_scores = self.calculate_altman_score(org_data_filtered)

            if altman_scores and not (isinstance(altman_scores, dict) and altman_scores.get(year, "") == "Insufficient data" or altman_scores.get(year, "") == "Insufficient data (missing TA)"):
                 org_result = {
                    "org_name": org_name,
                    "sector": sector,
                    "sub_sector": org_data['Sub-Sector'].iloc[0] if not org_data['Sub-Sector'].empty else None,
                    "altman_zscore": self.replace_nan(altman_scores.get(year, altman_scores) if year and year.lower() != "all" else altman_scores)
                }
                 results.append(org_result)
            elif not altman_scores:
                logger.warning(f"Altman Z-score calculation returned no valid scores for organization: {org_name} in sector {sector}")


        if not results:
             return Response({"message": f"No Altman Z-scores could be calculated for any organization in sector '{sector}'. "
                                        f"Total organizations identified in sector: {total_orgs_in_sector}"},
                            status=status.HTTP_404_NOT_FOUND)

        return Response({
            "sector": sector,
            "query_type": "All Organizations in Sector",
            "year": year if year else "all",
            "total_organizations_in_sector": total_orgs_in_sector,
            "organizations_returned_count": len(results),
            "organizations_data": results
        }, status=status.HTTP_200_OK)

    # --- REINSTATED AND CORRECTED HELPER METHOD ---
    def _handle_all_org_name_precalculated_averages(self, sector, sub_sector, year):
        """
        Handles the case where org_name="All" using the pre-calculated sector averages.
        This covers requests like /altmanzscore?org_name=All&sector=Finance&sub_sector=Banking
        or /altmanzscore?org_name=All&sector=Finance
        """
        try:
            average_data = self.df_sector_avg[self.df_sector_avg['Org Name'].str.contains('Average', case=False, na=False)].copy()

            if sector and sector.lower() != "all":
                average_data = average_data[average_data['Sector'].str.lower() == sector.lower()]

            if sub_sector:
                average_data = average_data[average_data['Sub-Sector'].str.lower() == sub_sector.lower()]

            if average_data.empty:
                return Response({"message": "No average data found matching the specified criteria."},
                                status=status.HTTP_404_NOT_FOUND)

            if year and year.lower() != "all":
                year_column = f"AltmanZscore {year}"
                if year_column not in average_data.columns:
                    return Response({"message": f"No data found for the year {year}."},
                                    status=status.HTTP_404_NOT_FOUND)

                result_value = average_data[year_column].iloc[0]

                return Response({
                    "sector": sector,
                    "sub_sector": sub_sector if sub_sector else "N/A", # Indicate N/A if no sub_sector was specified
                    "org_name": "All (Pre-calculated Average)",
                    "year": year,
                    "altman_zscore": self.replace_nan(result_value)
                }, status=status.HTTP_200_OK)
            else: # year is "all"
                year_columns = [col for col in average_data.columns if col.startswith('AltmanZscore')]

                result_dict = {}
                for col in year_columns:
                    year_value = col.split(' ')[1]
                    result_dict[year_value] = average_data[col].iloc[0]

                return Response({
                    "sector": sector,
                    "sub_sector": sub_sector if sub_sector else "N/A", # Indicate N/A if no sub_sector was specified
                    "org_name": "All (Pre-calculated Averages)",
                    "year": "all",
                    "altman_zscore": self.replace_nan(result_dict)
                }, status=status.HTTP_200_OK)
        except Exception as e:
            logger.error(f"Error processing pre-calculated average data: {str(e)}", exc_info=True)
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def _handle_all_sector_breakdown(self, year):
        """
        Handles the case where sector="All", providing a breakdown by sector and sub-sector,
        using the pre-calculated averages from df_sector_avg.
        """
        filtered_df = self.df_sector_avg.copy()

        all_possible_years = []
        for col in filtered_df.columns:
            if col.startswith('AltmanZscore '):
                year_value = col.split(' ')[1]
                all_possible_years.append(year_value)
        all_possible_years = sorted(list(set(all_possible_years)))

        sector_groups = {}

        # Use df_pivot to get actual organization counts
        all_orgs_for_counts = self.df_pivot.copy()

        # Populate sector_groups structure with actual counts from df_pivot
        for sector_name in all_orgs_for_counts['Sector'].unique():
            sector_name_l = sector_name.lower()
            total_orgs_in_current_sector = all_orgs_for_counts[all_orgs_for_counts['Sector'].str.lower() == sector_name_l]['Org Name'].nunique()

            sector_groups[sector_name] = {
                "sector": sector_name,
                "sub_sectors": {},
                "years": {yr: None for yr in all_possible_years},
                "total_organizations_in_sector": total_orgs_in_current_sector
            }

            for sub_sector_name in all_orgs_for_counts[all_orgs_for_counts['Sector'].str.lower() == sector_name_l]['Sub-Sector'].dropna().unique():
                sub_sector_name_l = sub_sector_name.lower()
                total_orgs_in_current_subsector = all_orgs_for_counts[
                    (all_orgs_for_counts['Sector'].str.lower() == sector_name_l) &
                    (all_orgs_for_counts['Sub-Sector'].str.lower() == sub_sector_name_l)
                ]['Org Name'].nunique()

                sector_groups[sector_name]["sub_sectors"][sub_sector_name] = {
                    "sub_sector": sub_sector_name,
                    "years": {yr: None for yr in all_possible_years},
                    "total_organizations_in_sub_sector": total_orgs_in_current_subsector,
                    "sum_for_sector_avg": {yr: None for yr in all_possible_years}
                }


        # Now, fill in the Altman Z-scores using subsector_averages_data
        for _, row in filtered_df[filtered_df['Org Name'].str.contains('Average', case=False, na=False)].iterrows():
            current_sector = row['Sector']
            current_sub_sector = row['Sub-Sector']
            
            if current_sector in sector_groups and current_sub_sector in sector_groups[current_sector]["sub_sectors"]:
                sub_sector_info = sector_groups[current_sector]["sub_sectors"][current_sub_sector]
                total_orgs_in_subsector_for_calc = sub_sector_info["total_organizations_in_sub_sector"]

                for yr in all_possible_years:
                    year_col = f"AltmanZscore {yr}"
                    if year_col in row.index and pd.notna(row[year_col]):
                        sub_sector_info["years"][yr] = row[year_col]
                        sub_sector_info["sum_for_sector_avg"][yr] = row[year_col] * total_orgs_in_subsector_for_calc

        # Calculate overall sector averages from weighted sums
        for sector_name, sector_info in sector_groups.items():
            for year_str in all_possible_years:
                year_total_sum_for_sector = 0
                total_orgs_for_sector_avg_calc = 0

                for sub_sector_info in sector_info["sub_sectors"].values():
                    if sub_sector_info["sum_for_sector_avg"][year_str] is not None:
                        year_total_sum_for_sector += sub_sector_info["sum_for_sector_avg"][year_str]
                        total_orgs_for_sector_avg_calc += sub_sector_info["total_organizations_in_sub_sector"]

                if total_orgs_for_sector_avg_calc > 0:
                    sector_avg = year_total_sum_for_sector / total_orgs_for_sector_avg_calc
                    sector_groups[sector_name]["years"][year_str] = sector_avg


        results = []
        for sector_name, sector_info in sector_groups.items():
            sector_entry = {
                "sector": sector_name,
                "org_name": "Sector Average",
                "years": sector_info["years"],
                "total_organizations_in_sector": sector_info["total_organizations_in_sector"]
            }

            sub_sectors_list = []
            for sub_name, sub_info in sector_info["sub_sectors"].items():
                sub_data = {
                    "sub_sector": sub_info["sub_sector"],
                    "org_name": "Sub-Sector Average",
                    "years": sub_info["years"],
                    "total_organizations_in_sub_sector": sub_info["total_organizations_in_sub_sector"]
                }
                sub_sectors_list.append(sub_data)

            sector_entry["sub_sectors"] = sorted(sub_sectors_list, key=lambda x: x['sub_sector'])
            results.append(sector_entry)

        results = sorted(results, key=lambda x: x['sector'])
        results = self.replace_nan(results)

        return Response(
            {
                "query_type": "All Sectors Breakdown",
                "year": year if year else "all",
                "altman_zscores_by_sector": results
            },
            status=status.HTTP_200_OK
        )


    def _handle_specific_org_request(self, sector, sub_sector, org_name, year):
        """Handles requests for a specific organization."""
        filtered_df = self.df_pivot.copy()

        if sector:
            filtered_df = filtered_df[filtered_df['Sector'].str.lower() == sector.lower()]
        if sub_sector:
            filtered_df = filtered_df[filtered_df['Sub-Sector'].str.lower() == sub_sector.lower()]
        if org_name:
            filtered_df = filtered_df[filtered_df['Org Name'].str.lower() == org_name.lower()]

        if filtered_df.empty and org_name:
            logger.info(f"Trying flexible match for org_name: {org_name}")
            matched_df = self.df_pivot[self.df_pivot['Org Name'].str.contains(org_name, case=False, na=False)]
            if not matched_df.empty:
                filtered_df = matched_df
                logger.info(f"Found organization using flexible match: {matched_df['Org Name'].iloc[0]}")

        if filtered_df.empty:
            return Response({"message": "No data found for the specified organization."},
                            status=status.HTTP_404_NOT_FOUND)

        predefined_sub_indicators = [
            '1. Capital work in progress', 'Total Assets (A+B) / Equity & Liabilities (C+D+E)',
            'of which: un-appropriated profit(loss) / retained earnings', '6. EBIT (F3-F4+F5)',
            "C. Shareholders' Equity (C1+C2+C3)", 'D. Non-Current Liabilities (D1+D2+D3+D4+D5)',
            'E. Current Liabilities (E1+E2+E3+E4)'
        ]
        filtered_df = filtered_df[
            (filtered_df['Sub Indicator'].str.strip().str.lower().isin([s.lower() for s in predefined_sub_indicators])) |
            (filtered_df['Indicator'].str.strip().str.lower().isin([s.lower() for s in predefined_sub_indicators])) |
            (filtered_df['Sub-Sub Indicator'].str.strip().str.lower().isin([s.lower() for s in predefined_sub_indicators]))
        ].copy()

        filtered_df.drop_duplicates(subset=['Indicator', 'Sub Indicator', 'Sub-Sub Indicator'], keep='first', inplace=True)

        if year and year.lower() != "all":
            if year not in filtered_df.columns and f"AltmanZscore {year}" not in filtered_df.columns:
                return Response({"message": f"No data found for the year {year}."},
                                status=status.HTTP_404_NOT_FOUND)

            cols_to_keep = ['Sector', 'Sub-Sector', 'Org Name', 'Indicator', 'Sub Indicator', 'Sub-Sub Indicator']
            if year in filtered_df.columns:
                cols_to_keep.append(year)
            elif f"AltmanZscore {year}" in filtered_df.columns:
                cols_to_keep.append(f"AltmanZscore {year}")

            filtered_df_for_calc = filtered_df[cols_to_keep]

            altman_zscore = self.calculate_altman_score(filtered_df_for_calc)
            response_data = {
                "sector": sector,
                "sub_sector": sub_sector,
                "org_name": org_name,
                "year": year,
                "altman_zscore": self.replace_nan(altman_zscore.get(year, "Insufficient data or error in calculation"))
            }
        else:
            altman_zscore = self.calculate_altman_score(filtered_df)
            response_data = {
                "sector": sector,
                "sub_sector": sub_sector,
                "org_name": org_name,
                "year": "all",
                "altman_zscore": self.replace_nan(altman_zscore)
            }
        return Response(response_data, status=status.HTTP_200_OK)


    def get(self, request):
        try:
            sector = request.query_params.get('sector', None)
            sub_sector = request.query_params.get('sub_sector', None)
            org_name = request.query_params.get('org_name', None)
            year = request.query_params.get('year', None)

            sector_l = sector.lower() if sector else None
            sub_sector_l = sub_sector.lower() if sub_sector else None
            org_name_l = org_name.lower() if org_name else None
            year_l = year.lower() if year else None

            # New Use Case: sector given, no sub_sector, org_name="All" - returns individual orgs in sector
            if sector_l and not sub_sector_l and org_name_l == "all":
                return self._handle_all_orgs_in_sector(sector, year)

            # Existing Use Case 1: org_name="All" and (sector/sub_sector are given or all) - uses pre-calculated averages
            # This handles queries like ?org_name=All&sector=Finance&sub_sector=Banking
            # OR ?org_name=All&sector=Finance (which would be handled by _handle_all_org_name_precalculated_averages)
            if org_name_l == "all":
                 return self._handle_all_org_name_precalculated_averages(sector, sub_sector, year)

            # Existing Use Case 2: sector="All" (overall breakdown by sector/sub-sector) - uses pre-calculated averages
            elif sector_l == "all":
                return self._handle_all_sector_breakdown(year)

            # Existing Use Case 3: Specific organization request
            elif org_name:
                return self._handle_specific_org_request(sector, sub_sector, org_name, year)

            else:
                return Response({"message": "Please provide 'org_name', 'sector', or 'sub_sector' parameters. "
                                           "Use 'org_name=All' for sector/all organizations, or 'sector=All' for overall breakdown."},
                                status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            logger.error(f"Unhandled error in AltmanZScoreView.get: {str(e)}", exc_info=True)
            return Response({"error": "An internal server error occurred. Please try again later."},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)