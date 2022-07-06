import mysql.connector as mysql
from django.contrib.auth.models import User
from django.http import JsonResponse
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import api_view, renderer_classes
from rest_framework.renderers import JSONRenderer, BrowsableAPIRenderer

import json
from datetime import datetime, timedelta

from ..models import (
    Event, Attendee, Attendance, TableBeacon
)
from bluguard37.models import (
    TableDevice, TableAllDevices, TblGateway,
    ScriptStatus
)
from ..serializers import (
    EventSerializer, AttendeeSerializer,
    AttendanceSerializer, BeaconSerializer
)
from bluguard37.serializers import (
    TableDeviceSerializer
)


def default(obj):
    if isinstance(obj, datetime):
        return obj.isoformat()
    return obj


@api_view(['GET', ])
@renderer_classes([JSONRenderer])
@renderer_classes([BrowsableAPIRenderer])
def get_event_name(request, event_id):
    event = Event.objects.filter(id=event_id)
    event_name = 'Not exist'
    if event.exists():
        event = event.first()
        event_name = event.event_name

    return Response({
        'event_name': event_name
    })


@api_view(['GET', ])
@renderer_classes([JSONRenderer])
@renderer_classes([BrowsableAPIRenderer])
def check_out_attendance(request, attendance_id, check_out_date, check_out_time):
    attendance = Attendance.objects.filter(id=attendance_id)
    updated = False
    if attendance.exists():
        attendance = attendance.first()
        attendance.check_out_date = check_out_date
        attendance.check_out_time = check_out_time
        attendance.save()
        updated = True

    return Response({
        'updated': updated
    })


@api_view(['GET', ])
@renderer_classes([JSONRenderer])
@renderer_classes([BrowsableAPIRenderer])
def search_attendance(requet, attendee_name, check_in_date, check_in_time):
    attendance = Attendance.objects.filter(
        attendee_name=attendee_name,
        check_in_date=check_in_date,
        check_in_time=check_in_time
    )
    if attendance.exists():
        exists = True
        attendance = attendance.first().serialize()
    else:
        exists = False
        attendance = {}

    return Response({
        'exists': exists,
        'attendance': attendance
    })


@api_view(['GET', ])
@renderer_classes([JSONRenderer])
@renderer_classes([BrowsableAPIRenderer])
def search_attendee_by_id(request, attendee_id):
    try:
        attendee = Attendee.objects.filter(id=attendee_id)
        attendee = attendee.first()
        attendence = Attendance.objects.create(attendee=attendee)
        created = True
    except:
        created = False

    return Response({
        'created': created
    })


@api_view(['GET', ])
@renderer_classes([JSONRenderer])
@renderer_classes([BrowsableAPIRenderer])
def search_device_mac(request, device_mac):
    device = TableDevice.objects.filter(device_mac=device_mac)
    if device.exists():
        device = device.first()
        device_mac = device.device_mac
    else:
        device_mac = None

    return Response({
        'device_mac': device_mac
    })



@api_view(['GET', ])
@renderer_classes([JSONRenderer])
@renderer_classes([BrowsableAPIRenderer])
def get_attendance_by_attendee_id(request, attendee_id):
    clear_checks = False
    attendee = Attendee.objects.filter(id=attendee_id)
    if attendee.exists():
        attendee = attendee.first()
        attendance = Attendance.objects.filter(
            attendee=attendee
        )
        if attendance.exists():
            attendance = attendance.last()
            if attendance.check_out_date is not None:
                clear_checks = True

    return Response({
        'clear_checks': clear_checks
    })


@api_view(['GET', ])
@renderer_classes([JSONRenderer])
@renderer_classes([BrowsableAPIRenderer])
def update_attendance(request, attendee,
                      check_in_date, check_in_time,
                      check_out_date, check_out_time):
    # check_out_date = datetime.strptime(check_out_date, '%Y-%m-%d')
    # check_out_time = datetime.strptime(check_out_time, '%H:%M:%S.%f')
    attendee = Attendee.objects.filter(attendee_name=attendee)
    exists = False
    if attendee.exists():
        print('ATTENDEE exists')
        attendee = attendee.first()
        print(f'attendee = {attendee}')
        event_name = attendee.event.event_name
        attendance = Attendance.objects.filter(
            attendee=attendee
            # check_in_date=check_in_date,
            # check_in_time=check_in_time
        )
        print(f'attendance = {attendance}')
        if attendance.exists():
            print('ATTENDANCE exists')
            exists = True
            attendance = attendance.last()
            print(f'check_out_date = {check_out_date}')
            print(f'check_out_time = {check_out_time}')
            attendance.check_out_date = check_out_date
            attendance.check_out_time = check_out_time
            attendance.save()
            print('Attendance checked-out successfully!')
        else:
            print('ATTENDANCE does not exists')
    else:
        attendee = {}
        print('ATTENDEE does not exists')

    return Response({
        'exists': exists,
        'attendee': 'attendee'
    })


