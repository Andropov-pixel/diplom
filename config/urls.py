from django.urls import path, include
from django.contrib import admin
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from django.http import JsonResponse
from django.shortcuts import redirect


def api_root(request):
    return JsonResponse({
        "message": "Добро пожаловать в API",
        "endpoints": {
            "admin": "/admin/",
            "api": "/api/",
            "token_obtain": "/api/token/",
            "token_refresh": "/api/token/refresh/"
        }
    })


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/', include('habits.urls')),

    # Добавьте корневой маршрут
    path('', api_root),  # или используйте redirect: path('', lambda request: redirect('api/'))
]