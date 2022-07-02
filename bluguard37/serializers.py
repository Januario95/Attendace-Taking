from rest_framework import serializers

from .models import (
    TableDevice, TblAlertCode, TblDeviceRawLength,
    TblGateway, TableAlert, TableQuarantine,
    TableAllDevices
)


class TableAllDevicesSerializer(serializers.ModelSerializer):
    class Meta:
        model = TableAllDevices
        fields = '__all__'


class TableQuarantineSerializer(serializers.ModelSerializer):
    class Meta:
        model = TableQuarantine
        fields = '__all__'


class TableDeviceSerializer(serializers.ModelSerializer):
    class Meta:
        model = TableDevice
        fields = '__all__'


class TblAlertCodeSerializer(serializers.ModelSerializer):
    class Meta:
        model = TblAlertCode
        fields = '__all__'


class TblDeviceRawLengthSerializer(serializers.ModelSerializer):
    class Meta:
        model = TblDeviceRawLength
        fields = '__all__'


class TblGatewaySerializer(serializers.ModelSerializer):
    class Meta:
        model = TblGateway
        fields = '__all__'


class TableAlertSerializer(serializers.ModelSerializer):
    class Meta:
        model = TableAlert
        fields = '__all__'
        depth = 2