def set_events_for_attendances(active_event, event):
    attendees = Attendee.objects.all()
    for att in attendees:
        att.event = event
        att.save()


@api_view(['GET', ])
@renderer_classes([JSONRenderer])
@renderer_classes([BrowsableAPIRenderer])
def set_event_active_inactive(request,
                              event_id, event_name):
    event = Event.objects.filter(
        id=event_id
    )
    exists = False
    active_event = None
    if event.exists():
        event = event.first()
        if event.active_event == True:
            event.active_event = False
            active_event = False
            event.save()
        else:
            event.active_event = True
            active_event = True
            event.save()
            set_events_for_attendances(active_event, event)

        event = event.serialize()
        exists = True
    else:
        event = {}

    return Response({
        'event': event,
        'exists': exists,
        'event_name': event_name,
        'active_event': active_event,
    })


@api_view(['GET', ])
@renderer_classes([JSONRenderer])
@renderer_classes([BrowsableAPIRenderer])
def create_attendance(request, tag_id, event_id,
                      check_in_date, check_in_time):

    event = Event.objects.filter(
        id=event_id
    )
    exists = False
    print('GETTING...')
    attendee = Attendee.objects.filter(
        tag_id=tag_id
    )
    if attendee.exists():
        attendee = attendee.first()
        print(f'attendee check_in_date = {attendee.check_in_date}')
        if attendee.check_in_date is not None and attendee.check_out_date is None:
            event_name = attendee.event.event_name
            attendance = Attendance.objects.create(
                attendee=attendee,
                check_in_date=check_in_date,
                check_in_time=check_in_time,
                # check_out_date=check_out_date,
                # check_out_time=check_out_time
            )
            attendance.save()
            print('Attendance taken successfully!')
            exists = True

    # if event.exists():
    #     event = event.first()
    #     print(f'event = {event}')
    #     attendee = Attendee.objects.filter(
    #         event=event
    #     )
    #     if attendee.exists():
    #         attendee = attendee.first()
    #         print(f'attendee check_in_date = {attendee.check_in_date}')
    #         if attendee.check_in_date is None:
    #             event_name = attendee.event.event_name
    #             attendance = Attendance.objects.create(
    #                 attendee=attendee,
    #                 check_in_date=check_in_date,
    #                 check_in_time=check_in_time,
    #                 # check_out_date=check_out_date,
    #                 # check_out_time=check_out_time
    #             )
    #             attendance.save()
    #             print('Attendance taken successfully!')
    #             exists = True
        # else:
        #     attendee = Attendee.objects.filter(attendee_name=attendee)
        #     if attendee.exists():
        #         attendee = attendee.first()
        #         event_name = attendee.event.event_name
        #         attendance = Attendance.objects.create(
        #             attendee=attendee,
        #             check_in_date=check_in_date,
        #             check_in_time=check_in_time,
        #             # check_out_date=check_out_date,
        #             # check_out_time=check_out_time
        #         )
        #         attendance.save()
        #         print('Attendance taken successfully!')
        #         exists = True

    # attendee = Attendee.objects.filter(attendee_name=attendee)
    # if attendee.exists():
    #     attendee = attendee.first()
    #     event_name = attendee.event.event_name
    #     attendance = Attendance.objects.create(
    #         attendee=attendee,
    #         check_in_date=check_in_date,
    #         check_in_time=check_in_time,
    #         # check_out_date=check_out_date,
    #         # check_out_time=check_out_time
    #     )
    #     attendance.save()
        # print('Attendance taken successfully!')
        # exists = True
    else:
        attendee = {}
        exists = False

    return Response({
        'exists': exists,
        'attendee': 'attendee'  # attendee
    })



