from rest_framework import viewsets
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter
from rest_framework.response import Response

from employee.models import Employee
from tracker.filters import TrackerFilter
from tracker.models import Tracker
from tracker.serializer import TrackerSerializer


class TrackerViewset(viewsets.ModelViewSet):
    """ViewSet для модели TRACKER"""

    queryset = Tracker.objects.all()
    serializer_class = TrackerSerializer
    filter_backends = (DjangoFilterBackend, OrderingFilter)
    filterset_class = TrackerFilter
    ordering_fields = ('id', 'status')

    def list(self, request, *args, **kwargs):
        """Вывод информации списка согласно шаблона"""

        # Список заданных параметров на фильтрацию в поисковой строке
        filter_params = request.query_params

        # Проверяем наличие фильтра в запросе
        if filter_params.get("important_trackers") == "true":

            # Список задач, у которых не назначен Сотрудник
            queryset = Tracker.objects.filter(employees__isnull=True)

            # Сериализация
            serializer = self.get_serializer(queryset, many=True)

            formatted_response = []

            employees = EmployeeSerializer(Employee.objects.all(), many=True).data  # Все Сотрудники

            # Мин кол-во задач Сотрудников
            min_count_trackers = len(min(employees, key=lambda x: len(x["trackers"]))["trackers"])

            # Сотрудники с мин. кол-вом задач
            least_busy_employee = [employee for employee in employees if
                                   len(employee["trackers"]) == min_count_trackers]
            for item in serializer.data:
                related_tracker = item["related_tracker"]
                if related_tracker:
                    # Сотрудник, выполняющий связанную задачу
                    related_employee = Employee.objects.get(pk=related_tracker)
                    count_task_related_employee = related_employee.trackers.count()

                    if count_task_related_employee <= min_count_trackers + 2:
                        employee_names = [related_employee.fio]
                    else:
                        employee_names = [employee["fio"] for employee in least_busy_employee]
                else:
                    employee_names = [employee["fio"] for employee in least_busy_employee]

                # Создаем необходимый формат ответа
                formatted_response.append({

                    "Важная задача": item['title'],
                    "Срок выполнения": item['time'],
                    "Выполняющие": employee_names,
                })

            return Response(formatted_response)

        serializer = self.get_serializer(self.queryset, many=True)
        return Response(serializer.data)