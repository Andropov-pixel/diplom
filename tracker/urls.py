from django.conf.urls.static import static
from rest_framework.routers import DefaultRouter

from config import settings
from tracker.apps import TrackerConfig
from tracker.views import TrackerViewset


app_name = TrackerConfig.name

router = DefaultRouter()
router.register("", TrackerViewset, basename="tracker")

urlpatterns = []

urlpatterns += router.urls

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)