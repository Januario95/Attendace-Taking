#!/usr/bin/env python3
# -*- encoding: utf-8 -*-
"""
Created at Thur Apr 22 2021 18:31:43
"""

from email import header
import time
import json
from wsgiref import headers
import requests
from pytz import timezone
from datetime import datetime
# from read_json import ManageJson
import mysql.connector as mysql
from General_Functions import (
    Create_PK, Validate_Raw_Data_Length
)
from credentials import Token


config = {
    # 'host': 'attendance1.mysql.database.azure.com',
    # 'user': 'attendance',
    # 'password': 'AskPermission2022!',
    # 'database': 'bluguarddb',
    # # 'client_flags': [mysql.ClientFlag.SSL],
    # # 'ssl_ca': 'C',
    # 'port': '3306'


    # 'user': 'attendance2',
    # 'password': 'AskPermission2022!',
    # 'database': 'bluguarddb',
    # 'host': 'attendance2.mysql.database.azure.com',
    # 'port': 3306,
    # 'ssl_disabled': True,

    'user': 'attendance4',
    'password': 'AskPermission2022!',
    'database': 'bluguarddb',
    'host': 'attendance4.mysql.database.azure.com',
    'port': 3306,
    'ssl_disabled': True,
    'ssl_ca': '/SSL/DigiCertGlobalRootCA.crt.pem'
}


def dictfetchall(cursor):
    """
    Return column_name: value.
    If table has 'name' as a column, and as a value of 'Hayysoft' the function will return

    """
    columns = [col[0] for col in cursor.description]
    return [
        dict(zip(columns, row)) for row in cursor.fetchall()
    ]


def Insert_Alert(Alert_Code, Alert_Reading, Device_ID):
    url = f"{Token['URL']}/filter_alert_by_code_and_device_id/"
    headers = {
        'Authorization': f"Token {Token['token']}",
        'Content-Type': 'application/json'
    }
    data = {
        'alert_code': Alert_Code,
        'alert_reading': Alert_Reading,
        'device_reading': Device_ID
    }
    res = requests.post(url, headers=headers, data=json.dumps(data))
    print(res.status_code)
    # Connector = mysql.connect(**config)
    # Cursor = Connector.cursor()
    # query = '''SELECT TIMEDIFF(CURRENT_TIMESTAMP(), Alert_Datetime) > TIME('00:01:00') AS TIMEDIFF
    # 	FROM TBL_Alert WHERE Alert_Code = %s AND Device_ID = %s AND
    # 		TIMEDIFF(CURRENT_TIMESTAMP(), Alert_Datetime) > TIME('00:00:30');
    # '''
    # parameters = (Alert_Code, Device_ID)
    # Cursor.execute(query, parameters)
    # results = dictfetchall(Cursor)
    # for row in results:
    #     time_diff = row['TIMEDIFF']
    #     if time_diff == 1:
    #         print(f'TIMEDIFF = {time_diff}')
    #         query = """
    # 			DELETE FROM TBL_Alert
    # 				WHERE Alert_Code = %s AND Device_ID = %s AND
    # 					TIMEDIFF(CURRENT_TIMESTAMP(), Alert_Datetime) > TIME('00:01:00')
    # 		"""

    #         parameters = (Alert_Code, Device_ID)
    #         Cursor.execute(query, parameters)
    #         Connector.commit()

    #         query = '''
    # 	        INSERT INTO TBL_Alert
    # 	            (Alert_ID, Alert_Code, Alert_Reading,
    # 	             Alert_Date, Alert_Time, Device_ID, Alert_Datetime)
    # 	            VALUES(%s, %s, %s, CURRENT_DATE(), CURRENT_TIME(), %s, CURRENT_TIMESTAMP())
    # 	    '''

    #         parameters = (Create_PK('ALT'), Alert_Code,
    #                       Alert_Reading, Device_ID)
    #         Cursor.execute(query, parameters)
    #         Connector.commit()
    #         print(f'Updated Alert_Code: {Alert_Code}')

    # query = '''SELECT * FROM TBL_Alert WHERE Alert_Code = %s AND Device_ID = %s'''
    # parameters = (Alert_Code, Device_ID)
    # Cursor.execute(query, parameters)
    # results = dictfetchall(Cursor)
    # if len(results) == 0:
    #     query = '''
    #         INSERT INTO TBL_Alert
    #             (Alert_ID, Alert_Code, Alert_Reading,
    #              Alert_Date, Alert_Time, Device_ID, Alert_Datetime)
    #             VALUES(%s, %s, %s, CURRENT_DATE(), CURRENT_TIME(), %s, CURRENT_TIMESTAMP())
    #     '''

    #     parameters = (Create_PK('ALT'), Alert_Code, Alert_Reading, Device_ID)
    #     Cursor.execute(query, parameters)
    #     Connector.commit()
    #     print(f'Inserted Alert_Code: {Alert_Code}')


