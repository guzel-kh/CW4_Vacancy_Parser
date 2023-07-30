
class Vacancy:
    def __init__(self, vacancy):
        self.employer = vacancy['employer']
        self.title = vacancy['title']
        self.url = vacancy['url']
        self.api = vacancy['api']
        self.salary_from = vacancy['salary_from']
        self.currency = vacancy['currency']
        self.currency_value = vacancy['currency_value']
        if self.currency and self.salary_from:
            self.salary_from_converted = int(self.salary_from / self.currency_value)
        else:
            self.salary_from_converted = None

    def __str__(self):
        return f'Работодатель: {self.employer}\n' \
               f'Вакансия: {self.title}\n' \
               f'Зарплата от: {self.salary_from} {self.currency}\n' \
               f'Ссылка: {self.url}'

    def __gt__(self, other) -> bool:
        return self.salary_from_converted > other.salary_from_converted
