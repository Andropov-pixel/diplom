from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def habit_list(request):
    habits = [
        {
            "id": 1,
            "name": "Утренняя зарядка",
            "place": "Дом",
            "time": "07:00",
            "action": "15 минут упражнений",
            "is_pleasant": True,
            "frequency": 1,
            "reward": "Кофе",
            "time_to_complete": 15,
            "is_public": True
        },
        {
            "id": 2,
            "name": "Изучение английского",
            "place": "Работа",
            "time": "18:00",
            "action": "30 минут занятий",
            "is_pleasant": False,
            "frequency": 1,
            "reward": "Отдых",
            "time_to_complete": 30,
            "is_public": False
        }
    ]
    return Response(habits)

# ДОБАВЬТЕ ЭТУ ФУНКЦИЮ ↓
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def habit_detail(request, pk):
    # Временные данные для демонстрации
    habit = {
        "id": pk,
        "name": f"Привычка {pk}",
        "place": "Место выполнения",
        "time": "12:00",
        "action": "Действие привычки",
        "is_pleasant": True,
        "frequency": 1,
        "reward": "Награда",
        "time_to_complete": 30,
        "is_public": True
    }
    return Response(habit)

@api_view(['GET'])
@permission_classes([AllowAny])
def public_habits(request):
    public_habits = [
        {
            "id": 1,
            "name": "Утренняя зарядка",
            "place": "Дом",
            "time": "07:00",
            "action": "15 минут упражнений",
            "time_to_complete": 15
        },
        {
            "id": 3,
            "name": "Вечерняя прогулка",
            "place": "Парк",
            "time": "21:00",
            "action": "Прогулка 40 минут",
            "time_to_complete": 40
        }
    ]
    return Response(public_habits)