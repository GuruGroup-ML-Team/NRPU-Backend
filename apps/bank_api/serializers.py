# bank_api/serializers.py
from rest_framework import serializers

class BankComparisonSerializer(serializers.Serializer):
    banks = serializers.ListField(
        child=serializers.CharField(),
        min_length=1,
        required=True
    )
    metrics = serializers.ListField(
        child=serializers.CharField(),
        min_length=1,
        required=True
    )
    year = serializers.CharField(default="2023", required=False)

class BankComparativeAnalysisSerializer(serializers.Serializer):
    """
    Serializer for bank comparative analysis API.
    """
    banks = serializers.ListField(
        child=serializers.CharField(),
        min_length=1,
        help_text="List of bank names to compare"
    )
    year = serializers.CharField(
        required=False,
        default="2023",
        help_text="Year for analysis (default: 2023)"
    )

class BankRatioAnalysisSerializer(serializers.Serializer):
    """
    Serializer for bank ratio analysis API parameters.
    """
    bank_name = serializers.CharField(help_text="Name of the bank to analyze")
    year = serializers.CharField(
        required=False,
        default="2023",
        help_text="Year for analysis (default: 2023)"
    )
    include_trends = serializers.BooleanField(
        required=False,
        default=False,
        help_text="Include multi-year trends data"
    )

class BankScoreSerializer(serializers.Serializer):
    """
    Serializer for bank scoring API.
    """
    banks = serializers.ListField(
        child=serializers.CharField(),
        min_length=1,
        help_text="List of bank names to score"
    )
    year = serializers.CharField(
        required=False,
        default="2023",
        help_text="Year for scoring (default: 2023)"
    )
    weights = serializers.DictField(
        required=False,
        default={
            "efficiency": 0.60,
            "liquidity": 0.25,
            "asset_quality": 0.15,
            "capital": 0.10
        },
        help_text="Category weightings for score calculation"
    )
