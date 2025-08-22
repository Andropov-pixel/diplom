from rest_framework import serializers
from employee.models import Employee


class EmployeeSerializer(serializers.ModelSerializer):
    """ Сериализатор для модели EMPLOYEE """

    # Вывод поля tracker_count только для чтения
    tracker_count = serializers.IntegerField(read_only=True)
    trackers = TrackerSerializer(many=True, read_only=True)

    class Meta:
        model = Employee
        fields = ['id', 'fio', 'employee_position', 'tracker_count', 'trackers']