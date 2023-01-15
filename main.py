from engine_classes import SuperJob, HH

from jobs_classes import HHVacancy, SJVacancy, sorting, get_top


def main():
    user_input = input("Выберите нужный сайт для поиска [SuperJob, HH]: ")
    input_keyword = input("Ведите ключевое слово для поиска: ")
    input_count = input("Введите нужное количество вакансий: ")
    input_sorting = input("Вы хотите отсортировать вакансии по зарплате? [Yes/No]")
    while True:
        if user_input == "SuperJob":
            sj_engine = SuperJob()
            key = input_keyword
            v_co = 1000
            sj_res = sj_engine.get_request(key, v_co)
            sj_data = SuperJob.get_connector('sj_res.json')
            sj_data.insert(sj_res)
            SJVacancy.read_data('sj_res.json')
            if input_sorting == 'No' or 'no':
                get_top(SJVacancy.sj_vacancies, int(input_count))
                print(f'{SJVacancy.get_count_of_vacancy}')
            if input_sorting == 'Yes' or 'yes':
                get_top(sorting(SJVacancy.sj_vacancies), int(input_count))
                print(f'{SJVacancy.get_count_of_vacancy}')
            break
        if user_input == 'HH':
            hh_engine = HH()
            key = input_keyword
            v_co = 1000
            hh_res = hh_engine.get_request(key, v_co)
            hh_data = HH.get_connector('hh_res.json')
            hh_data.insert(hh_res)
            HHVacancy.read_data('hh_res.json')
            if input_sorting == 'No' or 'no':
                get_top(HHVacancy.hh_vacancies, int(input_count))
                print(f'{HHVacancy.get_count_of_vacancy}')
            if input_sorting == 'Yes' or 'yes':
                get_top(sorting(HHVacancy.hh_vacancies), int(input_count))
                print(f"{HHVacancy.get_count_of_vacancy}")
        break


if __name__ == '__main__':
    main()
