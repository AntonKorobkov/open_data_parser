# coding=utf-8

import requests

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

    def send_request(self, regnum, **kwargs):
        """
        отправить запрос к апи, получить
        json
        предполагаем что именованный аргумент только один
        либо okdp либо okpd
        :param regnum:
        :param args:
        :return: :list список контрактов
        """
        classcode = list(kwargs.keys())[0]
        req = ''.join([RequestHandler.request_string, regnum, '&', classcode, '=', kwargs[classcode]])
        res = requests.get(req)

        return res.json()['contracts']['data']

    def result_to_contracts(self, result):
        """
        извлечь нужные данные
        :return:
        """
        contracts = {}
        for contract in result:
            # номер контракта
            contracts['conum'] = contract["regNum"]
            # дата подписания
            contracts['signed'] = contract["signDate"]
            # стоимость
            contracts['price'] = contract["price"]
            # предмет контракта
            contracts['product'] = contract["products"][0]["name"]
            # заказчик
            contracts['customer'] = contract["customer"]["fullName"]
            # инн заказчика
            contracts['customer_inn'] = contract["customer"]["inn"]
            # исполнитель
            contracts['supplname'] = contract["suppliers"][0]["organizationName"]
            # инн исполнителя
            contracts['supplinn'] = contract["suppliers"][0]["inn"]
            # орг форма исполнителя
            contracts['supplform'] = contract["suppliers"][0]

        return contracts

    def main(self, regnum, **kwargs):
        response = self.send_request(regnum, **kwargs)
        return self.result_to_contracts(response)


my_handler = RequestHandler()
test_result = my_handler.main('48', okpd='92.40.10.111')
print(test_result)

# print(test_result['data'])
