# books/management/commands/load_tasks.py
from django.core.management.base import BaseCommand
from django.core.management import call_command

class Command(BaseCommand):
    help = "Загружает данные сотрудников и задач из фикстуры."

    def handle(self, *args, **kwargs):
        call_command('loaddata', 'tasks_fixture.json')
        self.stdout.write(self.style.SUCCESS('Данные сотрудников и задач загружены успешно.'))