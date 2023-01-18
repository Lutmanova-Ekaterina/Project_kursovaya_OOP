import json


class Vacancy:
    class_name = 'Vacancy'
    __slots__ = ('name', 'link', 'salary')

    def __init__(self, name, link, salary, class_name):
        self.name = name
        self.link = link
        self.salary = salary
        self.class_name = Vacancy.class_name

    def check_salary(self, other):
        if not self.salary:
            self.salary = 0
            if not other.salary:
                other.salary = 0
            return self.salary, other.salary

    def __repr__(self):
        if self.salary:
            return f"{self.class_name}: {self.company_name}, зарплата: {self.salary} руб/мес"
        else:
            return f"{self.class_name}: {self.company_name}, зарплата: нет данных"

    def __str__(self):
        return f' {self.name}, зарплата {self.salary} руб/мес'

    def __eq__(self, other):
        return self.salary == other.salary

    def __ne__(self, other):
        return self.salary != other.salary

    def __lt__(self, other):
        return self.salary < other.salary

    def __le__(self, other):
        return self.salary <= other.salary

    def __gt__(self, other):
        return self.salary > other.salary

    def __ge__(self, other):
        return self.salary >= other.salary

    def __iter__(self):
        self.index = 0
        return self.index

    def __next__(self):
        if self.index < len(HHVacancy.hh_vacancies):
            d = HHVacancy.hh_vacancies[self.index]
            self.index += 1
            return d
        else:
            raise StopIteration


class CountMixin:
    @property
    def get_count_of_vacancy(self):
        """ Вернуть количество вакансий от текущего сервиса, Получать количество необходимо динамически из файла """
        with open(self.data_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
            return len(data)


class SJVacancy(CountMixin, Vacancy):
    # add counter mixin
    """ SuperJob Vacancy """
    sj_vacancies = []
    class_name = 'SJ'
    data_file = 'sj_res.json'

    def __init__(self, name, link, salary, company_name):
        super().__init__(name, link, salary, company_name)
        self.company_name = company_name
        self.class_name = SJVacancy.class_name
        self.data_file = SJVacancy.data_file
        self.salary = salary

    @classmethod
    def read_data(cls, data_file):
        with open(f'{data_file}') as f:
            data = json.load(f)
            for elem in data:
                for i in elem:
                    name = i.get('profession')
                    link = i.get('link')
                    company_name = i.get('employer')
                    try:
                        salary = i.get('payment_from')
                    except (AttributeError, TypeError):
                        salary = 0
                        company_name = i.get('firm_name')

                    cls.sj_vacancies.append(HHVacancy(name, link, salary, company_name))


class HHVacancy(CountMixin, Vacancy):
    # add counter mixin
    """ HeadHunter Vacancy """
    hh_vacancies = []
    class_name = 'HH'
    data_file = 'hh_res.json'

    def __init__(self, name, link, salary, company_name):
        super().__init__(name, link, salary, company_name)
        self.company_name = company_name
        self.class_name = HHVacancy.class_name
        self.data_file = HHVacancy.data_file
        self.salary = salary

    @classmethod
    def read_data(cls, data_file):
        with open(f'{data_file}') as f:
            data = json.load(f)
            for elem in data:
                for i in elem:
                    name = i.get('name')
                    link = i.get('url')
                    company_name = i.get('employer')
                    try:
                        if i.get('salary').get('currency') == 'USD':
                            salary = i.get('salary').get('from') * 70
                        elif i.get('salary').get('currency') == 'EUR':
                            salary = i.get('salary').get('from') * 75
                        else:
                            salary = i.get('salary').get('from')
                    except (AttributeError, TypeError):
                        salary = 0
                        company_name = i.get('employer').get('name')

                    cls.hh_vacancies.append(HHVacancy(name, link, salary, company_name))


def sorting(vacancies):
    """ Должен сортировать любой список вакансий по ежемесячной оплате (gt, lt, magic methods) """
    vacancies = sorted(vacancies, reverse=True)
    return vacancies


def get_top(vacancies, top_count):
    """ Должен возвращать {top_count} записей из вакансий по зарплате (iter, next magic methods) """
    try:
        for i in range(top_count):
            print(vacancies[i])
    except IndexError:
        print(f' {top_count} таких вакансий нет!')
