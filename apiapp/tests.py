import json
import requests
import datetime as dt
from pytz import timezone
from datetime import datetime
import mysql.connector as mysql
# from .models import TableDevice


def Process_IoTData():
    Token = {
        'dev': {
            'URL': 'http://localhost:8000',
            'token': 'fd8068e77a29c03af33aed4981333cc2c2f6c5ae'
        },
        'prod': {
            'URL': 'https://bluguard-attendance.herokuapp.com',
            'token': '3d7fbc0bc2ea8cb3c5e8afb4a7d289d04880b14f'
        }
    }

    tag_id = 'FEFDD727C6F5'  # data['mac']
    url = f"{Token['dev']['URL']}/search_attended_by_gatewaymac/{tag_id}/"
    res = requests.get(url, headers={
        'Authorization': f"Token {Token['dev']['token']}",
        'Content-Type': 'application/json'
    })
    data_ = res.json()
    print(data_)

    if len(data_['attendee']) != 0:
        event_id = data_['attendee'][0]['event']
        url = f"{Token['dev']['URL']}/get_event_name/{event_id}/"
        res = requests.get(url, headers={
            'Authorization': f"Token {Token['dev']['token']}"
        })
        data = res.json()
        event_name = data['event_name']

        attendee = data_['attendee'][0]
        attendee_id = attendee['id']
        attendee_name = attendee['attendee_name']
        timestamp = datetime.now()
        date = timestamp.date()  # attendee['check_in_date']
        time = timestamp.time()  # attendee['check_in_time']
        check_in_date = attendee['check_in_date']
        check_in_time = attendee['check_in_time']
        # check_out_date = attendee['check_out_date']
        # check_out_time = attendee['check_out_time']
        attendee_id = attendee['id']
        # print(f'attendee = {attendee}')

        data_ = {}
        if check_in_date is None:
            timestamp = datetime.now()
            date = timestamp.date()
            time = timestamp.time()
            data_ = {
                'check_in_date': date,
                'check_in_time': time,
                'is_online': True,
                'last_updated': datetime.now()
            }

            url = f"{Token['dev']['URL']}/create_attendance/{attendee_name}/{date}/{time}/"
            res = requests.get(url, headers={
                'Authorization': f"Token {Token['dev']['token']}",
                'Content-Type': 'application/json'
            })
            d = res.json()
            print(d)
        else:
            data_ = {'last_updated': datetime.now()}

        url = f"{Token['dev']['URL']}/attendee/{attendee_id}/"
        res = requests.patch(url, headers={
            'Authorization': f"Token {Token['dev']['token']}",
        }, data=data_)
        data_ = res.json()


# Process_IoTData()


TOKEN = {
    'dev': {
        'URL': 'http://localhost:8000',
        'token': 'fd8068e77a29c03af33aed4981333cc2c2f6c5ae'
    },
    'prod': {
        'URL': 'https://bluguard-attendance.herokuapp.com',
        'token': '3d7fbc0bc2ea8cb3c5e8afb4a7d289d04880b14f'
    }
}
url = TOKEN['prod']['URL'] + "/get_active_mac_ids/"
token = TOKEN['prod']['token']
headers = {
    'Authorization': f'Token {token}',
    'Content-Type': 'application/json'
}
data = {
    'mac_ids': ['AC233FC092FC', 'AC233F5A9EE9', 'AC233F5E688C', 'AC233F5E688E', 'F108BB3472D6', 'FEFDD727C6F5']
}
res = requests.post(url, headers=headers, data=json.dumps(data))
print(res.json())

# print(json.dumps(res.json(), indent=4))


config = {
    # 'user': 'attendance',
    # 'password': 'AskPermission2022!',
    # 'database': 'bluguarddb',
    # 'host': 'attendance1.mysql.database.azure.com',
    # 'port': 3306,
    # 'ssl_disabled': True

    # 'user': 'attendance3',
    # 'password': 'AskPermission2022!',
    # 'database': 'bluguarddb',
    # 'host': 'attendance3.mysql.database.azure.com',
    # 'port': 3306,
    # 'ssl_disabled': False,
    # 'ssl_ca': '/SSL/DigiCertGlobalRootCA.crt.pem'

    # 'user': 'attendance4',
    # 'password': 'AskPermission2022!',
    # 'database': 'bluguarddb',
    # 'host': 'attendance4.mysql.database.azure.com',
    # 'port': 3306,
    # 'ssl_disabled': False,
    # 'ssl_ca': '/SSL/DigiCertGlobalRootCA.crt.pem'

    'user': 'januario95',
    'password': 'Jaci1995',
    'database': 'bluguarddb',
    'host': 'localhost',
    'port': 3306,
    # 'ssl_disabled': False,
    # 'ssl_ca': '/SSL/DigiCertGlobalRootCA.crt.pem'
}


def dictfetchall(cursor):
    columns = [col[0] for col in cursor.description]
    return [
        dict(zip(columns, row)) for row in cursor.fetchall()
    ]


