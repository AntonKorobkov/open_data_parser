# coding=utf-8

import requests

res = requests.get('http://openapi.clearspending.ru/restapi/v3/contracts/select/?customerregion=48&okpd=92.40.10.111')
if res.ok:
    print(res.json())


class RequestHandler:
    """
    передавать экземпляру этого класса специальным
    образом сформированные строки
    """

    request_string = 'http://openapi.clearspending.ru/restapi/v3/contracts/select/?'

    def send_request(self, regnum, *kwargs):
        """
        отправить запрос к апи, получить
        json
        предполагаем что один именнованый аргумент
        который либо okdp либо okpd
        :param regnum:
        :param args:
        :return:
        """


