from abc import ABC, abstractmethod
from src.vacancy import Vacancy
import json


class ForJSON(ABC):
    @abstractmethod
    def add_vacancy(self, data, file_name):
        pass

    @abstractmethod
    def get_vacancies_by_salary(self, salary_from: int):
        pass

    @abstractmethod
    def delete_vacancy(self):
        pass

    @abstractmethod
    def top_vacancies(self):
        pass


class JSONSaver(ForJSON):
    """
    Класс для записи, удаления и фильтрации данных
    """
    @classmethod
    def add_vacancy(cls, data, file_name):
        """
        метод добавляет вакансию в файл
        :param data: список словарей в виде JSON
        :param file_name: название файла
        :return: "./data/{file_name}"
        """
        data = json.dumps(data, indent=4, ensure_ascii=False)
        with open(f"./data/{file_name}", "w", encoding="UTF8") as file:
            file.write(data)

    @classmethod
    def get_vacancies_by_salary(cls, salary_from):
        """
        метод фильтрует полученные вакансии по заданной ЗП
        :param salary_from: от какого значения искать
        :return: "./data/filtered_by_salary.json"
        """
        vacancies_by_salary = []
        try:
            with open("./data/hh_json.json", "r", encoding="UTF8") as file:
                read_data = json.load(file)
                for k in read_data:
                    if salary_from <= k["salary_from"]:
                        vacancies_by_salary.append(k)

            with open("./data/sj_json.json", "r", encoding="UTF8") as file:
                read_data = json.load(file)
                for k in read_data:
                    if salary_from <= k["salary_from"]:
                        vacancies_by_salary.append(k)

            data = json.dumps(vacancies_by_salary, indent=4, ensure_ascii=False)
            with open("./data/filtered_by_salary.json", "w", encoding="UTF8") as file:
                file.write(data)

        except FileExistsError as err:
            print("Файл не существует -", err)

    @classmethod
    def delete_vacancy(cls):
        """
        метод очищает все файлы
        :return: пустые файлы
        """
        open("./data/hh_json.json", 'w').close()
        open("./data/sj_json.json", 'w').close()
        open("./data/filtered_by_salary.json", 'w').close()

    @classmethod
    def top_vacancies(cls):
        """
        Выводит в консоль топ10 вакансий по ЗП
        :return:
        """
        try:
            with open("./data/filtered_by_salary.json", "r", encoding="UTF8") as file:

                read_data = json.load(file)
                sorted_data = sorted(read_data, key=lambda x: x['salary_from'] if x['salary_from'] else 0,
                                     reverse=True)

                for item in sorted_data[:10]:
                    vacancy = Vacancy(item["title"], item["salary_from"], item["salary_to"], item["description"], item["city"], item["url"])
                    print(
                        f"\nВакансия: {vacancy.title}\n"
                        f"Описание: {vacancy.description}\n"
                        f"ЗП: {vacancy.salary_from}\n"
                        f"Город: {vacancy.city}\n"
                        f"Ссылка: {vacancy.url}"
                    )
        except Exception as err:
            print("Ошибка в выводе топ-10 - ", err)
