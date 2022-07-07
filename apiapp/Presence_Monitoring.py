import requests


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


def Get_Mac_IDs_from_MQTT_DATA(data):
	return data['mac']

def Process_Mac_IDs(cloud_mqtt_mac_ids):
	ids_cards = ['AC233F5E688E', 'AC233F5E688C', 
				 'AC233F5A9EE9', 'F108BB3472D6', 'FEFDD727C6F5']
	for id_card in ids_cards:
		if id_card in cloud_mqtt_mac_ids:
			#it means that id_card is transmitting.
			#if not checked in then check in this id card
			#if already checked in then do nothing.
			url = f"{Token['dev']['URL']}/get_active_mac_ids_online/{id_card}/"
			res = requests.get(url, headers={
				'Authorization': f"Token {Token['dev']['token']}",
				'Content-Type': 'application/json'
			})
			checked_in = res.json()
			print(checked_in)
		else:
			#it means that id_card is not transmitting. so it could be switched off
			#so we need to check if this id_card is already checked in
			#if not checked in that means id_card is not present in event yet
			#if checked in that means id_card was present but now he is not
			url = f"{Token['dev']['URL']}/get_active_mac_ids/{id_card}/"
			res = requests.get(url, headers={
				'Authorization': f"Token {Token['dev']['token']}",
				'Content-Type': 'application/json'
			})
			checked_in = res.json()
			print(checked_in)
	


def Get_Mqtt_Data(data_from_gateway):
	print('GETTING DATA FROM NEW SCRIPT...')
	# Get MAC_IDs coming from Cloud MQTT
	cloud_mqtt_mac_ids = [data.get('mac') for data in data_from_gateway]
	Process_Mac_IDs(cloud_mqtt_mac_ids)

	# Get MAC_IDs of Attendees who are in ACTIVE Events 
	# And their check in status (Null or Not Null)

