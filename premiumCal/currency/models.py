from django.db import models


# Create your models here.
class Currency_Rate(models.Model):
    currency_symbol = models.CharField(max_length=100, primary_key=True, unique=True)
    currency_name = models.CharField(max_length=100)
    currency_rate = models.DecimalField(decimal_places=2, max_digits=8)
    currency_shortrate_charge = models.DecimalField(decimal_places=2, max_digits=8)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.currency_name
