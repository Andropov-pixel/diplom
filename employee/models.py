from django.db import models


class Employee(models.Model):
    """ Модель: Сотрудник """

    fio = models.CharField(
        max_length=200, verbose_name="ФИО сотрудника"
    )
    employee_position = models.CharField(
        max_length=100, blank=True, null=True, verbose_name="Должность"
    )
    # trackers = models.ManyToManyField(
    #     Tracker, blank=True, verbose_name="Задача"
    # )

    class Meta:
        verbose_name = "Сотрудник"
        verbose_name_plural = "Сотрудники"

    def __str__(self):
        return self.fio