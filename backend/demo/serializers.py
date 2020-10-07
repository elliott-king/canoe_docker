from rest_framework import serializers
from demo.models import Client, Fund, Investment, CashFlow

class ClientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Client
        fields = ('id', 'name', 'permission')

class FundSerializer(serializers.ModelSerializer):
    class Meta:
        model = Fund
        fields = ('id', 'name', 'type_field', 'description', 'inception_date')

class InvestmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Investment
        fields = ('id', 'name', 'date', 'amount', 'client_id', 'fund', 'current_value')
        depth = 1

class CashFlowSerializer(serializers.ModelSerializer):
    class Meta:
        model = CashFlow
        fields = ('date', 'return_field', 'investment_id')