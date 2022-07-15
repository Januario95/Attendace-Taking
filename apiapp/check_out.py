import requests
from time import sleep
from pytz import timezone
from datetime import datetime
from credentials import Token



def checkout_attendee():
    print(f'Calling checkout_attendee() ...')
    # Token = {
    #     'dev': {
    #         'URL': 'http://localhost:8000',
    #         'token': 'fd8068e77a29c03af33aed4981333cc2c2f6c5ae'
    #     },
    #     'prod': {
    #         'URL': 'https://attendance-bluguard.herokuapp.com',
    #         'token': 'b0d5d3983e8416da79454d60d13a9e26cd1ebe45'
    #     }
    # }
    url = f"{Token['URL']}/checkout_attendance/"
    headers = {
        'Authorization': f"Token {Token['token']}",
    }
    res = requests.get(url, headers=headers)
    data = res.json()

    print('\n')


# checkout_attendee()
while True:
    checkout_attendee()
    sleep(4)
