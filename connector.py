import json
import os


class Connector:
    """Класс коннектор к файлу, обязательно файл должен быть в json формате, не забывать проверять целостность данных, что файл с данными не подвергся внешней деградации"""
    __data_file = None

    @property
    def data_file(self):
        return self.__data_file

    @data_file.setter
    def data_file(self, value):
        self.__data_file = value
        self.__connect()

    def __init__(self, df):
        self.__data_file = df
        self.__connect()

    def __connect(self):
        """ Проверка на существование файла с данными и создание его при необходимости. Также проверить деградацию и возбудить исключение, если файл потерял актуальность в структуре данных """
        if self.__data_file not in os.listdir('.'):
            with open(self.__data_file, 'w', encoding='utf-8') as f:
                json.dump([], f)
        else:
            return self.__data_file

    def insert(self, data):
        """ Запись данных в файл с сохранением структуры и исходных данных """
        with open(self.__data_file, 'r') as f:
            files = json.load(f)
            files.append(data)
        with open(self.__data_file, 'w') as f:
            json.dump(files, f)

    def select(self, query):
        """ Выбор данных из файла с применением фильтрации query содержит словарь, в котором ключ это поле для фильтрации, а значение это искомое значение, например: {'price': 1000}, должно отфильтровать данные по полю price и вернуть все строки, в которых цена 1000 """
        data_in_file = []
        with open(self.__data_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
            if not query:
                return data

            for i in data:
                for m, t in query.items():
                    if i[m] == t:
                        data_in_file.append(i)
                    return data_in_file

    def delete(self, query):
        """ Удаление записей из файла, которые соответствуют запросу, как в методе select. Если в query передан пустой словарь, то функция удаления не сработает """
        with open(self.__data_file, encoding='utf-8') as f:
            data = json.load(f)
        count = 0
        for i in data:
            if i.get(list(query.keys())[0]) == list(query.values())[0]:
                del data[count]
            count += 1
        with open(self.__data_file, 'w', encoding='utf-8') as f:
            json.dump(data, f)

# if __name__ = '__main__':
#     df = Connector('df.json')
#     data_for_file = {'id': 1, 'title': 'tet'}
#     df.insert(data_for_file)
#     data_from_file = df.select(dict())
#     assert data_from_file == [data_for_file]
#     df.delete({'id': 1})
#     data_from_file = df.select(dict())
#     assert data_from_file == []
