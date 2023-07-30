import os
from abc import ABC, abstractmethod

import requests as requests

from exceptions import ParsingError
from utils import get_currencies


class VacancyAPI(ABC):
    """
    Aбстрактный класс для работы с API сайтов с вакансиями
    """

    @abstractmethod
    def get_request(self):
        pass

    @abstractmethod
    def get_vacancies(self):
        pass


class HeadHunterAPI(VacancyAPI):
    """Класс для работы с API сайта HeadHunter."""
    url = 'https://api.hh.ru/vacancies'

    def __init__(self, keyword: str):
        """
         Инициализация по ключевому слову поиска
        :param keyword: Ключевое слово для поиска вакансии
        """
        # page:Номер страницы;  per_page:Количество вакансий на странице;
        # text:Строка для поиска по названию вакансии;
        # area:Идентификатор региона с вакансией, по умолчанию 113 - Россия.
        # archived:архивирование вакансий
        self.params: dict = {
            'page': None,
            'per_page': 50,
            'text': keyword,
            # 'area': '113',
            'archived': False,
        }
        self.vacancies: list[dict] = []

    def get_request(self):
        """ Метод для получения вакансии"""
        response = requests.get(self.url, params=self.params)
        if response.status_code != 200:
            raise ParsingError(f'Ошибка получения вакансий! Статус: {response.status_code}')
        return response.json()['items']

    def get_vacancies(self, pages_count=2) -> None:
        """
        Метод для сбора вакансий со всех страниц (pages_count)
        :param pages_count: количество страниц для поиска
        :return: None
        """
        self.vacancies = []

        for page in range(pages_count):
            page_vacancies = []
            try:
                page_vacancies = self.get_request()
            except ParsingError as error:
                print(error)
            else:
                self.vacancies.extend(page_vacancies)
                print(f"Загружено вакансий: {len(page_vacancies)}")
            if len(page_vacancies) == 0:
                break

    def get_formatted_vacancies(self):
        """ Метод для получения отформатированных вакансий"""

        # Список для сохранения отформатированных вакансий
        formatted_vacancies: list[dict] = []

        #  курсы валют к рублю
        currencies = get_currencies()

        # валюты доступные на hh.ru
        hh_currencies = {
            "AZN": "AZN",
            "BYR": "BYR",
            'EUR': "EUR",
            'GEL': "GEL",
            "KGS": "KGS",
            "KZT": "KZT",
            "RUR": "RUR",
            "UAH": "UAH",
            "USD": "USD",
            "UZS": "UZS",
        }

        # Приведение вакансий к нужному виду
        for vacancy in self.vacancies:
            formatted_vacancy: dict = {
                'employer': vacancy['employer']['name'],
                'title': vacancy['name'],
                'url': vacancy['url'],
                'api': "hh",
            }
            if vacancy['salary'] is not None:
                formatted_vacancy['salary_from'] = vacancy['salary']['from'] if vacancy['salary']['from'] and \
                                                                                vacancy['salary'][
                                                                                    'from'] is not None else None
                formatted_vacancy['currency'] = vacancy['salary']['currency'] if vacancy['salary']['currency'] and \
                                                                                 vacancy['salary'][
                                                                                     'currency'] is not None else None
                formatted_vacancy['currency_value'] = currencies[hh_currencies[vacancy['salary']['currency']]] if \
                    hh_currencies[vacancy['salary']['currency']] in currencies else 1

                if vacancy['salary']['currency'] in hh_currencies:
                    formatted_vacancy['currency'] = hh_currencies[vacancy['salary']['currency']]
                    formatted_vacancy['currency_value'] = currencies[hh_currencies[vacancy['salary']['currency']]] if \
                        hh_currencies[vacancy['salary']['currency']] in currencies else 1
                elif vacancy['salary']['currency']:
                    formatted_vacancy['currency'] = 'RUR'
                    formatted_vacancy['currency_value'] = 1
                else:
                    formatted_vacancy['currency'] = None
                    formatted_vacancy['currency_value'] = None
            else:
                formatted_vacancy['salary_from'] = None
                formatted_vacancy['currency'] = None
                formatted_vacancy['currency_value'] = None

            formatted_vacancies.append(formatted_vacancy)
        return formatted_vacancies


class SuperJobAPI(VacancyAPI):
    """Класс для работы с API сайта superjob.ru."""
    url = 'https://api.superjob.ru/2.0/vacancies/'
    api_key: str = os.getenv('SUPER_JOB_API')

    def __init__(self, keyword):
        """
        Инициализация по ключевому слову поиска
        :param keyword: Ключевое слово для поиска вакансии
        """
        # page:Номер страницы;
        # count:Количество вакансий на странице;
        # keyword: Ключевое слово для поиска по названию вакансии;
        # с: id региона с вакансией, по умолчанию 1 - Россия.
        # archived:архивирование вакансий
        self.params = {
            'count': 50,
            'page': None,
            'keyword': keyword,
            # 'c': 1,
            'archived': False,
        }
        self.headers = {'X-Api-App-Id': self.api_key}
        self.vacancies = []

    def get_request(self) -> list[dict]:
        """ Метод для получения вакансии"""
        response = requests.get(self.url, headers=self.headers, params=self.params)
        if response.status_code != 200:
            raise ParsingError(f'Ошибка получения вакансий! Статус: {response.status_code}')
        return response.json()['objects']

    def get_formatted_vacancies(self) -> list[dict[str, str | None]]:
        """ Метод для получения отформатированных вакансии"""

        # Список для сохранения отформатированных вакансий
        formatted_vacancies = []

        #  Курсы валют к рублю
        currencies = get_currencies()

        # Валюты доступные на superjob.ru
        sj_currencies = {
            "rub": "RUR",
            "uah": "UAH",
            "uzs": "UZS",
        }

        # Приведение вакансий к нужному виду
        for vacancy in self.vacancies:
            formatted_vacancy = {
                'employer': vacancy['firm_name'],
                'title': vacancy['profession'],
                'url': vacancy['link'],
                'api': "SuperJob",
                'salary_from': vacancy['payment_from'] if vacancy['payment_from'] and vacancy[
                    'payment_from'] is not None else None,
            }
            if vacancy['currency'] in sj_currencies:
                formatted_vacancy['currency'] = sj_currencies[vacancy['currency']]
                formatted_vacancy['currency_value'] = currencies[sj_currencies[vacancy['currency']]] if \
                    sj_currencies[vacancy['currency']] in currencies else 1
            else:
                formatted_vacancy['currency'] = None
                formatted_vacancy['currency_value'] = None

            formatted_vacancies.append(formatted_vacancy)
        return formatted_vacancies

    def get_vacancies(self, pages_count=2) -> None:
        """
        Метод для сбора вакансий со всех страниц (pages_count)
        :param pages_count: количество страниц для поиска
        :return: None
        """
        self.vacancies = []
        for page in range(pages_count):
            page_vacancies = []

            try:
                page_vacancies = self.get_request()
            except ParsingError as error:
                print(error)
            else:
                self.vacancies.extend(page_vacancies)
                print(f'Загружено вакансий: {len(page_vacancies)}')
            if len(page_vacancies) == 0:
                break
