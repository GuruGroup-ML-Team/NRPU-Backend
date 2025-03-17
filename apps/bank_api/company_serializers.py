from rest_framework import serializers


class CompanyComparisonSerializer(serializers.Serializer):
    """
    Serializer for company comparison API
    """
    companies = serializers.ListField(
        child=serializers.CharField(),
        min_length=1,
        required=True,
        help_text="List of company names to compare"
    )
    indicators = serializers.ListField(
        child=serializers.CharField(),
        min_length=1,
        required=True,
        help_text="List of indicators to compare"
    )
    year = serializers.CharField(
        default="2022",
        required=False,
        help_text="Year for data comparison (default: 2022)"
    )


class CompanyScoreSerializer(serializers.Serializer):
    """
    Serializer for company scoring API
    """
    companies = serializers.ListField(
        child=serializers.CharField(),
        min_length=1,
        help_text="List of company names to score"
    )
    year = serializers.CharField(
        required=False,
        default="2022",
        help_text="Year for scoring (default: 2022)"
    )
    weights = serializers.DictField(
        required=False,
        default={
            "profitability": 0.50,
            "liquidity": 0.25,
            "activity": 0.15,  # Note: renamed from efficiency to match the data structure
            "solvency": 0.10
        },
        help_text="Category weightings for score calculation"
    )


class CompanyTrendAnalysisSerializer(serializers.Serializer):
    """
    Serializer for company trend analysis API parameters
    """
    company = serializers.CharField(
        help_text="Name of the company to analyze"
    )
    years = serializers.ListField(
        child=serializers.CharField(),
        required=False,
        help_text="List of years to include in the trend analysis"
    )