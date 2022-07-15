import requests
from time import sleep
from pytz import timezone
from datetime import datetime
from credentials import Token


def checkout_attendee():
    headers = {
        'Authorization': f"Token {Token['token']}",
    }
    url = f"{Token['URL']}/set_device_offline_online/"
    res = requests.get(url, headers=headers)
    data = res.json()
    print(data)


while True:
    checkout_attendee()
    sleep(5)

