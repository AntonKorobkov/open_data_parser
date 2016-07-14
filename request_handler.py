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
        self.all_contracts = []

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
        # может быть более одного продукта и более
        # одного поставщика

        contracts = []
        for record in result:

            contract = {}
            prodnum = len(record["products"])

            # номер контракта
            contract['Номер контракта'] = record["regNum"]
            # номер региона
            contract['Номер региона'] = record["regionCode"]
            # дата подписания
            contract['Дата подписи'] = record["signDate"]
            # стоимость
            contract['Стоимость контракта'] = record["price"]
            # предмет контракта, если их более одного,
            # они идут в одну ячейку
            contract['Предмет'] = '; '.join([record["products"][num]["name"] for num in range(prodnum)])
            # заказчик
            contract['Заказчик'] = record["customer"]["fullName"]
            # инн заказчика
            contract['ИНН заказчика'] = record["customer"]["inn"]
            # исполнитель (берем первого)
            contract['Поставщик'] = record["suppliers"][0]["organizationName"]
            # инн исполнителя
            contract['supplinn'] = record["suppliers"][0]["inn"]
            # орг форма исполнителя, определена не для всех
            try:
                contract['supplform'] = record["suppliers"][0]["legalForm"]["code"]
            except KeyError:
                contract['supplform'] = 'Not defined'

            contracts.append(contract)

        return contracts


    def main(self, regnum, **kwargs):
        # TODO: refactor
        response = self.result_to_contracts(self.send_request(regnum, **kwargs))
        for contr in response:
            self.all_contracts.append(contr)

    def write_to_excel(self, filepath):

        frame = pd.DataFrame(self.all_contracts)
        writer = pd.ExcelWriter(filepath, engine='xlsxwriter')
        frame.to_excel(writer, sheet_name='Contracts', index=False)
        writer.save()



if __name__ == "__main__":
    my_handler = RequestHandler()
    my_handler.main('48', okpd='92.40.10.111')
    my_handler.main('47', okpd='92.40.10.111')
    my_handler.write_to_excel('pandas_simple.xlsx')

