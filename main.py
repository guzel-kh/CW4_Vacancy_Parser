from connector import Connector
from api import HeadHunterAPI, SuperJobAPI


def main():
    vacancies_json = []
    keyword: str = input("Введите ключевое слово для поиска:  ")

    # Создание экземпляра класса для работы с API сайтов с вакансиями
    hh = HeadHunterAPI(keyword)
    sj = SuperJobAPI(keyword)

    # Получение вакансий с разных платформ
    for api in (hh, sj):
        api.get_vacancies(pages_count=2)
        vacancies_json.extend(api.get_formatted_vacancies())

    # Создание экземпляра класса для работы с вакансиями
    connector = Connector(keyword=keyword, vacancies_json=vacancies_json)

    # Работа с вакансиями, сортировка вакансий по зарплате
    while True:
        command = input(
            "1 - Вывести список вакансий;\n"
            "2 - Отсортировать по минимальной зарплате (от min к max);\n"
            "3 - Отсортировать по минимальной зарплате (от max к min);\n"
            "exit - для выхода.\n"
        )
        if command.lower() == 'exit':
            break
        elif command == "1":
            vacancies = connector.select()
        elif command == "2":
            vacancies = connector.sort_by_salary_from_min_to_max()
        elif command == "3":
            vacancies = connector.sort_by_salary_from_max_to_min()

        for vacancy in vacancies:
            print(vacancy, end='\n========================\n')


if __name__ == "__main__":
    main()