@api_view(['GET', ])
@renderer_classes([JSONRenderer])
@renderer_classes([BrowsableAPIRenderer])
def checkout_attendance(request):
    attendances = Attendance.objects.all()
    for att in attendances:
        event_name = att.event_name
        attendee = Attendee.objects.filter(
            attendee_name=att.attendee
        )
        if attendee.exists():
            attendee = attendee.first()
            if attendee.is_online:
                last_updated = attendee.last_updated
                now = datetime.now()
                time_diff = now - last_updated
                secs_delay = timedelta(seconds=15)
                if time_diff > secs_delay:
                    attendee.is_online = False
                    attendee.save()
                    now = datetime.now()
                    date = now.date()
                    time = now.time()
                    att.check_out_date = date
                    att.check_out_time = time
                    att.save()
                    print(f'{att} checked out')

    return Response({
        'status': 'Checking-out'
    })




@api_view(['POST', ])
@renderer_classes([JSONRenderer])
@renderer_classes([BrowsableAPIRenderer])
def create_attendance_by_attendee_id(request):
    data = json.loads(request.body)
    attendee_id = data['attendee_id']
    event_id = data['event_id']
    # print(data)

    timestamp = datetime.now()
    date = timestamp.date()
    time = timestamp.time()

    attendee = Attendee.objects.filter(
        id=attendee_id
    )
    event = Event.objects.filter(
        id=event_id
    )
    if event.exists():
        event = event.first()
        event_name = event.event_name

    if attendee.exists():
        attendee = attendee.first()
        attendee.is_online = True
        attendee.last_updated = timestamp
        attendee.save()

        attendee_name = attendee.attendee_name
        attendance = Attendance.objects.filter(
            attendee=attendee_name,
            # event_name=event_name
        )
        if attendance.exists():
            attendance = attendance.last()
            print(f'check_out_time = {attendance.check_out_time}')
            if attendance.check_out_date is not None:
                print(f'check_out_date = {attendance.check_out_date}')
                if attendance.event_name != event_name:
                    attendance = Attendance.objects.create(
                        attendee=attendee_name,
                        event_name=event_name,
                        check_in_date=date,
                        check_in_time=time
                    )
                    attendance.save()
                    print(f'{attendee_name} attending different Event "{event_name}"')
                             
        else:
            attendance = Attendance.objects.create(
                attendee=attendee.attendee_name,
                event_name=event_name,
                check_in_date=date,
                check_in_time=time
            )
            attendance.save()
            print(f'\nAttendance taken for {attendee.attendee_name} for EVENT {event_name}\n')    
        

    return Response({
        'created': data
    })





@api_view(['GET', ])
@renderer_classes([JSONRenderer])
@renderer_classes([BrowsableAPIRenderer])
def search_attended_by_gatewaymac(request, tag_id):
    attendee = Attendee.objects.filter(tag_id=tag_id)
    if not attendee.exists():
        attendee = []
    else:
        attendee = attendee.first()
        # event = Event.objects.filter(
        #     attendee=attendee
        # )
        events = [obj.serialize() for obj in attendee.event_set.all()]               
        attendee = attendee.serialize()
        attendee['events'] = events

    script = ScriptStatus.objects.filter(
        name='Process_Attendance'
    )
    if script.exists():
        script = script.first()
        script.status = 'ONLINE'
        script.save()

    return JsonResponse({
        'attendee': attendee,
    })



@api_view(['GET', ])
@renderer_classes([JSONRenderer])
@renderer_classes([BrowsableAPIRenderer])
def get_event_by_attendee_id(request, attendee_id):
    attendee = Attendee.objects.filter(id=attendee_id)
    if attendee.exists():
        attendee = attendee.first()
        events = attendee.event_set.all()
        events = events.serialize()
    else:
        events = []
    
    return Response({
        'events': events
    })

@api_view(['GET', ])
@renderer_classes([JSONRenderer])
@renderer_classes([BrowsableAPIRenderer])
def get_event_attendee(request, event_id):
    attendees = [] #Attendee.objects.filter(event__id=event_id)
    event = Event.objects.filter(id=event_id)
    if not event.exists():
    # if not event.exist():
        attendees = []
    else:
        data = []
        event = event.first()
        attendees = event.attendee.all()
        for att in attendees:
            row = att.serialize()
            row['event_id'] = event_id
            attendances = Attendance.objects.filter(
                attendee=att.attendee_name,
                event_name=event.event_name
            )
            if attendances.exists():
                row_attendance = []
                for attendance in attendances:
                    row_attendance.append(attendance.serialize())
                row['attendance'] = row_attendance
            print(row)
            print('\n')
                
            data.append(row)

        attendees = attendees.serialize()
        attendees = data
        # print(data)

    return JsonResponse({
        'attendees': attendees
    })


