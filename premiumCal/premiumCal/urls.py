from django.contrib import admin
from django.urls import path, include
from rest_framework import permissions
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from drf_yasg import openapi
from django.conf import settings
from django.conf.urls.static import static

schema_view = get_schema_view(
    openapi.Info(
        title="Premium Calculator API",
        default_version='v1',
        description="API documentation for Premium Calculator",
        contact=openapi.Contact(email="info@bluespaceafrica.com"),
    ),
    public=True,
    permission_classes=[permissions.AllowAny],
)

url_base = 'api/'

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/additional_cost/', include('additional_cost.urls')),
    path('account/', include('custom_user.urls')),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
