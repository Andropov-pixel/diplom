from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import TrackerViewSet

app_name = 'tracker'

router = DefaultRouter()
router.register(r'tracker', TrackerViewSet)  # ← ПРОВЕРЬТЕ ЧТО НЕТ ЛИШНИХ СКОБОК

urlpatterns = [
    path('', include(router.urls)),  # ← ПРАВИЛЬНЫЙ СИНТАКСИС
]