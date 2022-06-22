import requests
from time import sleep
from pytz import timezone
from datetime import datetime


def checkout_attendee():
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

    url = f"{Token['prod']['URL']}/attendee/"
    headers = {
        'Authorization': f"Token {Token['prod']['token']}",
    }

    res = requests.get(url, headers=headers)
    data = res.json()
    # print(data)
    for row in data:
        is_online = row['is_online']
        print(f'is_online = {is_online}')

        if is_online:
            attendee_id = row['id']
            last_updated = row['last_updated'].split('.')[0]
            last_updated = datetime.strptime(last_updated, '%Y-%m-%dT%H:%M:%S')
            now = datetime.now()  # timezone('Asia/Singapore'))
            date = now.date()
            time = now.time()
            diff = now - last_updated
            seconds = diff.seconds
            print(f'seconds = {seconds}')
            if seconds > 30:
                url = f"{Token['prod']['URL']}/attendee/{attendee_id}/"
                data = {
                    'check_out_date': date,
                    'check_out_time': time,
                    'is_online': False,
                    'last_updated': now
                }
                res = requests.patch(url, headers=headers, data=data)
                data = res.json()
                print(data)


# checkout_attendee()
while True:
    checkout_attendee()
    sleep(4)
