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

    url = f"{Token['dev']['URL']}/attendee/"
    headers = {
        'Authorization': f"Token {Token['dev']['token']}",
    }

    res = requests.get(url, headers=headers)
    data = res.json()
    # print(data)
    for row in data:
        is_online = row['is_online']
        tag_id = row['tag_id']
        print(f'{tag_id} = {is_online}')

        if is_online:
            attendee_id = row['id']
            attendee_name = row['attendee_name']
            check_in_date = row['check_in_date']
            check_in_time = row['check_in_time']

            last_updated = row['last_updated'].split('.')[0]
            last_updated = datetime.strptime(last_updated, '%Y-%m-%dT%H:%M:%S')
            now = datetime.now()
            date = now.date()
            time = now.time()
            diff = now - last_updated
            seconds = diff.seconds
            print(f'seconds = {seconds}')
            print(f'date = {date}')
            print(f'time = {time}')
            if seconds > 30:
                url = f"{Token['dev']['URL']}/attendee/{attendee_id}/"
                data = {
                    'check_out_date': date,
                    'check_out_time': time,
                    'is_online': False,
                    'last_updated': now
                }
                res = requests.patch(url, headers=headers, data=data)
                data = res.json()
                print(data)

                url = f"{Token['dev']['URL']}/update_attendance/{attendee_name}/{check_in_date}/{check_in_time}/{date}/{time}/"
                res = requests.get(url, headers={
                    'Authorization': f"Token {Token['dev']['token']}",
                    'Content-Type': 'application/json'
                })
                d = res.json()
                print(d)

                # url = f"{Token['dev']['URL']}/search_attendance/{attendee_name}/{check_in_date}/{check_in_time}/"
                # res = requests.get(url, headers=headers)
                # d = res.json()
                # print(d)
                # if d['exists']:
                #     attendance_id = d['attendance']['attendance_id']
                #     url = f"{Token['dev']['URL']}/check_out_attendance/{attendance_id}/{date}/{time}"
                #     res = requests.get(url, headers=headers)
                #     print(res.json())

    print('\n')


# checkout_attendee()
while True:
    checkout_attendee()
    sleep(4)
