from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status

from .models import Employee
from tracker.models import Tracker


class EmployeeTest(APITestCase):
    """ Тест модели EMPLOYEE """

    def setUp(self):
        """ Прописывем исходные данные и необходимые параметры """

        # Очищаем всю БД для корректной работы
        Employee.objects.all().delete()
        Tracker.objects.all().delete()

        # Создаем необходимы модели
        self.tracker = Tracker.objects.create(title='Test', time='2 дня')
        self.employee = Employee.objects.create(fio='Алексеев Алексей Алексеевич')

    def test_employee_create(self):
        """ Тестирование создание обьекта EMPLOYEE """

        data = {
            'fio': 'TESTfio',
            'employee_position': 'TESTpos',
        }
        response = self.client.post(
            '/employee/',
            data=data
        )
        # Сверяем статус код
        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED
        )

        # Сверяем ожидаемое количество Employee в БД
        self.assertEqual(
            Employee.objects.count(),
            2
        )

        # Сверяем данные с ожидаемыми
        self.assertEqual(
            response.json(),
            {'employee_position': 'TESTpos', 'fio': 'TESTfio', 'id': 2}
        )

    def test_employee_list(self):
        """ Тест списка всех EMPLOYEE в БД """

        url = reverse('employee:employee-list')
        response = self.client.get(url)
        data = response.json()

        # Сверяем статус кода
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Сверяем данные с ожидаемыми
        self.assertEqual(
            data,
            [{'id': self.employee.id, 'fio': 'Алексеев Алексей Алексеевич', 'employee_position': None,
              'tracker_count': 0}]
        )

        # Сверяем ожидаемое количество Employee в БД
        self.assertEqual(
            Employee.objects.count(),
            1
        )

    def test_employee_retrieve(self):
        """ Тест детальной информации обьекта EMPLOYEE """

        url = reverse('employee:employee-detail', args=(self.employee.pk,))
        response = self.client.get(url)
        data = response.json()

        # Сверяем статус кода
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Сверяем данные с ожидаемыми
        self.assertEqual(
            data,
            {'id': self.employee.id, 'fio': 'Алексеев Алексей Алексеевич', 'employee_position': None,
             'tracker_count': 0}

        )

    def test_employee_update(self):
        """ Тестирование обновление обьекта EMPLOYEE """

        url = reverse("employee:employee-detail", args=(self.employee.pk,))

        data = {
            'fio': 'TestUPDATE',
            'employee_position': 'TESTUPDATE',

        }
        response = self.client.patch(url, data=data)

        # Сверяем статус код
        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )

        # Сверяем ожидаемое количество Employee в БД
        self.assertEqual(
            Employee.objects.count(),
            1
        )

        # Сверяем данные с ожидаемыми
        self.assertEqual(
            response.json()["fio"], 'TestUPDATE')

    def test_employee_delete(self):
        """ Тестирование удаление обьекта EMPLOYEE """

        url = reverse("employee:employee-detail", args=(self.employee.pk,))

        response = self.client.delete(url)

        # Сверяем статус код
        self.assertEqual(
            response.status_code,
            status.HTTP_204_NO_CONTENT
        )

        # Сверяем ожидаемое количество Employee в БД
        self.assertEqual(
            Employee.objects.count(),
            0
        )