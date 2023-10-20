import os
PASSWORD = os.getenv('FOR_POSTGRES')
import psycopg2

class DBManager:
    '''класс для работы с базой данных о вакансиях'''
    def __init__(self, conn): #, id_item, name, salary_from, salary_to, currency, gross, url, requirement):
        self.conn = self.connects_db()
        # self.id_item = id_item
        # self.name = name
        # self.salary_from = salary_from
        # self.salary_to = salary_to
        # self.currency = currency
        # self.gross = gross
        # self.url = url
        # self.requirement = requirement
        #
        # self.salary_min = self.find_salary_relevant(salary_from)
        # self.salary_max = self.find_salary_relevant(salary_to)
        pass

    def connects_db(self):
        '''подключает к БД'''
        conn = psycopg2.connect(
            host='localhost',
            database='KR161023_API_DataBase',
            user='postgres',
            password=PASSWORD
        )
        return conn

    def disables_db(self):
        '''отключает БД'''
        self.conn.close()

    def get_companies_and_vacancies_count(self):
        '''получает список всех компаний и количество вакансий у каждой компании'''
        cur = self.conn.cursor()  # создаем курсор
        cur.execute('SELECT employer_id, employer_name, COUNT(*) FROM vacancies JOIN employers USING (employer_id) GROUP BY employer_id, employer_name ORDER BY COUNT(employer_id) DESC')
        # выводим выбранные из БД записи
        rows = cur.fetchall()
        for row in rows:
            print(row)
        cur.close()

    def get_all_vacancies(self):
        '''получает список всех вакансий с указанием названия компании, названия вакансии и зарплаты и ссылки на вакансию'''
        cur = self.conn.cursor()  # создаем курсор
        cur.execute('SELECT employer_name, vacancy_name, salary_from, salary_to, url FROM vacancies JOIN employers USING(employer_id) ORDER BY employer_name')
        # выводим выбранные из БД записи
        rows = cur.fetchall()
        print(rows)
        for row in rows:
            print(row)
        cur.close()

    def get_currency_rate(self):
        '''считываем справочник курсов валют из БД (таблица currency)'''
        cur = self.conn.cursor()  # создаем курсор
        cur.execute('SELECT currency_id, exchange_rate FROM currency')
        currency_rate = cur.fetchall()
        print(currency_rate)
        cur.close()
        return currency_rate


    def get_avg_salary(self):
        '''получает среднюю зарплату по вакансиям.'''
        cur = self.conn.cursor()  # создаем курсор
        cur.execute('SELECT AVG(salary_avg) FROM vacancies WHERE salary_avg <> 0')
        salary_avg = cur.fetchall()
        print(f'Это средняя зарплата {salary_avg[0]}')
        cur.close()
        list_salary_avg = list(salary_avg[0])
        print(list_salary_avg)
        return list_salary_avg


    def get_vacancies_with_higher_salary(self):
        '''получает список всех вакансий, у которых зарплата выше средней по всем вакансиям.'''
        cur = self.conn.cursor()  # создаем курсор
        list_salary_avg = self.get_avg_salary()
        #cur.execute('SELECT * FROM vacancies WHERE salary_avg > %s', salary_avg)
        cur.execute('SELECT * FROM vacancies')
        rows = cur.fetchall()
        #print(rows)
        for row in rows:
            list_row = list(row)
            #print(list_row)
            #print(list_row[9])
            if list_row[9] > list_salary_avg[0]:
                print(list_row)
        cur.close()

    def get_vacancies_with_keyword(self, user_word_lower):
        '''получает список всех вакансий, в названии которых содержатся переданные в метод слова'''
        cur = self.conn.cursor()  # создаем курсор
        cur.execute('SELECT * FROM vacancies')
        rows = cur.fetchall()
        # print(rows)
        for row in rows:
            list_row = list(row)
            print(list_row[1])
            print(list_row[7])
            if user_word_lower in list_row[1]:
                print(list_row)
            elif user_word_lower in list_row[7]:
                print(list_row)
            else:
                continue
        cur.close()

    def get_vacancies_with_keyword1(self, user_word):
        '''получает список всех вакансий, в названии которых содержатся переданные в метод слова'''
        cur = self.conn.cursor()  # создаем курсор
        sql_select = "SELECT * FROM vacancies WHERE vacancy_name LIKE ('%s%')" % (user_word))
        cur.execute(sql_select, (user_word,))
        #cur.execute("SELECT * FROM vacancies WHERE vacancy_name LIKE ('%%%s%%')", (user_word,))
        rows = cur.fetchall()
        print(rows)
        for row in rows:
            print(row)

        cur.close()


