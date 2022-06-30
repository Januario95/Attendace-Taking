from genericpath import exists
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import api_view, renderer_classes
from rest_framework.renderers import JSONRenderer, BrowsableAPIRenderer

import json

from .models import (
    TableDevice, TblAlertCode, TblDeviceRawLength,
    TblGateway, TableAlert, TableQuarantine,
    TableAllDevices,
)
from .serializers import (
    TableDeviceSerializer, TblAlertCodeSerializer,
    TblDeviceRawLengthSerializer, TblGatewaySerializer,
    TableAlertSerializer, TableQuarantineSerializer,
    TableAllDevicesSerializer,
)


@api_view(['POST', ])
@renderer_classes([JSONRenderer])
@renderer_classes([BrowsableAPIRenderer])
def filter_alert_by_code_and_device_id(request, alert_code, devide_id):
    data = json.loads(request.body)
    alert_code = data['temp']
    devide_id = data['heart_rate']
    alert = TableAlert.objects.filter(
        alert_code=alert_code,
        devide_id=devide_id
    )
    if alert.exists():
        alert = alert.first()
    else:
        alert = {}
    """
        query = '''SELECT TIMEDIFF(CURRENT_TIMESTAMP(), Alert_Datetime) > TIME('00:01:00') AS TIMEDIFF
            FROM TBL_Alert WHERE Alert_Code = %s AND Device_ID = %s AND
                TIMEDIFF(CURRENT_TIMESTAMP(), Alert_Datetime) > TIME('00:00:30');
        '''
        parameters = (Alert_Code, Device_ID)
    """

    return Response({
        'updated': alert
    })


def update_all_device_tables(table, data):
    table.device_temp = data['temp']
    table.device_o2 = data['heart_rate']
    table.device_bat = data['spo2']
    table.device_hr = data['batlevel']
    table.last_read_date = data['date']
    table.last_read_time = data['time']
    table.incorrect_data_flag = data['incorrect_data_flag']
    table.device_status = data['device_status']
    table.save()


@api_view(['POST', ])
@renderer_classes([JSONRenderer])
@renderer_classes([BrowsableAPIRenderer])
def update_device(request):
    data = json.loads(request.body)
    # temp = data['temp']
    # heart_rate = data['heart_rate']
    # spo2 = data['spo2']
    # batlevel = data['batlevel']
    # incorrect_data_flag = data['incorrect_data_flag']
    # date = data['date']
    # time = data['time']
    device_mac = data['device_mac']
    # device_status = data['device_status']
    device = TableDevice.objects.filter(device_mac=device_mac)
    alltables = TableAllDevices.objects.filter(device_mac=device_mac)
    quarantines = TableQuarantine.objects.filter(device_mac=device_mac)
    if device.exists():
        device = device.first()
        update_all_device_tables(device, data)
        update_all_device_tables(alltables.first(), data)
        # update_all_device_tables(quarantines.first(), data)
        # device.device_temp = temp
        # device.device_o2 = spo2
        # device.device_bat = batlevel
        # device.device_hr = heart_rate
        # device.last_read_date = date
        # device.last_read_time = time
        # device.incorrect_data_flag = incorrect_data_flag
        # device.device_status = device_status
        # device.save()
        updated = True
        device = device.serialize()
    else:
        updated = False
        device = {}

    return Response({
        'updated': updated,
        'device': device
    })


@api_view(['GET', ])
@renderer_classes([JSONRenderer])
@renderer_classes([BrowsableAPIRenderer])
def search_device_by_device_mac(request, device_mac):
    device = TableDevice.objects.filter(device_mac=device_mac)
    if device.exists():
        device = device.first().serialize()
        exists = True
    else:
        device = {}
        exists = False

    return Response({
        'device': device,
        'exists': exists
    })


class TableAllDevicesViewSet(ModelViewSet):
    queryset = TableAllDevices.objects.all()
    serializer_class = TableAllDevicesSerializer


class TableQuarantineViewSet(ModelViewSet):
    queryset = TableQuarantine.objects.all()
    serializer_class = TableQuarantineSerializer


class TableDeviceViewSet(ModelViewSet):
    queryset = TableDevice.objects.all()
    serializer_class = TableDeviceSerializer


class TblAlertCodeViewSet(ModelViewSet):
    queryset = TblAlertCode.objects.all()
    serializer_class = TblAlertCodeSerializer


class TblDeviceRawLengthViewSet(ModelViewSet):
    queryset = TblDeviceRawLength.objects.all()
    serializer_class = TblDeviceRawLengthSerializer


class TblGatewayViewSet(ModelViewSet):
    queryset = TblGateway.objects.all()
    serializer_class = TblGatewaySerializer


class TableAlertViewSet(ModelViewSet):
    queryset = TableAlert.objects.all()
    serializer_class = TableAlertSerializer
