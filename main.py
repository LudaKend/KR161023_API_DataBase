from utils import make_data_base
from utils import create_db
from utils import create_tables
from utils import write_currency

import os
PASSWORD = os.getenv('FOR_POSTGRES')

URL_SITE_HH = 'https://api.hh.ru/vacancies/'    #рабочий вариант  - выводит 20 вакансий с 0 (первой) страницы

if __name__ == '__main__':
    database = 'KR161023_API_DataBase1'
    create_db(database)         # создаем БД
    create_tables(database)     # создаем таблицы
    write_currency()    # заполняем справочник курсов валют
    make_data_base()
