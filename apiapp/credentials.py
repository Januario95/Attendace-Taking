

TOKEN = {
    'dev': {
        'URL': 'http://localhost:8000',
        'token': 'fd8068e77a29c03af33aed4981333cc2c2f6c5ae'
    },
    'prod': {
        'URL': 'https://attendance-bluguard.herokuapp.com',
        'token': 'b0d5d3983e8416da79454d60d13a9e26cd1ebe45'
    }
}

def Get_Credentials(mode):
    return TOKEN[mode]


Token = Get_Credentials('dev')