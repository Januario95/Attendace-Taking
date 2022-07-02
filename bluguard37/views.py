from datetime import datetime
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import api_view, renderer_classes
from rest_framework.renderers import JSONRenderer, BrowsableAPIRenderer

import json
import datetime as dt
from datetime import datetime

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


def Insert_Alert(alert_code, value, device_id):
    alert_code = int(alert_code)
    alert_code_instance = TblAlertCode.objects.get(
        alert_code=alert_code
    )
    device = TableDevice.objects.get(
        device_mac=device_id)
    alert = TableAlert.objects.filter(
        device_id=device,
        alert_code=alert_code_instance
    )
    if alert.exists():
        last = alert.last()
        alert_datetime = last.alert_datetime
        alert_code_ = int(last.alert_code.alert_code)
        alert_reading = last.alert_reading
        now = datetime.now()
        # print(f'new_alert_code = {type(alert_code)}')
        # print(f'old_alert_code = {type(alert_code_)}')
        diff = now - alert_datetime
        if alert_code == alert_code_:
            # print('EQUALS...')
            if diff > dt.timedelta(minutes=1):
                print('MORE THAN 1 MIN')
                alert = TableAlert.objects.create(
                    alert_code=alert_code_instance,
                    alert_reading=value,
                    device_id=device,
                    sent_to_crest=1
                )
                alert.save()
            else:
                print('LESS THAN 1 MIN')
        else:
            alert = TableAlert.objects.create(
                alert_code=alert_code_instance,
                alert_reading=value,
                device_id=device,
                sent_to_crest=1
            )
            alert.save()
            print('NEW Alert created')
    else:
        alert = TableAlert.objects.create(
            alert_code=alert_code_instance,
            alert_reading=value,
            device_id=device,
            sent_to_crest=1
        )
        alert.save()
        print('Non-Existing Alert')

    # if alert_code.exists():
    #     device = device.first()
    # print(alert.alert_datetime)
    # alert_code = alert_code.first()
    # alert = TableAlert.objects.create(
    #     alert_code=alert_code,
    #     alert_reading=value,
    #     device_id=device,
    #     sent_to_crest=1
    # )
    # alert.save()


def Check_Highest_Score(Type, value_attr, device_id):
    # print('HERE')
    value = 0
    alert_code = 0
    # print(f'TYPE = {Type}')
    if Type == 'temp':
        if value_attr > 37:
            value = value_attr
            alert_code = 1
        elif value_attr < 33:
            value = value_attr
            alert_code = 2
    elif Type == 'spo2':
        if value_attr > 100:
            value = value_attr
            alert_code = 3
        elif value_attr < 95:
            value = value_attr
            alert_code = 4
    elif Type == 'heart_rate':
        if value_attr > 100:
            value = value_attr
            alert_code = 5
        elif value_attr < 60:
            value = value_attr
            alert_code = 6
    elif Type == 'batlevel':
        if value_attr < 30:
            value = value_attr
            alert_code = 7

    # print(f'alert_code = {alert_code}')
    if alert_code != 0:
        # print('ALERTS')
        # print(f'alert_code = {alert_code}')
        Insert_Alert(alert_code, value, device_id)
    else:
        print('NOT ALERTS')


def update_all_device_tables(table_type, table, data):
    table.device_temp = data['temp']
    table.device_o2 = data['heart_rate']
    table.device_bat = data['spo2']
    table.device_hr = data['batlevel']
    table.last_read_date = data['date']
    table.last_read_time = data['time']
    table.incorrect_data_flag = data['incorrect_data_flag']
    table.device_status = data['device_status']
    table.save()

    if table_type == 'device':
        # Check_Highest_Score(
        #     'temp', table.device_temp, "FEFDD727C6F5")
        pass
        # Check_Highest_Score(
        #     'temp', table.device_temp, table.device_mac)
        # Check_Highest_Score(
        #     'heart_rate', table.device_o2, table.device_mac)
        # Check_Highest_Score(
        #     'spo2', table.device_bat, table.device_mac)
        # Check_Highest_Score(
        #     'batlevel', table.device_hr, table.device_mac)


@api_view(['GET', ])
@renderer_classes([JSONRenderer])
@renderer_classes([BrowsableAPIRenderer])
def get_all_alerts(request):
    alerts = TableAlert.objects.all()
    alerts = alerts.order_by('-id')

    return Response({
        'alerts': alerts.serialize()
    })


def update_gateway(gateway_mac):
    gateway = TblGateway.objects.filter(
        gateway_mac=gateway_mac
    )
    if gateway.exists():
        gateway = gateway.first()
        gateway.gateway_status = 'ONLINE'
        gateway.save()
        print('Gateways updated successfully!')


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
    gateway_mac = data['gateway_mac']

    # update_gateway(gateway_mac)
    gateway = TblGateway.objects.filter(
        gateway_mac=gateway_mac
    )
    print(f'gateway_mac = {gateway_mac}')
    if gateway.exists():
        gateway = gateway.first()
        gateway.gateway_status = 'ONLINE'
        gateway.save()
        print('Gateways updated successfully!')

    # device_status = data['device_status']
    device = TableDevice.objects.filter(device_mac=device_mac)
    alltables = TableAllDevices.objects.filter(device_mac=device_mac)
    quarantines = TableQuarantine.objects.filter(device_mac=device_mac)
    if device.exists():
        device = device.first()
        update_all_device_tables('device', device, data)
        update_all_device_tables('none', alltables.first(), data)
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
