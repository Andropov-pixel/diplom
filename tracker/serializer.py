# tracker/serializers.py
from rest_framework import serializers
from tracker.models import Tracker

class TrackerSerializer(serializers.ModelSerializer):
    # НЕ импортируйте здесь ничего из employee!
    class Meta:
        model = Tracker
        fields = '__all__'