@api_view(['GET', ])
@renderer_classes([JSONRenderer])
@renderer_classes([BrowsableAPIRenderer])
def delete_event(request, event_id):
    event = Event.objects.filter(pk=event_id)
    if event.exists():
        event = event.first()
        event.delete()
        deleted = True
    else:
        deleted = False

    return JsonResponse({
        'deleted': deleted
    })


def set_online_to_offline(table):
    data = []
    for device in table:
        last_read_date = device.last_read_date
        last_read_time = str(device.last_read_time)
        if last_read_date is None:
            pass
        else:
            last_read_time = last_read_time.split('.')[0]
            date_time = f'{last_read_date} {last_read_time}'
            date_time = datetime.strptime(date_time, "%Y-%m-%d %H:%M:%S")
            now = datetime.now()
            time_diff = now - date_time

            row = {}
            if device.device_status == 'ONLINE':
                if time_diff.seconds > 8:
                    device.device_status = 'OFFLINE'
                    device.save()
                    row['device_mac'] = device.device_mac
                    row['device_status'] = device.device_status
                    data.append(row)

    return data


@ api_view(['GET', ])
@ renderer_classes([JSONRenderer])
@ renderer_classes([BrowsableAPIRenderer])
def delete_all_attendance_by_event(request, event_id):
    print(f'event_id = {event_id}')
    event = Event.objects.filter(id=event_id)
    deleted = False
    if event.exists():
        event = event.first()
        print('EVENT exists')
        print(f'EVENT = {event}')
        attendees = Attendee.objects.filter(
            event=event
        )
        if attendees.exists():
            for att in attendees:
                attendee = att  # attendee.first()
                print('ATTENDEE exists')
                print(f'ATTENDEE = {attendee}')
                attendances = Attendance.objects.filter(
                    attendee=attendee
                )
                print(attendances)
                if attendances.exists():
                    print('ATTENDANCE exists')
                    for att in attendances:
                        att.delete()
                        deleted = True

    return Response({
        'deleted': deleted
    })


@ api_view(['GET', ])
@ renderer_classes([JSONRenderer])
@ renderer_classes([BrowsableAPIRenderer])
def delete_all_attendance(request):
    attendences = Attendance.objects.all()
    for att in attendences:
        att.delete()

    return Response({
        'deleted': True
    })


@ api_view(['GET', ])
@ renderer_classes([JSONRenderer])
@ renderer_classes([BrowsableAPIRenderer])
def set_device_offline_online(request):
    script = ScriptStatus.objects.filter(
        name='Process Devices data'
    )
    if script.exists():
        script = script.first()
        script.status = 'OFFLINE'
        script.save()

    script = ScriptStatus.objects.filter(
        name='Process_Attendance'
    )
    if script.exists():
        script = script.first()
        script.status = 'OFFLINE'
        script.save()

    script = ScriptStatus.objects.filter(
        name='Clear_checks'
    )
    if script.exists():
        script = script.first()
        script.status = 'ONLINE'
        script.save()

    devices = TableDevice.objects.all()
    alltables = TableAllDevices.objects.all()
    data = set_online_to_offline(devices)
    new_data = set_online_to_offline(alltables)
    gateways = TblGateway.objects.all()
    for gateway in gateways:
        if gateway.gateway_status == 'ONLINE':
            gateway.gateway_status = 'OFFLINE'
            gateway.save()

    # data = []
    # for device in devices:
    #     last_read_date = device.last_read_date
    #     last_read_time = str(device.last_read_time)
    #     last_read_time = last_read_time.split('.')[0]
    #     date_time = f'{last_read_date} {last_read_time}'
    #     date_time = datetime.strptime(date_time, "%Y-%m-%d %H:%M:%S")
    #     now = datetime.now()
    #     time_diff = now - date_time

    #     row = {}
    #     if device.device_status == 'ONLINE':
    #         if time_diff.seconds > 6:
    #             device.device_status = 'OFFLINE'
    #             device.save()
    #             row['device_mac'] = device.device_mac
    #             row['device_status'] = device.device_status
    #             data.append(row)

    return Response({
        'data': data
    })


class TableBeaconViewSet(ModelViewSet):
    queryset = TableBeacon.objects.all()
    serializer_class = BeaconSerializer


