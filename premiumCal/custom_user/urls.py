from .views import LoginView, LogoutView, AdminRegistrationView
from django.urls import path

app_name = 'custom_user'

urlpatterns = [
    path('login/', LoginView.as_view(), name='login_endpoint'),
    path('logout/', LogoutView.as_view(), name='logout_endpoint'),
    path('admin/', AdminRegistrationView.as_view(), name='admin_user_endpoint'),

]


