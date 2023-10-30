from configparser import ConfigParser
from ForAPI import ForAPI_hh
from DBManager import DBManager
URL_SITE_HH = 'https://api.hh.ru/vacancies/'

import psycopg2
import os
import csv

PASSWORD = os.getenv('FOR_POSTGRES')

def works_with_hh():
    '''функция для сбора информации о вакансиях с сайта hh.ru'''
    site_hh = ForAPI_hh(URL_SITE_HH)  # создаем экземпляр класса
    site_hh.make_requests()           #запрашиваем информацию
    list_base = site_hh.make_list_vacancies()     #формируем список вакансий
    site_hh.to_file_csv()             #записываем в csv-файл
    #print(f'list_vacancies из метода make_list_vacancies {list_base}')
    return list_base

def works_with_hh_employer(user_employer):
    '''функция для сбора информации о вакансиях с сайта hh.ru'''
    site_hh = ForAPI_hh(URL_SITE_HH)  # создаем экземпляр класса
    site_hh.make_requests_employer_id(user_employer)           #запрашиваем информацию по работодателю
    list_base = site_hh.make_list_vacancies()     #формируем список вакансий
    site_hh.to_file_csv()             #записываем в csv-файл
    #print(f'list_vacancies по работодателю из метода make_list_vacancies {list_base}')
    return list_base

def make_data_base():
    while True:
        print()
        print('Выберите опцию:\n'
              ' 0 - загрузить информацию о вакансиях в базу данных\n'
              ' 1 - получить список всех вакансий с указанием компании, названия вакансии, зарплаты и ссылки'
              ' на вакансию\n'
              ' 2 - сортировать по возврастанию среднего размера оплаты\n'
              ' 3 - выбрать только те вакансии, в которых указан размер оплаты\n'
              ' 4 - получить среднюю зарплату по всем вакансиям\n'
              ' 5 - получить список вакансий с зарплатой выше средней\n'
              ' 6 - выбрать вакансии с оплатой выше указанной суммы\n'
              ' 7 - выбрать вакансии с указанным словом\n'
              ' 8 - получить список всех компаний и количество вакансий у каждой\n'
              ' 9 - получить список вакансий по указанному работодателю\n'
              ' 99 - выход')
        option = int(input())
        if option == 99:
            print('Всего доброго! До новых встреч!')
            break
        elif option == 0:
            #здесь загружаем данные с hh.ru и записываем в *.csv файл
            works_with_hh()
            # здесь подключаемся к БД и заполняем БД новыми вакансиями
            write_data()
            print('База данных успешно заполнена')
        elif option == 7:
            print('Введите искомое слово:')
            user_word = input()
            #вызываем метод из класса DBManager для фильтрации вакансий по заданному слову
            print('       ВЫБРАННЫЕ ВАКАНСИИ:')
            conn = None
            db_manager = DBManager(conn)
            rows = db_manager.get_vacancies_with_keyword(user_word)
            #print(rows)
            db_manager.disables_db()  # отключаем БД
            save_vacancies(rows)
        elif option == 3:
            #вызываем метод из класса DBManager для фильтрации вакансий по ненулевой зарплате')
            print('       ВЫБРАННЫЕ ВАКАНСИИ:')
            conn = None
            db_manager = DBManager(conn)
            rows = db_manager.take_non_zero()
            db_manager.disables_db()  # отключаем БД
            save_vacancies(rows)
        elif option == 2:
            #вызываем метод из класса DBManager для сортировки вакансий по возрастанию средней зарплаты')
            print('       ВЫБРАННЫЕ ВАКАНСИИ:')
            conn = None
            db_manager = DBManager(conn)
            db_manager.sort_max_salary()
            db_manager.disables_db()  # отключаем БД
        elif option == 6:
            #вызываем метод из класса DBManager для выбора вакансий с min зарплатой >= указанной суммы')
            print('Введите сумму оплаты, ниже которой вакансии не рассматривать:')
            user_salary = int(input())
            print('       ВЫБРАННЫЕ ВАКАНСИИ:')
            conn = None
            db_manager = DBManager(conn)
            db_manager.take_only_big(user_salary)
            db_manager.disables_db()  # отключаем БД
        elif option == 8:
            #вызываем метод из класса DBManager,чтобы получить список всех компаний и количество вакансий у каждой
            print('       Работодатели:')
            conn = None
            db_manager = DBManager(conn)
            db_manager.get_companies_and_vacancies_count()
            db_manager.disables_db()    #отключаем БД
        elif option == 1:
            # вызываем метод из класса DBManager для вывода всех вакансий из БД с указанием компании,
            # названием вакансии, зарплаты и ссылки на вакансию
            print('       ВЫБРАННЫЕ ВАКАНСИИ:')
            conn = None
            db_manager = DBManager(conn)
            db_manager.get_all_vacancies()
            db_manager.disables_db()    #отключаем БД
        elif option == 4:
            # вызываем метод из класса DBManager чтобы получить среднюю зарплату по всем вакансиям
            conn = None
            db_manager = DBManager(conn)
            for_user_salary_avg = db_manager.get_avg_salary()
            print(f'РАЗМЕР СРЕДНЕЙ ЗАРПЛАТЫ ПО ВСЕМ ВАКАНСИЯМ БАЗЫ ДАННЫХ СОСТАВЛЯЕТ: {for_user_salary_avg} рублей')
            db_manager.disables_db()   #отключаем БД
        elif option == 5:
            # вызываем метод из класса DBManager чтобы получить список вакансий с зарплатой выше средней
            print('       ВЫБРАННЫЕ ВАКАНСИИ:')
            conn = None
            db_manager = DBManager(conn)
            db_manager.get_vacancies_with_higher_salary()
            db_manager.disables_db()   #отключаем БД
        elif option == 9:
            # вызываем метод из класса ForAPI, чтобы загрузить в БД список вакансий по указанному работодателю
            print('Введите id работодателя')
            user_employer = int(input())
            works_with_hh_employer(user_employer)
            write_data()
            # вызываем метод из класса DBManager чтобы получить список вакансий по указанному работодателю
            print('       ВЫБРАННЫЕ ВАКАНСИИ:')
            conn = None
            db_manager = DBManager(conn)
            db_manager.get_vacancies_employer(user_employer)
            db_manager.disables_db()  # отключаем БД
        else:
            continue