class TableDeviceViewSet(ModelViewSet):
    queryset = TableDevice.objects.all()
    serializer_class = TableDeviceSerializer


class EventViewSet(ModelViewSet):
    queryset = Event.objects.all()
    serializer_class = EventSerializer


class AttendeeViewSet(ModelViewSet):
    queryset = Attendee.objects.all()
    serializer_class = AttendeeSerializer


class AttendanceViewSet(ModelViewSet):
    queryset = Attendance.objects.all()
    serializer_class = AttendanceSerializer


config = {
    'user': 'attendance4',
    'password': 'AskPermission2022!',
    'database': 'bluguarddb',
    'host': 'attendance4.mysql.database.azure.com',
    'port': 3306,
    'ssl_disabled': False,
    'raise_on_warnings': True,
    'ssl_ca': '/SSL/DigiCertGlobalRootCA.crt.pem'

    # 'user': 'attendance2',
    # 'password': 'AskPermission2022!',
    # 'database': 'bluguarddb',
    # 'host': 'attendance2.mysql.database.azure.com',
    # 'port': 3306,
    # 'ssl_disabled': True,

    # 'host': 'localhost',
    # 'user': 'januario95',
    # 'password': 'Jaci1995',
    # 'database': 'bluguarddb',
    # 'port': 3306
}
# cnx = mysql.connector.connect(user="attendance", password="{your_password}", host="attendance1.mysql.database.azure.com", port=3306, database="{your_database}", ssl_ca="{ca-cert filename}", ssl_disabled=False)


def dictfetchall(cursor):
    columns = [col[0] for col in cursor.description]
    return [
        dict(zip(columns, row)) for row in cursor.fetchall()
    ]


# Connector = mysql.connect(**config)
# Cursor = Connector.cursor()

Connector = ''
Cursor = ''


@api_view(['GET', ])
@renderer_classes([JSONRenderer])
def Attendee_List_All(request):
    global Connector, Cursor

    # Query all attendees  from TBL_Attendee
    query = '''
        SELECT * FROM TBL_Attendee
    '''
    Cursor.execute(query)
    results = dictfetchall(Cursor)

    return Response({
        'attendees': results
    })


@api_view(['GET', ])
@renderer_classes([JSONRenderer])
def Attendee_List(request, Event_ID):
    global Connector, Cursor

    # Query all attendees  from TBL_Attendee filtered by the Event_ID
    query = '''
        SELECT * FROM TBL_Attendee
            WHERE Event_ID = %s
    '''
    parameter = (Event_ID,)
    Cursor.execute(query, parameter)
    results = dictfetchall(Cursor)

    return Response({
        'attendees': results
    })


@api_view(['GET', ])
@renderer_classes([JSONRenderer])
def Event_List(request):
    global Connector, Cursor

    # Query all events from TBL_Evet
    query = 'SELECT * FROM TBL_Event'
    Cursor.execute(query)
    results = dictfetchall(Cursor)
    for row in results:
        Event_ID = row['Event_ID']
        query = '''
            SELECT * FROM TBL_Attendee
                WHERE Event_ID = %s
        '''
        parameter = (Event_ID,)
        Cursor.execute(query, parameter)
        results_ = dictfetchall(Cursor)
        row['Attendees'] = results_
        del row['Event_ID']

    return Response({
        'events': results
    })


@api_view(['GET', ])
@renderer_classes([JSONRenderer])
def index(request):
    # global Connector, Cursor
    # query = '''
    # SELECT
    #     Device_Status, Device_Temp, Device_O2, Device_Bat_Level,
    #     Device_HR, Device_Last_Updated_Date, Device_Last_Updated_Time,
    #     Device_Tag, Device_Mac, Device_Status
    # FROM
    #     TBL_Device
    # WHERE
    #     Device_Type <> %s
    # ORDER BY Device_Tag;
    # '''
    # parameter = ('HSWB004', )
    # Cursor.execute(query, parameter)
    # results = dictfetchall(Cursor)
    # print(len(results))
    # for row in results:
    #     device_assignment = row['Device_Status']
    #     device_temp = row['Device_Temp']
    #     device_o2 = row['Device_O2']
    #     device_bat = row['Device_Bat_Level']
    #     device_hr = row['Device_HR']
    #     last_read_date = row['Device_Last_Updated_Date']
    #     last_read_time = row['Device_Last_Updated_Time']
    #     device_tag = row['Device_Tag']
    #     device_mac = row['Device_Mac']
    #     device_status = row['Device_Status']
    #     last_read_date = last_read_date if last_read_date is not None else '2022-06-19'
    #     last_read_time = last_read_time if last_read_time is not None else '02:52:30'

    #     device = TableDevice.objects.create(
    #         device_tag=device_tag,
    #         device_mac=device_mac,
    #         device_status=device_status,
    #         device_assignment=device_assignment,
    #         device_temp=device_temp,
    #         device_o2=device_o2,
    #         device_bat=device_bat,
    #         device_hr=device_hr,
    #         last_read_date=str(last_read_date),
    #         last_read_time=str(last_read_time)
    #     )
    #     device.save()

    return Response({
        'data': 'Yes'
    })


