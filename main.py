from utils import make_start_base
from utils import write_data
from utils import connect_bd
from utils import make_user_base
import psycopg2
import os
PASSWORD = os.getenv('FOR_POSTGRES')

URL_SITE_HH = 'https://api.hh.ru/vacancies/'
#URL_SITE_SUPERJOB = 'https://api.superjob.ru/2.0/vacancies/?t=4&count=10'
#print(len(URL_SITE_HH))

if __name__ == '__main__':

    # print("Привет! Введи пожалуйста свое имя:")
    # user_name = input()
    while True:
        print('Сделай выбор:')
        print(' 1 - дополним базу вакансий свежими данными и посмотрим\n 2 - посмотрим имеющуюся базу вакансий')
        option = int(input())
        if option == 1:
        #здесь загружаем данные с hh.ru и записываем в *.csv файл
            make_start_base()

        #здесь подключаемся к БД и заполняем БД новыми вакансиями
            # conn = psycopg2.connect(
            #     host='localhost',
            #     database='KR161023_API_DataBase',
            #     user='postgres',
            #     password=PASSWORD
            # )
            write_data()
            #conn.close()
        elif option == 2:
        #здесь подключаемся к БД и просматриваем существующую базу вакансий
            make_user_base()
        else:
            continue
