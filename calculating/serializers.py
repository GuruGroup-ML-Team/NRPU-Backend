from rest_framework import serializers

class IndicatorSerializer(serializers.Serializer):
    sector = serializers.CharField(max_length=100)
    indicator = serializers.CharField(max_length=100)
    sub_indicator = serializers.CharField(max_length=100, required=False)
    year = serializers.IntegerField()