def Check_Highest_Score(Type, value_attr, device_id):
    print('HERE')
    value = 0
    alert_code = 0
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

    if alert_code != 0:
        print(f'alert_code = {alert_code}')
        Insert_Alert(alert_code, value, device_id)


def Extract_MetaData(data, key):
    """Returns the value for the given inside
    data dictionary."""
    return data.get(key)


def Start_Process_IoTData(data_from_gateway):
    pass


def Convert_Hex_To_Decimal(hex_data):
    """Converts hexadecimal data to decimal.
    Returns decimal data"""
    try:
        decimal_data = int(hex_data, 16)
        return decimal_data
    except (ValueError, TypeError):
        return ''


def Get_Vital_Temp(raw_data,
                   temp_startpos,
                   temp_endpos):
    """Extracts temperature in hexadecimal and
    returns the temperature in decimal from the rawdata.

    Parameters
    -----------------
    raw_data:		 the raw data to be extracted from
    temp_startpos:	 is the starting position of the temperature
                                     in raw data.
    temp_endpos:	 is the ending position (not inclusive) of the
                                     temperature in raw data.

    Returns
    ------
    temperature:     temperature converted to decimal from hexadecimal

    Exmple:
            >> Get_Vital_Temp('0EFF3412CFE2BBA5F0860301420016',
                                            20, 24)
    """
    temp_ = raw_data[temp_startpos:temp_endpos]
    temp_ = temp_[2:4] + temp_[0:2]
    # print(f'| raw_temp = {temp_}')
    temperature = Convert_Hex_To_Decimal(temp_) / 10
    return temperature


def Get_Vital_Heart_Rate(raw_data,
                         heart_rate_startpos,
                         heart_rate_endpos):
    """Extracts and returns the heartrate from the rawdata.

    Implementation of this function follows the same
    logic as the Get_Vital_Temp function above.
    """
    heart_rate_ = raw_data[heart_rate_startpos:heart_rate_endpos]
    # print(f'| raw_heart_rate = {heart_rate_}')
    return Convert_Hex_To_Decimal(heart_rate_)


def Get_Vital_Spo2(raw_data,
                   spo2_startpos,
                   spo2_endpost):
    """Extracts and returns the spo2 from the rawdata.

    Implementation of this function follows the same
    logic as the Get_Vital_Temp function above.
    """
    spo2 = raw_data[spo2_startpos:spo2_endpost]
    # print(f'| raw_spo2 = {spo2}')
    return Convert_Hex_To_Decimal(spo2)


def Get_Status_Batlevel(raw_data,
                        batlevel_startpos,
                        batlevel_endpost):
    """Extracts and returns the spo2 from the rawdata.

    Implementation of this function follows the same
    logic as the Get_Vital_Temp function above.
    """
    batlevel = raw_data[batlevel_startpos:batlevel_endpost]
    # print(f'| raw_batlevel = {batlevel}')
    return Convert_Hex_To_Decimal(batlevel)


def Get_Device_Type(Device_Mac):
    url = f"{Token['URL']}/search_device_by_device_mac/{Device_Mac}/"
    headers = {
        'Authorization': f"Token {Token['token']}",
        'Content-Type': 'application/json'
    }
    res = requests.get(url, headers=headers)
    data = res.json()
    if data['exists']:
        device_type = data['device']['device_type']
    else:
        device_type = ''
    return device_type


def HSWB001_Process_Data(raw_data):
    temperature = raw_data[16:18] + raw_data[14:16]
    temperature = int(temperature, 16) / 10
    heart_rate = Get_Vital_Heart_Rate(raw_data, 22, 24)
    spo2 = Get_Vital_Spo2(raw_data, 24, 26)
    batlevel = Get_Status_Batlevel(raw_data, 26, 28)
    vital_data = {
        'temp': temperature,
        'heart_rate': heart_rate,
        'spo2': spo2,
        'batlevel': batlevel
    }
    return vital_data


def Process_RawData(raw_data, device_type):
    """Extracts temperature, heart_rate, spo2, batlevel
    from raw data based on the device type
    """
    if device_type == 'HSWB001':
        data = HSWB001_Process_Data(raw_data)
        return data
    elif device_type == 'HSWB002' and len(raw_data) == 56:
        try:
            temperature = raw_data[40:42] + raw_data[38:40]
            temperature = int(temperature, 16) / 100
            heart_rate = Get_Vital_Heart_Rate(raw_data, 52, 54)
        except ValueError:
            pass

        data = {
            'temp': temperature,
            'heart_rate': heart_rate,
            'spo2': 0,
            'batlevel': 0
        }
        return data


