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
    headers = {
        'Authorization': f"Token {Token['dev']['token']}",
    }
    url = f"{Token['dev']['URL']}/set_device_offline_online/"
    res = requests.get(url, headers=headers)
    data = res.json()
    print(data)

    url = f"{Token['dev']['URL']}/attendee/"
    res = requests.get(url, headers=headers)
    data = res.json()
    # print(data)
    for row in data:
        check_out_date = row['check_out_date']
        print(f'check_out_date = {check_out_date}')
        if check_out_date is not None:
            attendee_id = row['id']
            last_updated = row['last_updated']
            if last_updated is not None:

                url = f"{Token['dev']['URL']}/get_attendance_by_attendee_id/{attendee_id}/"
                res = requests.get(url, headers=headers)
                data = res.json()
                clear_checks = data['clear_checks']
                print(f'clear_checks = {clear_checks}')
                if clear_checks:
                    last_updated = last_updated.split('.')[0]
                    last_updated = datetime.strptime(
                        last_updated, '%Y-%m-%dT%H:%M:%S')
                    now = datetime.now()
                    diff = now - last_updated
                    seconds = diff.seconds
                    print(f'seconds = {seconds}')
                    if seconds > 60:
                        url = f"{Token['dev']['URL']}/attendee/{attendee_id}/"
                        data = {
                            'check_out_date': '',
                            'check_out_time': '',
                            'check_in_date': '',
                            'check_in_time': '',
                        }
                        res = requests.patch(url, headers=headers, data=data)
                        data = res.json()
                        print(data)
    print('\n')


# checkout_attendee()
while True:
    checkout_attendee()
    sleep(5)


# Token = {
#     'dev': {
#         'URL': 'http://localhost:8000',
#         'token': 'fd8068e77a29c03af33aed4981333cc2c2f6c5ae'
#     },
#     'prod': {
#         'URL': 'https://bluguard-attendance.herokuapp.com',
#         'token': '3d7fbc0bc2ea8cb3c5e8afb4a7d289d04880b14f'
#     }
# }
# headers = {
#     'Authorization': f"Token {Token['dev']['token']}",
# }
# attendee_id = 8
# url = f"{Token['dev']['URL']}/attendee/{attendee_id}/"
# data = {
#     'check_out_date': '',
#     'check_out_time': '',
#     'check_in_date': '',
#     'check_in_time': '',
# }
# res = requests.patch(url, headers=headers, data=data)
# data = res.json()
# print(data)
