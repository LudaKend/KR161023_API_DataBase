from utils import make_data_base
from utils import create_db

import os
PASSWORD = os.getenv('FOR_POSTGRES')   #для доступа к БД Postgresql нужен пароль

URL_SITE_HH = 'https://api.hh.ru/vacancies/'    #рабочий вариант  - выводит 20 вакансий с 0 (первой) страницы

if __name__ == '__main__':
    database = 'kr_api_database'
    create_db(database)         # создаем структуру БД

    make_data_base()            # наполняем БД вакансиями
