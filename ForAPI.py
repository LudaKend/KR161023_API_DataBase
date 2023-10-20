from abc import ABC, abstractmethod
import requests
import json
import os
#from GeneralBase import GeneralBase
import csv

class ForAPI(ABC):
    '''абстрактный класс для API'''
    @classmethod
    def __init__(cls, url_site):
        cls.url_site = url_site
        cls.list_vacancies = []

    def make_requests(cls):
        pass

    def make_list_vacancies(cls):
        pass


    def to_json(self):
        '''Записываем, полученный список словарей, в файл в формате JSON'''
        with open(self.name_array, 'w') as f:
            f.truncate(0)                    # очистим файл перед записью массива вакансий
        data = self.list_vacancies
        #print('это то, что записываем в json-файл:')
        #print(data)
        with open(self.name_array, 'w') as f:
            json.dump(data, f)

    def to_file_csv(self):
        '''Записываем, полученный список словарей, в .csv файл'''
        filename = 'vacancies_hh' + '.csv'
        with open(filename, 'w') as f:
            f.truncate(0)                    # очистим файл перед записью массива вакансий
        data = self.list_vacancies
        #print('это то, что записываем в csv-файл:')
        #print(data)
        table_head = ['id', 'name', 'salary_from', 'salary_to', 'currency', 'gross', 'url', 'requirement', 'employer_id', 'employer_name']
        with open(filename, 'w', encoding='utf-8') as f:
            #json.dump(data, f)
            file_writer = csv.DictWriter(f, lineterminator="\r", fieldnames=table_head)
            file_writer.writeheader()
            for vacancy in data:
                file_writer.writerow(vacancy)
        #print('Данные записаны в файл CSV')


class ForAPI_hh(ForAPI):
    '''класс для API с сайта hh.ru'''
    @classmethod
    def __init__(cls, url_site):
        super().__init__(url_site)
        cls.list_vacancies = []
        cls.name_array = 'vacancies_hh'

    @classmethod
    def make_requests(cls):
        '''выполняем API запрос к сайту hh.ru, получаем массив данных'''
        cls.responce = requests.get(cls.url_site)
        print(cls.responce.status_code)
        #print(cls.responce.text)
        cls.all_vacancies = json.loads(cls.responce.text)
        #print(all_vacancies)
        return cls.all_vacancies

    @classmethod
    def make_list_vacancies(cls):
        '''из полученного массива данных формируем список словарей нужной структуры'''
        cls.list_vacancies = []
        for vacancy in cls.all_vacancies['items']:
            # print()
            # print(vacancy)
            temp_dict = vacancy
            #print(temp_dict)
            id_item = temp_dict['id']
            name = temp_dict['name']
            salary = temp_dict['salary']

            url = temp_dict['url']
            requirement = temp_dict['snippet']['requirement']
            employer_id = temp_dict['employer']['id']
            employer_name = temp_dict['employer']['name']
            # responsibility = temp_dict['snippet']['responsibility']
            #решаем проблемы с незаполненными полями по зарплате
            if salary == None:
                salary_from = 0
                salary_to = 0
                currency = 'RUR'
                gross = False
            else:
                salary_from = temp_dict['salary']['from']
                salary_to = temp_dict['salary']['to']
                currency = temp_dict['salary']['currency']
                gross = temp_dict['salary']['gross']
            if salary_from == None:
                salary_from = 0
            if salary_to == None:
                salary_to = 0
            if currency == None:
                currency = 'RUR'
            if gross == False or gross == None:
                gross_bd = 0
            else:
                gross_bd = 1

            data = {'id':id_item, 'name': name, 'salary_from': salary_from, 'salary_to': salary_to,
                    'currency': currency,
                    'gross': gross_bd, 'url': url, 'requirement': requirement, 'employer_id': employer_id,
                    'employer_name':employer_name}
            #print(data)
            cls.list_vacancies.append(data)
        #print('это список словарей cls.list_vacancies:')
        #print(cls.list_vacancies)
        return cls.list_vacancies

# class ForAPI_superjob(ForAPI):
#     '''класс для API с сайта superjob.ru'''
#     api_key = os.getenv('API_KEY_superjob')
#
#     @classmethod
#     def __init__(cls, url_site):
#         super().__init__(url_site)
#         cls.list_vacancies = []
#         cls.name_array = 'vacancies_superjob'
#
#     @classmethod
#     def make_requests(cls):
#         '''выполняем API запрос к сайту superjob.ru, полученную информацию раскладываем в экземпляры класса'''
#         cls.responce = requests.get(cls.url_site, headers={'X-Api-App-Id': cls.api_key})
#         print(cls.responce.status_code)
#         #print(cls.responce.text)
#         cls.all_vacancies = json.loads(cls.responce.text)
#         #print(cls.all_vacancies)
#         return cls.all_vacancies
#
