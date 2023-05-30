from abc import ABC, abstractmethod
import requests
import json
import os


class InitApi(ABC):

    @abstractmethod
    def get_vacancies(self):
        pass

    @abstractmethod
    def get_request(self):
        pass


class HeadHunterAPI(InitApi):

    def __init__(self, title):
        self.title = title
        self.params = {
            'text': f'{self.title}',  # Текст фильтра профессии
            'area': 113,  # Поиск по всем городам РФ
            'pages': 100,
            'page': 0,
            'per_page': 100,
            'only_with_salary': True,
            'archived': False
        }
        self.header = {
            "User-Agent": "My_App_v1.0"
        }
        self.api_url = 'https://api.hh.ru/vacancies'
        self.vacancies_hh = []

    def get_request(self):
        req = requests.get(self.api_url, headers=self.header, params=self.params)
        if req.status_code != 200:
            raise Exception(f"Ошибка в получении данных")
        data = req.content.decode()
        data = json.loads(data)["items"]
        req.close()
        return data

    def get_vacancies(self):
        try:
            for page in range(self.params["pages"]):
                self.params["page"] = page
                data = self.get_request()

                for k in data:
                    vacancy_id = k["id"]
                    vacancy_name = k["name"]
                    city = k["area"]["name"]
                    salary_from = k["salary"]["from"]
                    salary_to = k["salary"]["to"]
                    requirements = k["snippet"]["requirement"]
                    data = {
                        "id": vacancy_id,
                        "description": vacancy_name,
                        "city": city,
                        "requirements": requirements,
                        "salary": {
                            "from": salary_from,
                            "to": salary_to
                            }
                        }

                    self.vacancies_hh.append(data)

        except KeyError:
            pass

        vacancies_hh = json.dumps(self.vacancies_hh, sort_keys=True, indent=4, ensure_ascii=False)

        return vacancies_hh


class SuperJobAPI(InitApi):

    superjob_api = os.getenv("SJ_API")

    def __init__(self, title):
        self.api_url = 'https://api.superjob.ru/2.0/vacancies/'
        self.title = title
        self.headers = {
            "X-Api-App-Id": self.superjob_api
        }
        self.params = {
            "keyword": {self.title},
            "page": 0,
            "archive": False,
            "count": 100,
            "payment_defined": 1,
            "pages": 100
        }
        self.vacancies_sj = []

    def get_request(self):
        req = requests.get(self.api_url, headers=self.headers, params=self.params)
        if req.status_code != 200:
            raise Exception(f"Ошибка в получении данных")
        data = req.content.decode()
        data = json.loads(data)["objects"]
        req.close()
        return data

    def get_vacancies(self):
        try:
            for page in range(self.params["pages"]):
                self.params["page"] = page
                data = self.get_request()

                for k in data:
                    vacancy_id = k["id"]
                    vacancy_name = k["profession"]
                    city = k["town"]["title"]
                    salary_from = k["payment_from"]
                    salary_to = k["payment_to"]
                    requirements = k["candidat"]
                    data = {
                        "id": vacancy_id,
                        "description": vacancy_name,
                        "city": city,
                        "requirements": requirements,
                        "salary": {
                            "from": salary_from,
                            "to": salary_to
                            }
                        }

                    self.vacancies_sj.append(data)

        except KeyError:
            pass

        vacancies_sj = json.dumps(self.vacancies_sj, sort_keys=True, indent=4, ensure_ascii=False)

        return vacancies_sj


class Vacancy:
    def __init__(self):
        pass


class JSONSaver:

    def __init__(self, vacancy):
        self.vacancy = vacancy

    def add_vacancy(self):
        pass

    def get_vacancies_by_salary(self):
        pass

    def delete_vacancy(self):
        pass


hh_api = SuperJobAPI("python")
hh_vacancies = hh_api.get_vacancies()
print(hh_vacancies)