def Extract_Device_Mac(data):
    device_macs = []
    for key, value in data.items():
        if key == 'mac':
            if data.get('type') != 'Gateway':
                device_macs.append(value)

    return device_macs


def Populate_MetaData(data, gateway_mac):
    Metadata_ = {}
    Metadata_['timestamp'] = data['timestamp']
    timestamp = data['timestamp'].split('T')
    date = timestamp[0]
    time = datetime.now().time()
    Metadata_['date'] = f'{date}'
    Metadata_['time'] = f'{time}'
    Metadata_['gateway_mac'] = gateway_mac
    Metadata_['device_mac'] = data['mac']
    Metadata_['bleName'] = data["bleName"]
    Metadata_['rssi'] = data['rssi']

    return Metadata_


def Process_Quarentine_Band(data, gateway_mac, Device_Mac, Device_Type):
    Connector = mysql.connect(**config)

    Cursor = Connector.cursor()

    populate_metadata = Populate_MetaData(data, gateway_mac)
    # print(populate_metadata)

    query_to_tbl_device = '''
		UPDATE TBL_Device
			SET Device_Last_Updated_Date = %s,
				Device_Last_Updated_Time = %s,
	            Device_Temp = %s,
	            Device_HR = %s,
	            Device_O2 = %s,
	            Incorrect_Data_Flag = %s,
	            Incorrect_Data_Flag = %s,
	            Device_Status = "ONLINE"
	        WHERE Device_Mac = %s
	'''
    parameters_to_tbl_device = (populate_metadata['date'],
                                populate_metadata['time'], 0, 0, 0, 0, 0, Device_Mac)
    Cursor.execute(query_to_tbl_device, parameters_to_tbl_device)
    Connector.commit()


def Filter_Message(validated, Device_Type, Raw_Data, data, gateway_mac, Device_Mac):
    populate_metadata = Populate_MetaData(data, gateway_mac)
    # print(populate_metadata)

    url = f"{Token['URL']}/update_device/"
    headers = {
        'Authorization': f"Token {Token['token']}",
        'Content-Type': 'application/json'
    }

    query_to_tbl_device = '''
		UPDATE TBL_Device
			SET Device_Last_Updated_Date = %s,
				Device_Last_Updated_Time = %s,
	            Device_Temp = %s,
	            Device_HR = %s,
	            Device_O2 = %s,
	            Device_Bat_Level = %s,
	            Incorrect_Data_Flag = %s,
	            Device_Status = "ONLINE"
	        WHERE Device_Mac = %s
	'''

    if validated == False:
        # json_manager = ManageJson('incorrect_raw_data')
        # data_from_json = json_manager.load_json()
        populate_metadata.update({
            'rawData': Raw_Data
        })
        # data_from_json.append(populate_metadata)
        # json_manager.save_json(data_from_json)
        # print('*' * 10, 'INCORRECT_DATA', '*' * 10)
        # print(f'validated = {validated}')
        # print(Raw_Data)
        # print(f'rawData = {data["rawData"]}')
        # print(f'Device_Mac = {Device_Mac}')
        # print(f'device_type = {Device_Type}')

        # parameters_to_tbl_device = (populate_metadata['date'],
        #                             populate_metadata['time'], 0, 0, 0, 0, 1, Device_Mac)
        # print(parameters_to_tbl_device)
        data = {
            'temp': 0, 'heart_rate': 0, 'spo2': 0, 'batlevel': 0,
            'incorrect_data_flag': 0, 'date': populate_metadata['date'],
            'time': populate_metadata['time'], 'device_mac': Device_Mac,
            'device_status': 'ONLINE', 'gateway_mac': gateway_mac
        }
        # print(json.dumps(data, indent=4))
        res = requests.post(url, headers=headers, data=json.dumps(data))
        data_ = res.json()
        print(data_['remark'])
        device_id = data_['device']['id']
    elif validated == True:
        # Data is correct
        populate_vitaldata = Process_RawData(Raw_Data, Device_Type)
        populate_vitaldata.update(populate_metadata)
        # print(populate_vitaldata)
        # json_manager = ManageJson()
        # data_from_json = json_manager.load_json()
        # data_from_json.append(populate_vitaldata)
        # json_manager.save_json(data_from_json)
        # print('*' * 10, 'CORRECT_DATA', '*' * 10)
        # print(f'validated = {validated}')
        # print(populate_vitaldata)
        # print(f'rawData = {data["rawData"]}')
        # print(f'Device_Mac = {Device_Mac}')
        # print(f'device_type = {Device_Type}')
        # print(f'batlevel = {populate_vitaldata["batlevel"]}')

        # parameters_to_tbl_device = (populate_metadata['date'], populate_metadata['time'],
        #                             populate_vitaldata['temp'], populate_vitaldata['heart_rate'],
        #                             populate_vitaldata['spo2'], populate_vitaldata['batlevel'], 0,
        #                             Device_Mac)

        # print(populate_vitaldata)
        temp = populate_vitaldata['temp']
        heart_rate = populate_vitaldata['heart_rate']
        spo2 = populate_vitaldata['spo2']
        batlevel = populate_vitaldata['batlevel']
        incorrect_data_flag = 1
        date = populate_metadata['date']
        time = populate_metadata['time']
        data = {
            'temp': temp, 'heart_rate': heart_rate, 'spo2': spo2,
            'batlevel': batlevel, 'incorrect_data_flag': incorrect_data_flag,
            'date': date, 'time': time, 'device_mac': Device_Mac,
            'device_status': 'ONLINE', 'gateway_mac': gateway_mac
        }
        # print(json.dumps(data, indent=4))
        res = requests.post(url, headers=headers, data=json.dumps(data))
        data_ = res.json()
        print(data_['remark'])
        device_id = data_['device']['id']

    print('\n')

    # query = '''
    # 	SELECT Device_ID FROM TBL_Device
    #         WHERE Device_Mac = %s
    # '''
    # parameter = (Device_Mac, )
    # Cursor.execute(query, parameter)
    # results = dictfetchall(Cursor)
    # Device_ID = results[0]['Device_ID']
    # Check_Highest_Score('temp', populate_vitaldata['temp'], device_id)
    # Check_Highest_Score(
    #     'heart_rate', populate_vitaldata['heart_rate'], device_id)
    # Check_Highest_Score('spo2', populate_vitaldata['spo2'], device_id)
    # Check_Highest_Score(
    #     'batlevel', populate_vitaldata['batlevel'], device_id)

    # try:
    #     print('SUCCESS')
    #     Cursor.execute(query_to_tbl_device, parameters_to_tbl_device)
    #     Connector.commit()
    # except:
    #     print('ERROR')

    # last_read_date, last_read_time, temp, heart_rate, spo2, batlevel, incorrect_data_flag, device_mac = parameters_to_tbl_device
    # print('YES')
    # headers = {
    #     'Authorization': f'Token {token}',
    #     'Content-Type': 'application/json'
    # }
    # url = f'http://localhost:8000/search_device_mac/{device_mac}/'
    # token = 'fd8068e77a29c03af33aed4981333cc2c2f6c5ae'
    # print(f'token = {token}')
    # res = requests.get(url, headers=headers)
    # data = res.json()
    # print(data)
    # print('Filter_Message function executed successfully!')
    # print(populate_vitaldata)



