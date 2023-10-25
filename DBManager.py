import os
PASSWORD = os.getenv('FOR_POSTGRES')
import psycopg2

class DBManager:
    '''класс для работы с базой данных о вакансиях'''
    def __init__(self, conn):
        self.conn = self.connects_db()

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

    def take_non_zero(self):
        '''получает список вакансий из БД, в которых указан размер оплаты'''
        cur = self.conn.cursor()  # создаем курсор
        cur.execute('select vacancy_id, vacancy_name, salary_from_rub, salary_to_rub, requirement, url'
                    ' from vacancies WHERE salary_from <> 0 OR salary_to <> 0')
        # выводим выбранные из БД записи
        rows = cur.fetchall()
        self.print_vacancies(rows)
        cur.close()


    def sort_max_salary(self):
        '''получает из БД список вакансий, отсортированный в порядке возрастания средней зарплаты'''
        cur = self.conn.cursor()  # создаем курсор
        cur.execute('select vacancy_id, vacancy_name, salary_avg from vacancies ORDER BY salary_avg')
        # выводим выбранные из БД записи
        rows = cur.fetchall()
        for row in rows:
            print(f'№ вакансии {row[0]} {row[1]}\nсредняя зарплата по вакансии {row[2]} рублей')
        cur.close()


    def take_only_big(self, user_salary):
       '''получает из БД список вакансий с min зарплатой >= указанной суммы'''
       cur = self.conn.cursor()  # создаем курсор
       cur.execute("""select vacancy_id, vacancy_name, salary_from_rub, salary_to_rub, requirement, url
        from vacancies WHERE salary_from_rub >= (%s)""", (f'{user_salary}',))
       # выводим выбранные из БД записи
       rows = cur.fetchall()
       self.print_vacancies(rows)
       cur.close()


    def get_companies_and_vacancies_count(self):
        '''получает список всех компаний и количество вакансий у каждой компании'''
        cur = self.conn.cursor()  # создаем курсор
        cur.execute('SELECT employer_id, employer_name, COUNT(*) FROM vacancies JOIN employers '
                    'USING (employer_id) GROUP BY employer_id, employer_name ORDER BY COUNT(employer_id) DESC')
        # выводим выбранные из БД записи
        rows = cur.fetchall()
        for row in rows:
            print(f'{row[0]} {row[1]} количество вакансий: {row[2]}')
        cur.close()


    def get_all_vacancies(self):
        '''получает список всех вакансий с указанием названия компании,названия вакансии,зарплаты и ссылки на вакансию'''
        cur = self.conn.cursor()  # создаем курсор
        cur.execute('SELECT employer_name, vacancy_name, salary_from_rub, salary_to_rub, url FROM vacancies '
                    'JOIN employers USING(employer_id) ORDER BY employer_name')
        # выводим выбранные из БД записи
        rows = cur.fetchall()
        for row in rows:
            print(f'{row[0]}\n{row[1]}\nзарплата от: {row[2]} до {row[3]} рублей\n{row[4]}')
        cur.close()


    def get_currency_rate(self):
        '''считываем справочник курсов валют из БД (таблица currency)'''
        cur = self.conn.cursor()  # создаем курсор
        cur.execute('SELECT currency_id, exchange_rate FROM currency')
        currency_rate = cur.fetchall()
        #print(currency_rate)
        cur.close()
        return currency_rate


    def get_avg_salary(self):
        '''получает среднюю зарплату по вакансиям.'''
        cur = self.conn.cursor()  # создаем курсор
        cur.execute('SELECT AVG(salary_avg) FROM vacancies WHERE salary_avg <> 0')
        salary_avg = cur.fetchall()
        # print(salary_avg)
        # print(f'Это средняя зарплата {salary_avg[0]}')
        cur.close()
        list_salary_avg = list(salary_avg[0])
        # print(list_salary_avg)
        # print(list_salary_avg[0])
        # print(round(list_salary_avg[0]))
        for_user_salary_avg = round(list_salary_avg[0])
        return for_user_salary_avg


    def get_vacancies_with_higher_salary(self):
        '''получает список всех вакансий, у которых зарплата выше средней по всем вакансиям.'''
        cur = self.conn.cursor()  # создаем курсор
        #list_salary_avg = self.get_avg_salary()
        cur.execute('SELECT vacancy_id, vacancy_name, salary_from_rub, salary_to_rub, requirement, url'
                    ' FROM vacancies WHERE salary_avg > (%s)', (f'{self.get_avg_salary()}',))
        #cur.execute('SELECT * FROM vacancies')
        rows = cur.fetchall()
        self.print_vacancies(rows)
        cur.close()


    def get_vacancies_with_keyword(self, user_word):
        '''получает список всех вакансий, в названии которых содержатся переданные в метод слова'''
        cur = self.conn.cursor()  # создаем курсор
        cur.execute("""SELECT vacancy_id, vacancy_name, salary_from_rub, salary_to_rub, requirement, url 
        FROM vacancies WHERE vacancy_name LIKE(%s)""", (f'%{user_word}%',))
        rows = cur.fetchall()
        #print(f'что нашли в vacancy_name:{rows}')
        self.print_vacancies(rows)
        cur.execute("""SELECT vacancy_id, vacancy_name, salary_from_rub, salary_to_rub, requirement, url 
        FROM vacancies WHERE requirement LIKE(%s)""", (f'%{user_word}%',))
        rows = cur.fetchall()
        #print(f'что нашли в requirement:{rows}')
        self.print_vacancies(rows)
        cur.close()


    def get_vacancies_employer(self, user_employer):
        '''получает список всех вакансий, у которых id работодателя равно введенному пользователем'''
        cur = self.conn.cursor()  # создаем курсор
        cur.execute("""SELECT vacancy_id, vacancy_name, salary_from_rub, salary_to_rub, requirement, url
         FROM vacancies JOIN employers USING (employer_id) WHERE employer_id =(%s)""",
                    (f'{user_employer}',))
        rows = cur.fetchall()
        self.print_vacancies(rows)
        cur.close()

    def print_vacancies(self, rows):
        '''выводит на экран список вакансий в удобном для пользователя виде'''
        for row in rows:
            #print(row)
            print(f'№ вакансии {row[0]} {row[1]}\n'
                  f'зарплата от {row[2]} до {row[3]} рублей\n'
                  f'Описание вакансии: {row[4]}\n'
                  f'{row[5]}')
            print()


