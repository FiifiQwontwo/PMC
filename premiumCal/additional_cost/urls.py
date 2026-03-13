from .views import ListAdditionalCostView, CreateAdditional_costView, Additional_CostDetailView, Delete_Additional_CostView, UpdateAdditional_CostView
from django.urls import path

app_name = 'additional_cost'

urlpatterns = [
    path('list/', ListAdditionalCostView.as_view(), name='list_additional_cost_endpoint'),
    path('detail/<int:pk>', Additional_CostDetailView.as_view(), name='details_additional_cost_endpoint'),
    path('up/<int:pk>', UpdateAdditional_CostView.as_view(), name='update_additional_cost_endpoint'),
    path('dels/<int:pk>', Delete_Additional_CostView.as_view(), name='dels_additional_cost_endpoint'),
    path('new/', CreateAdditional_costView.as_view(), name='add_additional_cost_endpoint'),

]


