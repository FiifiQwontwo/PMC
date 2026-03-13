from rest_framework import serializers
from .models import Currency_Rate


class List_Currency_Rate_Serializer(serializers.ModelSerializer):
    class Meta:
        model = Currency_Rate
        fields = ('currency_name', 'currency_rate', 'currency_shortrate_charge',
                  'currency_symbol')


class Create_Currency_RateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Currency_Rate
        fields = ('currency_name', 'currency_rate', 'currency_shortrate_charge',
                  'currency_symbol')

    def save(self, **kwargs):
        currency_name = self.validated_data.get('currency_name')
        currency_rate = self.validated_data.get('currency_rate')
        currency_shortrate_charge = self.validated_data.get('currency_shortrate_charge')
        currency_symbol = self.validated_data.get('currency_symbol')

        new_class = Currency_Rate(
            currency_rate=currency_rate,
            currency_name=currency_name,
            currency_shortrate_charge=currency_shortrate_charge,
            currency_symbol=currency_symbol
        )
        new_class.save()
        return new_class


class Update_Currency_Rate_Serializer(serializers.ModelSerializer):
    class Meta:
        model = Currency_Rate
        fields = "__all__"
        read_only_fields = ["created_at", "updated_at"]

    def update(self, instance, validated_data):
        instance = super().update(instance, validated_data)
        return instance


class Currency_Rate_DetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Currency_Rate
        fields = '__all__'
