import requests
from time import sleep
from pytz import timezone
from datetime import datetime


def checkout_attendee():
    token = 'fd8068e77a29c03af33aed4981333cc2c2f6c5ae'
    url = 'http://localhost:8000/attendee/'
    headers = {
        'Authorization': f'Token {token}',
    }

    res = requests.get(url, headers=headers)
    data = res.json()
    for row in data:
        is_online = row['is_online']

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
                url = f'http://localhost:8000/attendee/{attendee_id}/'
                data = {
                    'check_out_date': date,
                    'check_out_time': time,
                    'is_online': False,
                    'last_updated': now
                }
                res = requests.patch(url, headers=headers, data=data)
                data = res.json()
                print(data)

                # print(f'attendee_id = {attendee_id}')
                # check_in = data['check_in']
                # check_out = data['check_out']
                # url = f'http://localhost:8000/create_attendance/{attendee_id}/{check_in}/{check_out}/'
                # res = requests.get(url, headers=headers)  # , data=data)
                # data = res.json()
                # print(data)


# checkout_attendee()

while True:
    checkout_attendee()
    sleep(4)
