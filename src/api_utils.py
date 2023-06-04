from abc import ABC, abstractmethod
from src.vacancy import Vacancy
from src.json_saver import JSONSaver
import requests
import json
import os


class InitApi(ABC):

    @abstractmethod
    def get_request(self):
        pass

    @abstractmethod
    def get_parsed_data(self):
        pass


class HeadHunterAPI(InitApi):

    def __init__(self, title, pages):
        self.title = title
        self.pages = pages
        self.api_url = 'https://api.hh.ru/vacancies'
        self.data = None
        self.vacancies_hh = []

    def get_request(self):
        for page in range(self.pages):
            params = {
                'text': f'{self.title}',  # Текст фильтра профессии
                'area': 113,  # Поиск по всем городам РФ
                'page': page,
                'per_page': 100,
                'only_with_salary': True,
                'archived': False
            }
            header = {
                "User-Agent": "My_App_v1.0"
            }

            req = requests.get(self.api_url, headers=header, params=params)
            if req.status_code != 200:
                raise Exception(f"Ошибка в получении доступа к данным")
            self.data = json.loads(req.text)["items"]
            self.data.append(self.data)
            req.close()
        return self.data

    def get_parsed_data(self):
        for item in self.data:
            vacancy = Vacancy()
            try:
                vacancy.title = item["name"]
                vacancy.description = item["snippet"]["requirement"]
                vacancy.city = item["area"]["name"]
                vacancy.url = item["alternate_url"]

                if item["salary"]:
                    vacancy.salary_from = item["salary"]["from"] if item["salary"]["from"] else 0
                    vacancy.salary_to = item["salary"]["to"] if item["salary"]["to"] else 0

            except Exception as err:
                print("Ошибка в данных ['item'] - ", err)

            self.vacancies_hh.append(vacancy.get_json())
            JSONSaver().add_vacancy(self.vacancies_hh, "hh_json.json")

        return self.vacancies_hh


class SuperJobAPI(InitApi):

    superjob_api = os.getenv("SJ_API")

    def __init__(self, title, pages):
        self.api_url = 'https://api.superjob.ru/2.0/vacancies/'
        self.title = title
        self.pages = pages
        self.data = None
        self.vacancies_sj = []

    def get_request(self):
        for page in range(self.pages):
            params = {
                "keyword": {self.title},
                "page": page,
                "archive": False,
                "count": 100,
                "payment_defined": 1,
                "pages": 100
            }
            headers = {
                "X-Api-App-Id": self.superjob_api
            }
            req = requests.get(self.api_url, headers=headers, params=params)
            if req.status_code != 200:
                raise Exception(f"Ошибка в получении данных")
            self.data = json.loads(req.text)["objects"]
            self.data.append(self.data)
            req.close()
        return self.data

    def get_parsed_data(self):
        for item in self.data:
            vacancy = Vacancy()
            try:
                vacancy.title = item["profession"]
                vacancy.description = item["candidat"]
                vacancy.city = item["town"]["title"]
                vacancy.url = item["link"]
                vacancy.salary_from = item["payment_from"] if item["payment_from"] else 0
                vacancy.salary_to = item["payment_to"] if item["payment_to"] else 0

            except Exception as err:
                print("bad data in item", err)

            self.vacancies_sj.append(vacancy.get_json())
            JSONSaver().add_vacancy(self.vacancies_sj, "sj_json.json")

        return self.vacancies_sj


# hh_api = HeadHunterAPI("python", 1)
# hh_vacancies = hh_api.get_request()
# hh_vacancies_ = hh_api.get_parsed_data()
# sj_api = SuperJobAPI("python", 1)
# sj_vacancies = sj_api.get_request()
# sj_vacancies_ = sj_api.get_parsed_data()
