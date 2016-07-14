# -*- coding: utf-8 -*-
"""
Отсюда вызывать RequestHandler
с параметрами
"""

from request_handler import RequestHandler
import json

__author__ = 'Anton Korobkov'

# загружаем параметры

with open('parameters.json') as data_file:
    connection_data = json.load(data_file)

handler = RequestHandler()

for regnum in connection_data["regions"]:
    for okpd in connection_data["okpds"]:
        handler.main(regnum, okpd=okpd)

handler.write_to_excel('pandas_simple.xlsx')