def write_data():
    '''записываем информацию о вакансиях из csv-файла в таблицы БД'''
    filename = 'vacancies_hh.csv'
    conn = psycopg2.connect(
        host='localhost',
        database='kr_api_database',
        user='postgres',
        password=PASSWORD
    )
    #для определения рублевого эквивалента считываем курсы валют из справочника в БД(таблица currency)
    db_manager = DBManager(conn)
    currency_rate = db_manager.get_currency_rate()
    dict_currency_rate = dict(currency_rate)
    #print(dict_currency_rate)
    with open(filename, encoding='utf-8') as f:
        data_file = csv.DictReader(f)
        for line in data_file:
            #рассчитываем рублевый эквивалент и среднюю зарплату по вакансии
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

def save_vacancies(rows):
    '''сохраняет, выбранные пользователем данные в обособленную БД'''
    print('Сохранить выбранные вакансии? Y/N')
    save_option = input()
    if save_option == 'Y' or save_option == 'y' or save_option == 'да' or save_option == 'Да':
        conn = None
        db_manager = DBManager(conn)
        conn = db_manager.connects_db()
        cur = conn.cursor()  # создаем курсор
        try:
            cur.execute("""
                CREATE TABLE user_vacancies (
                    vacancy_id INT PRIMARY KEY,
                    vacancy_name varchar(100),
                    salary_from_rub real,
                    salary_to_rub real,
                    requirement varchar,
                    url varchar
                )
            """)
        except psycopg2.errors.DuplicateTable:
            print('предыдущая пользовательская выборка удаляется')

        cur.close()
        conn.commit()
        #предварительно удалим записи из пользовательской таблицы
        cur = conn.cursor()  # создаем курсор
        cur.execute('TRUNCATE TABLE user_vacancies')
        cur.close()
        conn.commit()
        for row in rows:
            cur = conn.cursor()  # создаем курсор на каждую запись
            cur.execute('INSERT INTO user_vacancies(vacancy_id, vacancy_name, salary_from_rub, salary_to_rub,'
                        ' requirement, url) VALUES (%s, %s, %s, %s, %s, %s) ON CONFLICT DO NOTHING',
                        (row[0], row[1], row[2], row[3], row[4], row[5]))
            cur.close()
            conn.commit()
        db_manager.disables_db()

