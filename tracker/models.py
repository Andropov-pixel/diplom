from django.db import models

from employee.models import Employee


class Tracker(models.Model):
    """ Модель: Задачи """

    STATUS_CHOICE = [

        ('inactive', 'Не активна'),
        ('active', 'В работе'),
        ('complete', 'Выполнена')
    ]

    title = models.CharField(
        max_length=100, verbose_name="Название"
    )
    related_tracker = models.ForeignKey(
        "self", on_delete=models.SET_NULL, verbose_name="Связанная приятная задача", blank=True, null=True
    )
    time = models.CharField(
        blank=True, null=True, verbose_name="Срок выполнения"
    )
    status = models.CharField(
        max_length=100, choices=STATUS_CHOICE, default='inactive', blank=True, null=True,
        verbose_name="Статус выполнения"
    )
    employees = models.ManyToManyField(
        Employee, blank=True, verbose_name="Сотрудники", related_name="trackers"
    )

    class Meta:
        verbose_name = "Задача"
        verbose_name_plural = "Задачи"

    def __str__(self):
        return self.title