@api_view(['GET'])
@renderer_classes([JSONRenderer])
def update_user_info(request, username, email):
    is_updated = False
    old_email = ''
    user = User.objects.filter(username=username)
    if user.exists():
        user = user.first()
        old_email = user.email
        user.email = email
        user.save()
        is_updated = True

    if is_updated:
        data = {
            'old_email': old_email,
            'new_email': user.email
        }
    else:
        data = {
            'is_updated': is_updated
        }

    return Response(data)


@api_view(['GET'])
@renderer_classes([JSONRenderer])
def top_five_alerts_api(request):
    global Connector, Cursor

    # def format_time(time):
    # 	date_, time_ = str(time).split('T')
    # 	time_ = time_.split('.')
    # 	datetime_ = date_ + ' ' + time_[0]
    # 	return datetime_

    query = '''
        SELECT Alert_Datetime, Device_ID, Alert_Reading, Alert_Code
        FROM tbl_alert ORDER BY Alert_Datetime DESC LIMIT 5;
    '''
    Cursor.execute(query)

    results = Cursor.fetchall()
    # print(results)

    data = [
        {
            'Alert_Datetime': f'{row[0].date()} {row[0].time()}',
            'Device_ID': row[1],
            'Device_Temp': row[2],
            'Alert_Code': row[3]
        } for row in results
    ]
    for row in data:
        query = '''
    		SELECT Alert_Description FROM TBL_Alert_Code
    		WHERE Alert_Code = %s
    	'''
        Alert_Code = row['Alert_Code']
        parameter = (Alert_Code,)
        Cursor.execute(query, parameter)
        results = dictfetchall(Cursor)
        row['Alert_Description'] = results[0]['Alert_Description']

        if row['Alert_Code'] == '1':
            row['vital_icon'] = 'Alert_Icons_Latest/temp_high_alert.png'
        elif row['Alert_Code'] == '2':
            row['vital_icon'] = 'Alert_Icons_Latest/temp_high_alert.png'
        elif row['Alert_Code'] == '3':
            row['vital_icon'] = 'Alert_Icons_Latest/High_O2-removebg.png'
        elif row['Alert_Code'] == '4':
            row['vital_icon'] = 'Alert_Icons_Latest/High_O2-removebg.png'
        elif row['Alert_Code'] == '5':
            row['vital_icon'] = 'Alert_Icons_Latest/High_HR-removebg.png'
        elif row['Alert_Code'] == '6':
            row['vital_icon'] = 'Alert_Icons_Latest/High_HR-removebg.png'
        elif row['Alert_Code'] == '7':
            row['vital_icon'] = 'Alert_Icons_Latest/BatLevel.jpeg'

        row['device_icon'] = 'Alert_Icons_Latest/device_icon.png'

        Device_ID = row['Device_ID']
        query = '''
    	SELECT Wearer_ID FROM tbl_device
    	WHERE Device_ID = %s
    	'''
        parameter = (Device_ID,)
        Cursor.execute(query, parameter)
        Fetch_Results = Cursor.fetchall()

        try:
            Wearer_ID = Fetch_Results[0][0]
            query = '''
    			SELECT Wearer_Nick FROM tbl_wearer
    			WHERE Wearer_ID = %s
    		'''
            parameter = (Wearer_ID,)
            Cursor.execute(query, parameter)
            Fetch_Result = Cursor.fetchall()
            Wearer_Nick = Fetch_Result[0][0]
            row['Wearer_Nick'] = Wearer_Nick
        except LookupError:
            pass

    return Response({
        'alerts': data
    })


