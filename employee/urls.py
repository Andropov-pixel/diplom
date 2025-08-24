from django.conf.urls.static import static
from rest_framework.routers import DefaultRouter

from config import settings
from employee.apps import EmployeeConfig
from employee.views import EmployeeViewset


app_name = EmployeeConfig.name

router = DefaultRouter()
router.register("", EmployeeViewset, basename="employee")

urlpatterns = []

urlpatterns += router.urls

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)