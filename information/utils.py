import hashlib
from datetime import datetime
from random import randint
from django.http.response import JsonResponse


def gen_hash_pwd(passwd):
    return str(hashlib.sha256(passwd).hexdigest())


def rand4Digit():
    return randint(1000, 9999)


def generate_unique_id(key):
    dt = datetime.now()
    return key + str(dt.year) + str(dt.month) + \
        str(dt.day) + str(dt.hour) + str(dt.minute) + \
        str(dt.second) + str(dt.microsecond) + \
        str(rand4Digit())


def _send(data, status_code):
    return JsonResponse(data=data, status=status_code)


def send_200(data, res_str=''):
    if res_str:
        data['res_str'] = res_str
    return _send(data, 200)


def send_400(data, res_str=''):
    if res_str:
        data['res_str'] = res_str
    return _send(data, 400)


def send_201(data):
    return _send(data, 201)