@api_view(['GET'])
@renderer_classes([JSONRenderer])
def fetch_user_info(request):
    user = User.objects.filter(username='hayysoft')
    if user.exists():
        user = user.first()
        data = {
            'username': user.username,
            'email': user.email
        }
    else:
        data = {}

    return Response(data)


@api_view(['GET'])
@renderer_classes([JSONRenderer])
def Online_Gateways_API(request):
    global Connector, Cursor

    query = '''
	SELECT Gateway_Status, Gateway_Location, Gateway_Mac, Gateway_Serial_No, Last_Updated_Time
	FROM TBL_Gateway
	'''
    Cursor.execute(query)
    results = dictfetchall(Cursor)

    for row in results:
        Gateway_Mac = row['Gateway_Mac']
        query = """
			SELECT COUNT(*) AS Total_Alerts FROM TBL_Alert
				WHERE Device_ID IN (
					SELECT Device_ID FROM TBL_Device
						WHERE Gateway_Mac IN (
							SELECT Gateway_Mac FROM TBL_Gateway
								WHERE Gateway_Mac = %s
			            )
			    );
		"""
        parameter = (Gateway_Mac, )
        Cursor.execute(query, parameter)
        res = dictfetchall(Cursor)
        try:
            row.update({'Total_Alerts': res[0]['Total_Alerts']})
        except:
            row.update({'Total_Alerts': 0})

    return Response({
        'online_gateways': results
    })


@api_view(['GET'])
@renderer_classes([JSONRenderer])
def Quanrantine_Surveillance_Data(request):
    global Connector, Cursor

    query = '''
    SELECT
        Device_Status, Device_ID, Device_Last_Updated_Time,
        Device_Last_Updated_Date, Wearer_ID, Device_Tag
    FROM
        TBL_Device
    WHERE
        Device_Type = %s
    ORDER BY Device_Tag;
    '''
    parameter = ('HSWB004', )
    Cursor.execute(query, parameter)

    results = Cursor.fetchall()
    data = [
        {
            'Device_Status': row[0],
            'Device_ID': row[1],
            'Device_Last_Updated_Time': row[2],
            'Device_Last_Updated_Date': row[3],
            'Wearer_ID': row[4],
            'Device_Tag': row[5]
        } for row in results
    ]

    for row in range(len(data)):
        Device_ID = data[row]['Device_ID']
        Wearer_ID = data[row]['Wearer_ID']

        query = '''
			SELECT * FROM TBL_Crest_Patient
			WHERE Patient_Discharged = %s AND Q_Device_ID = %s
		'''
        parameters = (0, 'NA')
        Cursor.execute(query, parameters)
        results = dictfetchall(Cursor)
        data[row][f'Patient_Tag'] = results

        query = '''
			SELECT Patient_Tag FROM TBL_Crest_Patient
			WHERE Q_Device_ID = %s AND
				  Wearer_ID IN (
				  	SELECT Wearer_ID FROM TBL_Wearer
				  	WHERE Status = %s
				)
		'''
        parameter = (Device_ID, 'Assigned')
        Cursor.execute(query, parameter)
        Patient_Tag_Row = dictfetchall(Cursor)
        data[row]['Patient_Tag_Row'] = Patient_Tag_Row

        data[row]['Breach_Link'] = f"/invidual_quarantine/{Wearer_ID}/"
        data[row]['Assign_Unassign'] = f"/set_to_assigned_unassigned/{Wearer_ID}/"
        data[row]['set_Q_Device_and_Q_End'] = f"/set_Q_Device_and_Q_End/?Device_ID={Device_ID}&Wearer_ID={Wearer_ID}&Patient_Tag={'Patient_Tag'}"
        data[row]['set_Q_Device_and_Q_Start'] = f"/set_Q_Device_and_Q_Start/?Device_ID={Device_ID}&Wearer_ID={Wearer_ID}&Patient_Tag={'Patient_Tag'}"

        query = '''
			SELECT Status, Patient_Tag_Status FROM TBL_Wearer
			WHERE Wearer_ID = %s
		'''
        parameter = (Wearer_ID,)
        Cursor.execute(query, parameter)
        results = dictfetchall(Cursor)
        Status = results[0]['Status']
        data[row]['Patient_Tag_Status'] = results[0]['Patient_Tag_Status']

        if results[0].get('Status') == 'Unassigned':
            data[row]['Assigned'] = False
            data[row]['Background'] = 'green-bg'
        elif results[0].get('Status') == 'Assigned':
            data[row]['Assigned'] = True
            data[row]['Background'] = 'red-bg'

        query = '''
			SELECT Wearer_Nick FROM tbl_wearer
			WHERE Wearer_ID IN (
				SELECT Wearer_ID FROM TBL_Device
				WHERE Wearer_ID = %s
			)
		'''
        parameter = (Wearer_ID,)
        Cursor.execute(query, parameter)
        results = Cursor.fetchall()
        try:
            Wearer_Nick = results[0][0]
            data[row]['Wearer_Nick'] = Wearer_Nick
        except Exception:
            pass

        query = '''
			SELECT Alert_ID FROM TBL_Alert
			WHERE Device_ID IN (
				SELECT Device_ID FROM TBL_Device
				WHERE Device_ID = %s
			)
		'''
        parameter = (Device_ID,)
        Cursor.execute(query, parameter)
        results = Cursor.fetchall()
        try:
            Alert_ID = results[0][0]
            data[row]['Alert_ID'] = Alert_ID
        except Exception:
            pass

        query = '''
			SELECT Quarantine_Start_Date, Quarantine_End_Date FROM TBL_Quarantine
			WHERE Wearer_ID IN (
				SELECT Wearer_ID FROM TBL_Device
				WHERE Wearer_ID = %s
			)
		'''
        parameter = (Wearer_ID,)
        Cursor.execute(query, parameter)
        results = Cursor.fetchall()
        try:
            Quarantine_Start_Date = results[0][0]
            Quarantine_End_Date = results[0][1]
            data[row]['Quarantine_Start_Date'] = Quarantine_Start_Date
            data[row]['Quarantine_End_Date'] = Quarantine_End_Date
            Time_Diff = Quarantine_End_Date - Quarantine_Start_Date
            data[row]['Time_Diff'] = f'{Time_Diff}'
        except Exception:
            pass

    return Response({
        'surveillance': data
    })


