from ForAPI import ForAPI_hh
#from ForAPI import ForAPI_superjob
#from GeneralBase import GeneralBase
#from UserBase import UserBase
from DBManager import DBManager
URL_SITE_HH = 'https://api.hh.ru/vacancies/'
#URL_SITE_SUPERJOB = 'https://api.superjob.ru/2.0/vacancies/?t=4&count=10'

import psycopg2
import os
import csv

PASSWORD = os.getenv('FOR_POSTGRES')

def make_start_base():
    '''формируем стартовую базу данных  '''
    list_base = works_with_hh()
    # print()
    # print()
    print(f'Это базовый список из функции make_start_base(): {list_base}')
    #make_user_base(user_name, resourse, list_base)


def works_with_hh():
    '''функция для сбора информации о вакансиях с сайта hh.ru'''
    site_hh = ForAPI_hh(URL_SITE_HH)  # создаем экземпляр класса
    site_hh.make_requests()           #запрашиваем информацию
    list_base = site_hh.make_list_vacancies()     #формируем список вакансий
    #site_hh.to_json()                 #записываем в файл
    site_hh.to_file_csv()             #записываем в csv-файл

    ##GeneralBase.instantiate_from_json('vacancies_hh')  # создаём экземпляры класса из данных файла
    ##list_base = GeneralBase.instantiate_from_json('vacancies_hh')
    print(f'list_base из метода instantiate_from_json {list_base}')
    return list_base


def make_user_base():
    while True:
        print()
        print('Выберите опцию:\n'
              ' 2 - сортировать по возврастанию среднего размера оплаты\n'
              ' 3 - выбрать только те вакансии, в которых указан размер оплаты\n'
              ' 4 - выбрать вакансии с указанным словом\n'
              ' 5 - выбрать вакансии с оплатой выше указанной суммы\n'
              ' 6 - возврат к исходному списку вакансий\n'
              ' 7 - сохранить в файл, полученный на экране список вакансий\n'
              ' 0 - выход без сохранения информации\n'
              ' 10 - получить список всех компаний и количество вакансий у каждой\n'
              ' 11 - получить список всех вакансий с указанием компании, названием вакансии, зарплаты и ссылки на вакансию\n'
              ' 12 - получить среднюю зарплату по всем вакансиям\n'
              ' 14 - получить список вакансий с зарплатой выше средней')
        option = int(input())
        if option == 0:
            print('Информация не сохранена.')  # БД со списком вакансий для пользователя не создаем
            break
        elif option == 6:
            print('ИСХОДНЫЙ ПЕРЕЧЕНЬ ВАКАНСИЙ:')
            conn = None
            db_manager = DBManager(conn)
            db_manager.get_all_vacancies()  # выводим на экран исходный список вакансий
        elif option == 7:
            #здесь надо вызвать метод из класса UserBase для сохранения экземпляров класса UserBase в файл
            if list_user_base == []:
                user_base = UserBase(list_base)
                user_base.to_json(user_name, resourse, list_base)
            else:
                user_base = UserBase(list_user_base)
                user_base.__dict__
                user_base.to_json(user_name, resourse, list_user_base)
            print(f'\nИнформация о вакансиях сохранена в файл "{user_name}_{resourse}"')
            break
        elif option == 4:
            print('Введите искомое слово:')
            user_word = input()
            #user_word_lower = user_word.lower()
            #вызываем метод из класса DBManager для фильтрации вакансий по заданному слову
            print('       ВЫБРАННЫЕ ВАКАНСИИ:')
            conn = None
            db_manager = DBManager(conn)
            db_manager.get_vacancies_with_keyword(user_word)
        elif option == 3:
            #вызываем метод из класса DBManager для фильтрации вакансий по ненулевой зарплате')
            print('       ВЫБРАННЫЕ ВАКАНСИИ:')
            # user_base = UserBase(list_base)
            # user_base.print_user_list(user_base.take_non_zero())
            conn = None
            db_manager = DBManager(conn)
            db_manager.take_non_zero()
        elif option == 2:
            #вызываем метод из класса DBManager для сортировки вакансий по возрастанию средней зарплаты')
            print('       ВЫБРАННЫЕ ВАКАНСИИ:')
            conn = None
            db_manager = DBManager(conn)
            db_manager.sort_max_salary()
        elif option == 5:
            #вызываем метод из класса DBManager для выбора вакансий с min зарплатой >= указанной суммы')
            print('Введите сумму оплаты, ниже которой вакансии не рассматривать:')
            user_salary = int(input())
            print('       ВЫБРАННЫЕ ВАКАНСИИ:')
            conn = None
            db_manager = DBManager(conn)
            db_manager.take_only_big(user_salary)
        elif option == 10:
            # вызываем метод из класса DBManager
            conn = None
            db_manager = DBManager(conn)
            db_manager.get_companies_and_vacancies_count()
            db_manager.disables_db()
        elif option == 11:
            # вызываем метод из класса DBManager
            conn = None
            db_manager = DBManager(conn)
            db_manager.get_all_vacancies()
            db_manager.disables_db()
        elif option == 12:
            conn = None
            db_manager = DBManager(conn)
            db_manager.get_avg_salary()
        elif option == 14:
            conn = None
            db_manager = DBManager(conn)
            db_manager.get_vacancies_with_higher_salary()
        else:
            continue

