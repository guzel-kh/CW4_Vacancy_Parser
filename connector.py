import json
import os

from vacancy import Vacancy


class Connector:
    def __init__(self, keyword, vacancies_json):
        self.filename = f"{keyword}.json"
        self.insert(vacancies_json)

    def insert(self, vacancies_json):
        with open(self.filename, "w", encoding="utf-8") as f:
            json.dump(vacancies_json, f, indent=3)

    def select(self):
        with open(self.filename, "r", encoding="utf-8") as file:
            vacancies = json.load(file)
        return [Vacancy(x) for x in vacancies]

    def delete(self):
        os.remove(self.filename)

    def sort_by_salary_from_min_to_max(self):
        vacancies = self.select()
        return sorted(vacancies, key=lambda x: (x.salary_from_converted if x.salary_from_converted else 0), reverse=False)

    def sort_by_salary_from_max_to_min(self):
        vacancies = self.select()
        return sorted(vacancies, key=lambda x: (x.salary_from_converted if x.salary_from_converted else 0), reverse=True)
