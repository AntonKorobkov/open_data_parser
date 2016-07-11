# coding=utf-8

import requests
import pandas as pd

res = requests.get('http://openapi.clearspending.ru/restapi/v3/contracts/select/?customerregion=48&okpd=92.40.10.111')
if res.ok:
    print(res.json())


class RequestHandler:
    """
    Передавать экземпляру этого класса специальным
    образом сформированные строки
    предполагаем что номер региона всегда дан
    """

    request_string = 'http://openapi.clearspending.ru/restapi/v3/contracts/select/?customerregion='

    def __init__(self):
        self.response = {}

    def send_request(self, regnum, **kwargs):
        """
        отправить запрос к апи, получить
        json
        предполагаем что именованный аргумент только один
        либо okdp либо okpd
        :param regnum:
        :param args:
        :return:
        """
        classcode = list(kwargs.keys())[0]
        req = ''.join([RequestHandler.request_string, regnum, '&', classcode, '=', kwargs[classcode]])
        res = requests.get(req)

        return res.json()

    def run_everything(self):
        pass


my_handler = RequestHandler()
test_result = my_handler.send_request('48', okpd='92.40.10.111')
