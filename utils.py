from ForAPI import ForAPI_hh
#from ForAPI import ForAPI_superjob
#from GeneralBase import GeneralBase
#from UserBase import UserBase
URL_SITE_HH = 'https://api.hh.ru/vacancies/'
#URL_SITE_SUPERJOB = 'https://api.superjob.ru/2.0/vacancies/?t=4&count=10'

def make_start_base():
    '''формируем стартовую базу данных  '''
    list_base = works_with_hh()
    # print()
    # print()
    print(f'Это базовый список из функции make_start_base(): {list_base}')
    #make_user_base(user_name, resourse, list_base)

# def make_start_base(user_name, resourse):
#     '''формируем стартовую базу данных  '''
#     if resourse == 0:
#         print("Поиск вакансий с других ресурсов в настоящее время находится в работе, \n приносим извинения"
#               " за доставленные неудобства")
#     elif resourse > 3:
#         print('К сожалению с таким номером источника информации не существует. Всего доброго!')
#     elif resourse == 1:
#         list_base = works_with_hh()
#         make_user_base(user_name,resourse,list_base)
#     elif resourse == 2:
#         list_base = works_with_superjob()
#         make_user_base(user_name,resourse,list_base)
#     elif resourse == 3:
#         list_base = works_with_hh()
#         list_base_add = works_with_superjob()
#         for item in list_base_add:
#             list_base.append(item)
#         make_user_base(user_name,resourse,list_base)

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

# def works_with_superjob():
#     '''функция для сбора информации о вакансиях с сайта superjob.ru'''
#     site_superjob = ForAPI_superjob(URL_SITE_SUPERJOB)
#     site_superjob.make_requests()
#     site_superjob.make_list_vacancies()
#     site_superjob.to_json()
#     list_base = GeneralBase.instantiate_from_json('vacancies_superjob')  # создаём экземпляры класса из данных файла
#     return list_base

def make_user_base(user_name,resourse,list_base):
    list_user_base = []
    while True:
        print()
        print('Выберите опцию:\n'
              ' 1 - сортировать по возврастанию МИНИМАЛЬНОГО размера оплаты\n'
              ' 2 - сортировать по возврастанию МАКСИМАЛЬНОГО размера оплаты\n'
              ' 3 - выбрать только те вакансии, в которых указан размер оплаты\n'
              ' 4 - выбрать вакансии с указанным словом\n'
              ' 5 - выбрать вакансии с оплатой выше указанной суммы\n'
              ' 6 - возврат к исходному списку вакансий\n'
              ' 7 - сохранить в файл, полученный на экране список вакансий\n'
              ' 0 - выход без сохранения информации')
        option = int(input())
        if option == 0:
            print('Информация не сохранена. Всего доброго!')  # файл со списком вакансий для пользователя не создаем
            break
        elif option == 6:
            print('ИСХОДНЫЙ ПЕРЕЧЕНЬ ВАКАНСИЙ:')
            make_start_base(user_name,resourse)  # выводим на экран исходный список вакансий
            list_user_base = []
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
            user_word_lower = user_word.lower()
            #вызываем метод из класса UserBase для фильтрации экземпляров класса UserBase по заданному слову
            print('       ВЫБРАННЫЕ ВАКАНСИИ:')
            user_base = UserBase(list_base)
            user_base.print_user_list(user_base.find_word(user_word_lower))
        elif option == 3:
            #вызываем метод из класса UserBase для фильтрации экземпляров класса UserBase по нулевой зарплате')
            print('       ВЫБРАННЫЕ ВАКАНСИИ:')
            user_base = UserBase(list_base)
            user_base.print_user_list(user_base.take_non_zero())
        elif option == 2:
            #вызываем метод из класса UserBase для сортировки экземпляров класса UserBase по возрастанию max зарплаты')
            print('       ВЫБРАННЫЕ ВАКАНСИИ:')
            user_base = UserBase(list_base)
            user_base.print_user_list(user_base.sort_max_salary())
        elif option == 1:
            #вызываем метод из класса UserBase для сортировки экземпляров класса UserBase по возрастанию min зарплаты')
            print('       ВЫБРАННЫЕ ВАКАНСИИ:')
            user_base = UserBase(list_base)
            user_base.print_user_list(user_base.sort_min_salary())
        elif option == 5:
            #вызываем метод из класса UserBase для выбора экземпляров класса UserBase с min зарплатой >= указанной')
            print('Введите сумму оплаты, ниже которой вакансии не рассматривать:')
            user_salary = int(input())
            print('       ВЫБРАННЫЕ ВАКАНСИИ:')
            user_base = UserBase(list_base)
            user_base.print_user_list(user_base.take_only_big(user_salary))
        else:
            continue
