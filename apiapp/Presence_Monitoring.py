import requests
from credentials import Token




def Process_Mac_IDs(cloud_mqtt_mac_ids):
	url = Token['URL'] + "/get_id_cards/"
	token = Token['token']	
	headers = {
    	'Authorization': f'Token {token}'
	}		
	res = requests.get(url, headers=headers)
	data = res.json()
	ids_cards = data['device_macs']

	for id_card in ids_cards:
		if id_card in cloud_mqtt_mac_ids:
			#it means that id_card is transmitting.
			#if not checked in then check in this id card
			#if already checked in then do nothing.
			url = f"{Token['URL']}/get_active_mac_ids_online/{id_card}/"
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
			url = f"{Token['URL']}/get_active_mac_ids/{id_card}/"
			res = requests.get(url, headers={
				'Authorization': f"Token {Token['token']}",
				'Content-Type': 'application/json'
			})
			checked_in = res.json()
			print(checked_in)
	


def Get_Mqtt_Data(data_from_gateway):
	print('GETTING DATA FROM NEW SCRIPT...')
	# Get MAC_IDs coming from Cloud MQTT
	cloud_mqtt_mac_ids = [data.get('mac') for data in data_from_gateway]
	Process_Mac_IDs(cloud_mqtt_mac_ids)

