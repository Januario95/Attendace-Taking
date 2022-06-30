from rest_framework import serializers
from .models import (
    Event, Attendee, Attendance, TableBeacon
)


class BeaconSerializer(serializers.ModelSerializer):
    class Meta:
        model = TableBeacon
        fields = '__all__'
        depth = 1


class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = '__all__'
        depth = 1


class AttendeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Attendee
        fields = '__all__'
        depth = 2


class AttendanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Attendance
        fields = '__all__'
        depth = 2
