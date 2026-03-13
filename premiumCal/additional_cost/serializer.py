from rest_framework import serializers
from .models import AdditionalCost


class ListAdditional_costSerializer(serializers.ModelSerializer):
    class Meta:
        model = AdditionalCost
        fields = ('brown_card_charge', 'nic_contribution_charge', 'sticker_charge',
                  'age_loading_charge', 'age_loading_percentage', 'educational_fee', 'gia_levy')


class CreateAdditional_costSerializer(serializers.ModelSerializer):
    class Meta:
        model = AdditionalCost
        fields = ('brown_card_charge', 'nic_contribution_charge', 'sticker_charge',
                  'age_loading_charge', 'age_loading_percentage', 'educational_fee', 'gia_levy')

    def save(self, **kwargs):
        brown_card_charge = self.validated_data.get('brown_card_charge')
        nic_contribution_charge = self.validated_data.get('nic_contribution_charge')
        sticker_charge = self.validated_data.get('sticker_charge')
        age_loading_charge = self.validated_data.get('age_loading_charge')
        educational_fee = self.validated_data.get('educational_fee')
        gia_levy = self.validated_data.get('gia_levy')

        new_class = AdditionalCost(
            brown_card_charge=brown_card_charge,
            nic_contribution_charge=nic_contribution_charge,
            sticker_charge=sticker_charge,
            age_loading_charge=age_loading_charge,
            educational_fee=educational_fee,
            gia_levy=gia_levy
        )
        new_class.save()
        return new_class


class UpdateAdditionalCostSerializer(serializers.ModelSerializer):
    class Meta:
        model = AdditionalCost
        fields = "__all__"
        read_only_fields = ["created_at", "updated_at", "user"]


class Additional_costDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = AdditionalCost
        fields = '__all__'
