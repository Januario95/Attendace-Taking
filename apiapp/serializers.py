from rest_framework import serializers
from .models import (
    Event, Attendee, Attendance,
    TableDevice
)


class TableDeviceSerializer(serializers.ModelSerializer):
    class Meta:
        model = TableDevice
        fields = '__all__'


class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = '__all__'
        depth = 1


class AttendeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Attendee
        fields = '__all__'
        depth = 1


class AttendanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Attendance
        fields = '__all__'
        depth = 1