def default(obj):
    if isinstance(obj, datetime):
        return obj.isoformat()
    return obj


Connector = '' # mysql.connect(**config)
Cursor = '' # Connector.cursor()


# query = '''
#     SELECT * FROM TBL_Device;
# '''
# parameter = ('HSWB004', )
# Cursor.execute(query)  # , parameter)
# results = dictfetchall(Cursor)
# data = []
# fields = [
#     'device_tag', 'device_mac', 'device_type',
#     'device_status', 'device_assignment', 'device_temp',
#     'device_o2', 'device_bat', 'device_hr',
#     'incorrect_data_flag',
#     'last_read_date', 'last_read_time'
# ]
# for row in results:
#     new_row = {}
#     for key, value in row.items():
#         key = key.lower()
#         if key in fields:
#             new_row[key.lower()] = value
#     data.append(new_row)

# data = json.dumps(data, default=default, indent=4)
# print(data)

# with open('all_devices.json', 'w') as f:
#     f.write(data)


# row1 = results[0]
# print(row1)
# Device_Status = row1['Device_Status']
# Device_Temp = row1['Device_Temp']
# Device_O2 = row1['Device_O2']
# Device_Bat_Level = row1['Device_Bat_Level']
# Device_HR = row1['Device_HR']
# Device_Last_Updated_Date = row1['Device_Last_Updated_Date']
# Device_Last_Updated_Time = row1['Device_Last_Updated_Time']
# Device_Tag = row1['Device_Tag']
# Device_Mac = row1['Device_Mac']
# Device_Status = row1['Device_Status']

# for row in results:
#     Device_Status=row['Device_Status']
#     Device_Temp=row['Device_Temp']
#     Device_O2=row['Device_O2']
#     Device_Bat_Level=row['Device_Bat_Level']
#     Device_HR=row['Device_HR']
#     Device_Last_Updated_Date=row['Device_Last_Updated_Date']
#     Device_Last_Updated_Time=row['Device_Last_Updated_Time']
#     Device_Tag=row['Device_Tag']
#     Device_Mac=row['Device_Mac']
#     Device_Status=row['Device_Status']


# tag_id = 'FEFDD727C6F5'
# token = 'fd8068e77a29c03af33aed4981333cc2c2f6c5ae'
# url = f'http://localhost:8000/search_attended_by_gatewaymac/{tag_id}/'
# res = requests.get(url, headers={
#     'Authorization': f'Token {token}',
#     'Content-Type': 'application/json'
# })
# data = res.json()
# # print(data)

# if len(data['attendee']) != 0:
#     attendee = data['attendee']
#     check_in_date = attendee[0]['check_in_date']
#     check_in_time = attendee[0]['check_in_time']
#     check_out_date = attendee[0]['check_out_date']
#     check_out_time = attendee[0]['check_out_time']
#     attendee_id = attendee[0]['id']
#     print(f'check_in_date = {check_in_date}')

#     data = {}
#     if check_in_date is None:
#         timestamp = datetime.now()
#         date = timestamp.date()
#         time = timestamp.time()
#         data = {
#             'check_in_date': date,
#             'check_in_time': time,
#             'is_online': True,
#             'last_updated': datetime.now()  # timezone('Asia/Singapore'))
#         }
#     else:
#         data = {'last_updated': datetime.now()}
#         # timezone('Asia/Singapore'))}

#     url = f'http://localhost:8000/attendee/{attendee_id}/'
#     res = requests.patch(url, headers={
#         'Authorization': f'Token {token}',
#     }, data=data)
#     data = res.json()
#     print(data)


# now = datetime.now()
# data = {
#     'attendee_id': 1,
#     'check_in': now,
#     'check_out': now
# }

# token = 'fd8068e77a29c03af33aed4981333cc2c2f6c5ae'
# url = f'http://localhost:8000/create_attendance/{1}/{now}/{now}/'
# res = requests.get(url, headers={
#     'Authorization': f'Token {token}',
#     'Content-Type': 'application/json'
# })
# print(res.status_code)
# data = res.json()
# print(data)


def attendee_list(event_id):
    global Connector, Cursor

    query = '''
        SELECT * FROM TBL_Attendee
            WHERE Event_ID = %s
    '''
    parameter = (event_id,)
    Cursor.execute(query, parameter)
    results = dictfetchall(Cursor)
    print(json.dumps(results, indent=4, default=default))


# attendee_list('EVENT2022-06-14 10:31:47')


def event():
    global Connector, Cursor

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

        print(json.dumps(row, indent=4, default=default))

# event()


def top_five_alerts_api():
    global Connector, Cursor

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
        results_ = dictfetchall(Cursor)
        row['Alert_Description'] = results_[0]['Alert_Description']

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
            print(f'Fetch_Result = {Fetch_Result}')
            Wearer_Nick = Fetch_Result[0][0]
            row['Wearer_Nick'] = Wearer_Nick
        except LookupError:
            pass

        print(row)

    # print(data)


# top_five_alerts_api()