@api_view(['GET'])
@renderer_classes([JSONRenderer])
def Lastest_Device_Data(request):
    global Connector, Cursor

    query = '''
		SELECT
	        Device_ID AS Device_ID,
	        Wearer_ID AS Wearer_ID,
	        Device_Temp AS Device_Temp,
	        Device_HR AS Device_HR,
	        Device_O2 AS Device_O2,
	        Device_Last_Updated_Date AS Device_Last_Updated_Date,
	        Device_Last_Updated_Time AS Device_Last_Updated_Time,
	        Incorrect_Data_Flag AS Incorrect_Data_Flag,
	        Device_Status AS Device_Status,
	        Device_Mac AS Device_Mac,
	        Device_Bat_Level AS Device_Bat_Level,
	        Device_Tag AS Device_Tag
	    FROM
	    	TBL_Device
	    WHERE
	        Device_Type <> %s
	    ORDER BY Device_Tag;
	'''
    parameter = ('HSWB004', )
    Cursor.execute(query, parameter)

    devices = Cursor.fetchall()

    devices_data = []
    for row in devices:
        # files = get_individual_files()
        try:
            # [filename for filename in files if filename == row[9]][0]
            file = None
            Device_Mac_Link = f'/device_json_display/{row[9]}/'
            Is_Link = True
        except IndexError:
            file = None
            Device_Mac_Link = '#'
            Is_Link = False

        def default(obj): return obj.isoformat(
        ) if isinstance(obj, datetime) else obj
        row_data = {
            'Device_ID': row[0],
            'Wearer_ID': row[1],
            'Device_Temp': row[2],
            'Device_HR': row[3],
            'Device_O2': row[4],
            'Device_Last_Updated_Date': row[5],
            'Device_Last_Updated_Time': row[6],
            'Incorrect_Data_Flag': row[7],
            'Device_Status': row[8],
            'Device_Mac': row[9],
            'Device_Bat_Level': row[10],
            'Device_Tag': row[11],
            'Device_Mac_Link': Device_Mac_Link,
            'Is_Link': Is_Link
        }
        devices_data.append(row_data)

    for row in devices_data:
        Wearer_ID = row['Wearer_ID']
        query = '''
			SELECT Status FROM TBL_Wearer
			WHERE Wearer_ID = %s
		'''
        parameter = (Wearer_ID,)
        Cursor.execute(query, parameter)
        results = dictfetchall(Cursor)

        try:
            Status = results[0]['Status']
            row['Status'] = Status
        except LookupError:
            pass

    return Response({
        'lastest': devices_data
    })
