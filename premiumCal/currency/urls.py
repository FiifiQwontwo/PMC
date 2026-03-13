from .views import ListCurrency_RateView, CreateCurrency_RateView
from django.urls import path

app_name = 'currency'

urlpatterns = [
    path('list/', ListCurrency_RateView.as_view(), name='list_currency_rate_endpoint'),
    path('new/', CreateCurrency_RateView.as_view(), name='add_currency_rate_endpoint'),

]