def create_db(database):
    '''удаляет и создает БД'''
    database_name = database #'KR161023_API_DataBase1'
    parser = ConfigParser()
    parser.read("database.ini")   #считываем параметры для подключения к POSGRESQL
    dict_db = {}
    if parser.has_section("postgresql"):
        params = parser.items("postgresql")
        for param in params:
            dict_db[param[0]] = param[1]
    else:
        raise Exception(
            'Section {0} is not found in the {1} file.'.format(database_name, "database.ini"))
    dict_db['password'] = PASSWORD

    conn = psycopg2.connect(dbname='postgres', **dict_db)
    conn.autocommit = True
    cur = conn.cursor()

    cur.execute(f"DROP DATABASE IF EXISTS {database_name}")
    cur.execute(f"CREATE DATABASE {database_name}")
    cur.close()
    conn.close()
    # создаем таблицы в БД
    conn = None
    db_manager = DBManager(conn)
    conn = db_manager.connects_db()
    create_table_employers(conn)
    create_table_currency(conn)
    create_table_vacancies(conn)
    write_currency(conn)  # заполняем справочник курсов валют
    db_manager.disables_db()

def create_table_employers(conn):
    '''создает таблицу employers в БД'''
    try:
        cur = conn.cursor()
        cur.execute("""CREATE TABLE employers (
                employer_id INTEGER PRIMARY KEY,
                employer_name VARCHAR(100)
            )
        """)
        conn.commit()
        cur.close()
    except psycopg2.errors.DuplicateTable:
        print('таблица employers уже создана')
        cur.close()
    except psycopg2.errors.InFailedSqlTransaction:
        cur.close()

def create_table_currency(conn):
    '''создает таблицу currency в БД'''
    try:
        cur = conn.cursor()
        cur.execute("""CREATE TABLE currency (
                currency_id varchar(3) PRIMARY KEY,
                currency_name varchar(20),
                exchange_rate real	
            )
        """)
        conn.commit()
        cur.close()
    except psycopg2.errors.DuplicateTable:
        print('таблица currency уже создана')
    except psycopg2.errors.InFailedSqlTransaction:
        cur.close()

def create_table_vacancies(conn):
    '''создает таблицу vacancies в БД'''
    try:
        cur = conn.cursor()
        cur.execute("""CREATE TABLE vacancies (
                vacancy_id INTEGER PRIMARY KEY,
                vacancy_name varchar(100),
                salary_from real,
                salary_to real,
                currency_id varchar(3),
                gross INTEGER,
                url varchar,
                requirement varchar,
                employer_id INTEGER,
                salary_avg real,
                salary_from_rub real,
                salary_to_rub real,
                FOREIGN KEY(currency_id) REFERENCES currency(currency_id),
                FOREIGN KEY(employer_id) REFERENCES employers(employer_id))
        """)
        conn.commit()
        cur.close()
    except psycopg2.errors.DuplicateTable:
        print('таблица vacancies уже создана')
    except psycopg2.errors.InFailedSqlTransaction:
        cur.close()

def write_currency(conn):
    '''заполняет справочник курсов валют'''
    list_currency = [('RUR', 'Российский рубль', 1), ('USD', 'Доллар США', 97.31), ('EUR', 'Евро', 102.55),
                     ('BYR', 'Белорусский рубль', 29.5776), ('KZT', 'Казахстанский тенге', 0.203576),
                     ('UZS', 'Узбекский сум', 0.00797149), ('KGS', 'Киргизский сом', 1.04)]

    #conn = None
    # db_manager = DBManager(conn)
    # conn = db_manager.connects_db()
    try:
        for pos in list_currency:
            cur = conn.cursor()  # создаем курсор на каждую запись
            cur.execute('INSERT INTO currency(currency_id, currency_name, exchange_rate)'
                    ' VALUES (%s, %s, %s) ON CONFLICT DO NOTHING',
                    (pos[0], pos[1], pos[2]))
            cur.close()
            conn.commit()
    except psycopg2.errors.InFailedSqlTransaction:
        cur.close()
