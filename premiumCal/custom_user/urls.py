from .views import LoginView
from django.urls import path

app_name = 'custom_user'

urlpatterns = [
    path('login/', LoginView.as_view(), name='login_endpoint'),

]


