from src.api_utils import *
from src.vacancy import *
from src.json_saver import JSONSaver


def main():
    while True:
        print("1 - Загрузить вакансии Head Hunter")
        print("2 - Загрузить вакансии Super Job")
        print("3 - Отсортировать вакансии по ЗП")
        print("4 - Удалить данные из файлов")
        print("Exit - Завершить программу\n")

        user_input = input("Выберите пункт меню - ")

        if user_input.lower() == "exit":
            break

        elif int(user_input) == 1:
            title_input = input("Введите ключевое слово для поиска - ")
            pages_input = input("Введите кол-во страниц для поиска - ")
            hh_api = HeadHunterAPI(title_input, int(pages_input))
            hh_api.get_request()
            hh_api.get_parsed_data()

        elif int(user_input) == 2:
            title_input = input("Введите ключевое слово для поиска - ")
            pages_input = input("Введите кол-во страниц для поиска - ")
            sj_api = SuperJobAPI(title_input, int(pages_input))
            sj_api.get_request()
            sj_api.get_parsed_data()

        elif int(user_input) == 3:
            salary_input = int(input("Введите ЗП 'от' - "))
            JSONSaver.get_vacancies_by_salary(salary_from=salary_input)

        elif int(user_input) == 4:
            JSONSaver.delete_vacancy()

        else:
            print("Я тебя не понимаю")
            continue


if __name__ == "__main__":
    main()
