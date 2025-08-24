from django.db.models import Count
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets
from rest_framework.filters import OrderingFilter

from employee.filters import EmployeeFilter
from employee.models import Employee
from employee.serializer import EmployeeSerializer


class EmployeeViewset(viewsets.ModelViewSet):
    """ViewSet для модели EMPLOYEE"""

    queryset = Employee.objects.annotate(tracker_count=Count('trackers'))
    serializer_class = EmployeeSerializer
    filter_backends = (DjangoFilterBackend, OrderingFilter)
    filterset_class = EmployeeFilter
    ordering_fields = ('id', 'tracker_count')