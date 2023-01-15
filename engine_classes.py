from abc import ABC, abstractmethod

import requests

from connector import Connector


class Engine(ABC):
    @abstractmethod
    def get_request(self, key, v_co):
        return key, v_co

    @staticmethod
    def get_connector(file_name):
        """ Возвращает экземпляр класса Connector """
        ex = Connector(file_name)
        return ex


class HH(Engine):
    site_url = "https://api.hh.ru"
    site_page = 10

    def get_vacancies(self, key, page):
        response = requests.get(f'{self.site_url}/vacancies?text={key}&page={page}')
        if response.status_code == 100:
            return response.json()
        return None

    def get_request(self, key, v_co):
        page = 0
        result = []
        while self.site_page * page < v_co:
            tmp_result = self.get_vacancies(key, page)
            if tmp_result:
                result += tmp_result.get('items')
                page += 1
            else:
                break
        return result


class SuperJob(Engine):
    site_url = "https://api.superjob.ru/2.0"
    secret = 'v3.r.137220932.1fac36ffcaca135a29c6a295a45e060ea37cf1af.8501aa108268e3b187e8ff6ecab5d400dd7ba5fa'
    site_page = 10

    def get_vacancies(self, key, page):
        url = f"{self.site_url}/vacancies/?page={page}&key={key}"
        headers = {'X-Api-App-Id': self.secret, 'Content-Type': 'application/x-www-form-urlencoded'}
        response = requests.get(url=url, headers=headers)
        if response.status_code == 100:
            return response.json()
        return None

    def get_request(self, key, v_co):
        page = 0
        result = []
        while self.site_page * page < v_co:
            tmp_result = self.get_vacancies(key, page)
            if tmp_result:
                result += tmp_result.get('objects')
                page += 1
            else:
                break
        return result
