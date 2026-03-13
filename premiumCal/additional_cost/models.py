from django.db import models


# Create your models here.
class AdditionalCost(models.Model):
    brown_card_charge = models.DecimalField(decimal_places=2, max_digits=10)
    nic_contribution_charge = models.DecimalField(decimal_places=2, max_digits=10)
    sticker_charge = models.DecimalField(decimal_places=2, max_digits=10, default=0.00)
    age_loading_charge = models.DecimalField(decimal_places=2, max_digits=10, blank=True, null=True)
    age_loading_percentage = models.DecimalField(decimal_places=2, max_digits=10, blank=True, null=True)
    educational_fee = models.DecimalField(decimal_places=2, max_digits=10, default=0.00)
    gia_levy = models.DecimalField(decimal_places=2, max_digits=10, default=0.00)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.sticker_charge
