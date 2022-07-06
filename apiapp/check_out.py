import requests
from time import sleep
from pytz import timezone
from datetime import datetime


def checkout_attendee():
    print(f'Calling checkout_attendee() ...')
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

    url = f"{Token['dev']['URL']}/checkout_attendance/"
    headers = {
        'Authorization': f"Token {Token['dev']['token']}",
    }
    res = requests.get(url, headers=headers)
    data = res.json()


    # url = f"{Token['dev']['URL']}/checkout_attendance/"
    # headers = {
    #     'Authorization': f"Token {Token['dev']['token']}",
    # }
    # res = requests.get(url, headers=headers)
    # data = res.json()
    # print(data)
    # for row in data:
    #     pass

    print('\n')


# checkout_attendee()
while True:
    checkout_attendee()
    sleep(4)
