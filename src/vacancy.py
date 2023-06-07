class Vacancy:
    """
    Класс приводит получаемые данные к общему виду для последующей записи в JSON формате.
    """
    def __init__(self, title="нет названия", salary_from=0, salary_to=0, description="нет описания", city="нет города", url="нет ссылки"):
        self.title = title
        self.salary_from = salary_from
        self.salary_to = salary_to
        self.description = description
        self.city = city
        self.url = url

    def __repr__(self):
        return f"{self.__class__.__name__}('{self.title}', {self.salary_from}-{self.salary_to})"

    def __str__(self):
        return f"Вакансия:{self.title}\nЗП: {self.salary_from}-{self.salary_to}\nГород:{self.city}\nURL:{self.url}"

    def __lt__(self, other):
        return self.salary_to < other.salary_to

    def __le__(self, other):
        return self.salary_to <= other.salary_to

    def __gt__(self, other):
        return self.salary_to > other.salary_to

    def __ge__(self, other):
        return self.salary_to >= other.salary_to

    def get_json(self):
        return {
            "title": self.title,
            "description": self.description,
            "salary_from": self.salary_from,
            "salary_to": self.salary_to,
            "city": self.city,
            "url": self.url
            }
