from rest_framework import serializers
from tracker.models import Tracker


class TrackerSerializer(serializers.ModelSerializer):
    """ Сериализатор для модели TRACKER """

    class Meta:
        model = Tracker
        fields = '__all__'