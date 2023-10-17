"""Скрипт для заполнения данными таблиц в БД Postgres."""
import psycopg2
import os
import csv

PASSWORD = os.getenv('FOR_POSTGRES')

def write_data():
    '''записываем информацию о вакансиях из csv-файла в таблицы БД'''
    filename = 'vacancies_hh.csv'
    #try:
    #path = f'../homework-1/north_data/{filename}'
    with open(filename) as f:
        data_file = csv.DictReader(f)
        for line in data_file:
            cur = conn.cursor()  #создаем курсор на каждую запись таблицы
            if line['currency'] not in ['RUR', 'USD', 'EUR']:
                #записываем сначала новый currency в справочник (таблица currency)
                cur.execute('INSERT INTO currency VALUES (%s) ON CONFLICT DO NOTHING',
                            (line['currency_name']))
            else:
                #записываем работодателя в справочник - таблицу employers
                cur.execute('INSERT INTO employers VALUES (%s, %s) ON CONFLICT DO NOTHING', (line['employer_id'],
                                                                              line['employer_name']))
            #записываем информацию о вакансии в таблицу vacancies
            cur.execute('INSERT INTO vacancies VALUES (vacancy_id, vacancy_name, salary_from, salary_to,'
                        ' currency_id, gross, url, requirement, employer_id) ON CONFLICT DO NOTHING',
                        (line['id'], line['name'], line['salary_from'], line['salary_to'], line['gross'],
                         line['url'], line['requirement'], line['employer_id']))
    # except psycopg2.errors.UniqueViolation:
    #     print(f'запись с таким ключом уже есть в таблице {table_name}')
    # except psycopg2.errors.InFailedSqlTransaction:
    #     print('текущая транзакция прервана, команды до конца блока транзакции игнорируются')
    # else:
            cur.close()
            conn.commit()

#подключаемся к БД
conn = psycopg2.connect(
    host='localhost',
    database='KR161023_API_DataBase',
    user='postgres',
    password=PASSWORD
)

# создаем курсор
# cur = conn.cursor()

# записываем данные в таблицы

write_data()

# создаем курсор
# cur = conn.cursor()

# # проверяем записи в таблице employees
# cur.execute("SELECT *FROM employees")
# rows = cur.fetchall()
# for row in rows:
#     print(row)
# # проверяем записи в таблице customers
# cur.execute("SELECT *FROM customers")
# rows = cur.fetchall()
# for row in rows:
#     print(row)
# # проверяем записи в таблице orders
# cur.execute("SELECT *FROM orders")
# rows = cur.fetchall()
# for row in rows:
#     print(row)


conn.close()

def get_companies_and_vacancies_count():
    '''получает список всех компаний и количество вакансий у каждой компании'''
    pass

def get_all_vacancies():
    '''получает список всех вакансий с указанием названия компании, названия вакансии и зарплаты и ссылки на вакансию'''
    pass

def get_avg_salary():
    '''получает среднюю зарплату по вакансиям.'''
    pass

def get_vacancies_with_higher_salary():
    '''получает список всех вакансий, у которых зарплата выше средней по всем вакансиям.'''
    pass

def get_vacancies_with_keyword():
    '''получает список всех вакансий, в названии которых содержатся переданные в метод слова, например python.'''
    pass
