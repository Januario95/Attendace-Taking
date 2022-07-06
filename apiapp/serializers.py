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
        depth = 2


class AttendeeSerializer(serializers.ModelSerializer):
    events = serializers.SerializerMethodField()

    class Meta:
        model = Attendee
        fields = '__all__'
        depth = 2

    def get_events(self, obj):
        events = [obj.serialize() for obj in obj.event_set.all()]
        return events        



class AttendanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Attendance
        fields = '__all__'
        depth = 2
