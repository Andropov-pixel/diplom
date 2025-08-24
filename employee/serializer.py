from rest_framework import serializers
from employee.models import Employee


class EmployeeSerializer(serializers.ModelSerializer):
    trackers = serializers.SerializerMethodField()  # Измените на этот тип

    class Meta:
        model = Employee
        fields = '__all__'

    def get_trackers(self, obj):
        # Импортируем внутри метода чтобы избежать циклического импорта
        from tracker.serializer import TrackerSerializer
        return TrackerSerializer(obj.tracker_set.all(), many=True).data