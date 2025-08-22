from faker import Faker
import pandas as pd
import random

# Создаем экземпляр класса Faker
fake = Faker()

# Задаем количество записей
num_records = 100

# Определяем возможные статусы и приоритеты
statuses = ['Не активна', 'В работе', 'Выполнена']

# Создаем списки для хранения данных
data = {
    'ID задачи': [],
    'Название': [],
    'Связанная приятная задача': [],
    'Статус выполнения': [],
    'Срок выполнения': [],
    'Сотрудники': [],
    'Дата создания': [],
}

# Заполняем список случайными данными
for task_id in range(1, num_records + 1):
    data['ID задачи'].append(task_id)
    data['Название'].append(fake.sentence(nb_words=6))
    data['Связанная приятная задача'].append(fake.text(max_nb_chars=200))
    data['Статус выполнения'].append(random.choice(statuses))
    data['Срок выполнения'].append(fake.date_between(start_date='today', end_date='+30d'))
    data['Сотрудники'].append(fake.name())
    data['Дата создания'].append(fake.date_this_year())

# Превращаем данные в DataFrame
df = pd.DataFrame(data)

# Сохраняем таблицу в CSV файл
df.to_csv('task_tracker.csv', index=False, encoding='utf-8-sig')

print("Таблица задач успешно заполнена и сохранена в 'task_tracker.csv'")