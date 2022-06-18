import mysql.connector as mysql
from rest_framework.response import Response


def index(request):
    return Response({
        'data': 'Yes'
    })