def Process_Mac_IDs(Device_Mac):
    print(f'Processing {Device_Mac}')
    url = Token['URL'] + "/get_id_cards/"
    token = Token['token']	
    headers = {
        'Authorization': f'Token {token}'
    }		
    res = requests.get(url, headers=headers)
    data = res.json()
    ids_cards = data['device_macs']

    if Device_Mac in ids_cards:
        #it means that id_card is transmitting.
        #if not checked in then check in this id card
        #if already checked in then do nothing.
        url = f"{Token['URL']}/get_active_mac_ids_online/{Device_Mac}/"
        res = requests.get(url, headers={
            'Authorization': f"Token {Token['token']}",
            'Content-Type': 'application/json'
        })
        checked_in = res.json()
        print(checked_in)
    else:
        #it means that id_card is not transmitting. so it could be switched off
        #so we need to check if this id_card is already checked in
        #if not checked in that means id_card is not present in event yet
        #if checked in that means id_card was present but now he is not
        url = f"{Token['URL']}/get_active_mac_ids/{Device_Mac}/"
        res = requests.get(url, headers={
            'Authorization': f"Token {Token['token']}",
            'Content-Type': 'application/json'
        })
        checked_in = res.json()
        print(checked_in)


def Get_Mqtt_Data(data_from_gateway):
    for data in data_from_gateway:
        if data['type'] == 'Gateway':
            gateway_mac = data['mac']

        if data['type'] != 'Gateway':
            Device_Mac = data['mac']
            Device_Type = Get_Device_Type(Device_Mac)

            Process_Mac_IDs(Device_Mac)

            if Device_Type == 'HSWB004':
                pass
                # Process_Quarentine_Band(
                #     data, gateway_mac, Device_Mac, Device_Type)
            elif data.get('rawData') is not None:
                try:
                    # results = Validate_Raw_Data_Length(Device_Type, data['rawData'])
                    results = True if len(data['rawData']) > 0 else False
                    Filter_Message(results, Device_Type, data['rawData'], data,
                                   gateway_mac=gateway_mac, Device_Mac=Device_Mac)
                except Exception:
                    pass

    print('\n\n')
