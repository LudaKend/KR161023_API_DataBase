from utils import make_data_base
from utils import create_db
from utils import create_tables

import os
PASSWORD = os.getenv('FOR_POSTGRES')

URL_SITE_HH = 'https://api.hh.ru/vacancies/'    #рабочий вариант  - выводит 20 вакансий с 0 (первой) страницы

if __name__ == '__main__':

    create_db()
    create_tables()
    make_data_base()
