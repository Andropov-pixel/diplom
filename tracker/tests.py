from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status

from .models import Tracker
from employee.models import Employee


class TrackerTest(APITestCase):
    """ Тест модели TRACKER """

    def setUp(self):
        """ Прописывем исходные данные и необходимые параметры """

        # Очищаем всю БД для корректной работы
        Employee.objects.all().delete()
        Tracker.objects.all().delete()

        # Создаем необходимы модели
        self.employee = Employee.objects.create(fio='Алексеев Алексей Алексеевич')
        self.tracker = Tracker.objects.create(title='Test', time='2 дня')

    def test_tracker_create(self):
        """ Тестирование создание обьекта TRACKER """

        data = {
            'title': 'TESTtitle',
            'time': 'TESTtime',
            'status': 'active',
            'employees': self.employee.id,
        }
        response = self.client.post(
            '/tracker/',
            data=data
        )

        # Сверяем статус код
        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED
        )

        # Сверяем ожидаемое количество Tracker в БД
        self.assertEqual(
            Tracker.objects.count(),
            2
        )

        # Сверяем данные с ожидаемыми
        self.assertEqual(
            response.json(),
            {'id': 7, 'title': 'TESTtitle', 'time': 'TESTtime', 'status': 'active', 'related_tracker': None,
             'employees': [7]}
        )

    def test_tracker_list(self):
        """ Тест списка всех TRACKER в БД """

        url = reverse('tracker:tracker-list')
        response = self.client.get(url)
        data = response.json()
        print(data)
        # Сверяем статус кода
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Сверяем данные с ожидаемыми
        self.assertEqual(
            data,
            [{'id': 9, 'title': 'Test', 'time': '2 дня', 'status': 'inactive',
              'related_tracker': None, 'employees': []}]
        )

        # Сверяем ожидаемое количество Tracker в БД
        self.assertEqual(
            Tracker.objects.count(),
            1
        )

    def test_tracker_retrieve(self):
        """ Тест детальной информации обьекта TRACKER """

        url = reverse('tracker:tracker-detail', args=(self.tracker.pk,))
        response = self.client.get(url)
        data = response.json()

        # Сверяем статус кода
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Сверяем данные с ожидаемыми
        self.assertEqual(
            data,
            {'id': self.tracker.id, 'title': 'Test', 'time': '2 дня', 'status': 'inactive',
             'related_tracker': None, 'employees': []}
        )

    def test_tracker_update(self):
        """ Тестирование обновление обьекта TRACKER """

        url = reverse("tracker:tracker-detail", args=(self.tracker.pk,))

        data = {
            'employees': [self.employee.id],
            'related_tracker': [self.tracker.id],
            'status': 'inactive',
            'time': 'TESTtime',
            'title': 'TESTtitle',
        }
        response = self.client.patch(url, data=data)

        # Сверяем статус код
        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )

        # Сверяем ожидаемое количество Tracker в БД
        self.assertEqual(
            Tracker.objects.count(),
            1
        )

        # Сверяем данные с ожидаемыми
        self.assertEqual(
            response.json()["status"], 'inactive')

    def test_tracker_delete(self):
        """ Тестирование удаление обьекта TRACKER """

        url = reverse("tracker:tracker-detail", args=(self.tracker.pk,))

        response = self.client.delete(url)

        # Сверяем статус код
        self.assertEqual(
            response.status_code,
            status.HTTP_204_NO_CONTENT
        )

        # Сверяем ожидаемое количество Tracker в БД
        self.assertEqual(
            Tracker.objects.count(),
            0
        )