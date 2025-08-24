import django_filters
from django.db.models import Count, Min

from employee.models import Employee


class EmployeeFilter(django_filters.FilterSet):
    """Фильтры для модели EMPLOYEE """

    # Фильтрация сотрудника по количеству задач <=
    count_lte = django_filters.NumberFilter(field_name='tracker_count', lookup_expr='lte')

    # Фильтрация сотрудника по количеству задач >=
    count_gte = django_filters.NumberFilter(field_name='tracker_count', lookup_expr='gte')

    # Кастомный фильтр для получения сотрудников которые выполняют одну из связанных задач или имеют загруженность по
    # задачам максимум на 2 больше от самого разгруженного сотрудника
    can_take_task = django_filters.BooleanFilter(method='filter_can_take_task')

    class Meta:
        model = Employee
        fields = ('count_lte', 'count_gte', 'can_take_task')

    def filter_can_take_task(self, queryset, name, value):
        """ Метод фильтра сотрудников по возмождности принятия дополнительной задачи """

        # Получаем минимальное количество задач у любого сотрудника
        min_tracker_count = queryset.annotate(tracker_count=Count('trackers')).aggregate(
            Min('tracker_count'))['tracker_count__min']

        # Фильтруем сотрудников, которые могут взять задачи:
        # Сотрудники, у которых количество задач <= min_task_count + 2
        possible_employees = queryset.filter(tracker_count__lte=min_tracker_count + 2)

        # Сотрудники, у которых есть родительская задача
        parent_tasks_employees = queryset.filter(
            trackers__related_tracker__isnull=False
        )

        # Объединяем результаты
        return queryset.filter(pk__in=parent_tasks_employees | possible_employees)