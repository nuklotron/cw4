from abc import ABC, abstractmethod
import json
import os


class ForJSON(ABC):
    @abstractmethod
    def add_vacancy(self, data, file_name):
        pass

    @abstractmethod
    def get_vacancies_by_salary(self, salary_from):
        pass

    @abstractmethod
    def delete_vacancy(self):
        pass


class JSONSaver(ForJSON):

    def add_vacancy(self, data, file_name):
        data = json.dumps(data, indent=4, ensure_ascii=False)
        with open(f"./data/{file_name}", "w", encoding="UTF8") as file:
            file.write(data)

    def get_vacancies_by_salary(self, salary_from):
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

    def delete_vacancy(self):
        open("./data/hh_json.json", 'w').close()
        open("./data/sj_json.json", 'w').close()
        open("./data/filtered_by_salary.json", 'w').close()