def connect_bd():
    '''подключаемся к БД'''
    conn = psycopg2.connect(
        host='localhost',
        database='KR161023_API_DataBase',
        user='postgres',
        password=PASSWORD
    )

def write_data():
    '''записываем информацию о вакансиях из csv-файла в таблицы БД'''
    filename = 'vacancies_hh.csv'
    conn = psycopg2.connect(
        host='localhost',
        database='KR161023_API_DataBase',
        user='postgres',
        password=PASSWORD
    )
    #для определения рублевого эквивалента считываем курсы валют из справочника в БД(таблица currency)
    db_manager = DBManager(conn)
    currency_rate = db_manager.get_currency_rate()
    dict_currency_rate = dict(currency_rate)
    #print(dict_currency_rate)
    #try:
    #path = f'../homework-1/north_data/{filename}'
    with open(filename, encoding='utf-8') as f:
        data_file = csv.DictReader(f)
        for line in data_file:
            #рассчитываем рублевый эквивалент среднюю зарплату по вакансии
            exchange_rate = dict_currency_rate[line['currency']]
            #print(dict_currency_rate[line['currency']])
            salary_from_rub = float(line['salary_from']) * exchange_rate
            salary_to_rub = float(line['salary_to']) * exchange_rate
            if salary_from_rub == 0:
                salary_avg = salary_to_rub
            elif salary_to_rub == 0:
                salary_avg = salary_from_rub
            else:
                salary_avg = round((salary_from_rub + salary_to_rub) / 2, 2)

            cur = conn.cursor()  #создаем курсор на каждую запись таблицы
            # сначала записываем работодателя в справочник - таблицу employers
            cur.execute('INSERT INTO employers VALUES (%s, %s) ON CONFLICT DO NOTHING',
                        (line['employer_id'], line['employer_name']))

            # записываем информацию о вакансии в таблицу vacancies
            cur.execute('INSERT INTO vacancies(vacancy_id, vacancy_name, salary_from, salary_to, currency_id, '
                        'gross, url, requirement, employer_id, salary_from_rub, salary_to_rub, salary_avg) '
                        'VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s) ON CONFLICT DO NOTHING',
                (line['id'], line['name'], line['salary_from'], line['salary_to'], line['currency'], line['gross'],
                 line['url'], line['requirement'], line['employer_id'], salary_from_rub, salary_to_rub, salary_avg))

            cur.close()
            conn.commit()
    conn.close()




