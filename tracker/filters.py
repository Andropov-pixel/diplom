import django_filters
from django.db.models import Q

from tracker.models import Tracker


class TrackerFilter(django_filters.FilterSet):
    """Фильтры для модели TACKER """

    # Фильтрует по статусу tracker
    status = django_filters.CharFilter(field_name="status", lookup_expr="exact")

    # Фильтрует по наличию связанных задач
    related_tracker_isnull = django_filters.BooleanFilter(field_name="related_tracker", lookup_expr="isnull")

    # Фильтрует по статусу связанной задачи
    related_tracker_status = django_filters.CharFilter(field_name="related_tracker__status", lookup_expr="exact")

    # Фильтрует задачи и выводит только важные
    # (которые не взяты в работу, но имеют связанную задачу, которая взята в работу)
    important_trackers = django_filters.BooleanFilter(method='filter_important_trackers')

    class Meta:
        model = Tracker
        fields = ['status', 'related_tracker_isnull', 'related_tracker_status', 'important_trackers']

    def filter_important_trackers(self, queryset, name, value):
        """ Метод для вывода только важных задач """

        # Фильтруем по статусу inactive
        status_check = queryset.filter(status="inactive")

        # Фильтруем по наличию связанной задачи
        related_tracker_check = queryset.filter(related_tracker__isnull=False)

        # Фильтруем по статусу active связанной задачи
        related_tracker_status_check = queryset.filter(related_tracker__status="active")

        # Объединяем условия
        return queryset.filter(Q(pk__in=status_check) & Q(pk__in=related_tracker_check) &
                               Q(pk__in=related_tracker_status_check))