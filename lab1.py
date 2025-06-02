import psycopg2
from psycopg2.extensions import register_type, UNICODE

CONN_STR = "host='localhost' dbname='postgres' user='postgres' password='postgres'"
# CONN_STR = "host='10.22.31.252' dbname='rpr' user='zuev_g' password='efb3de92'"


def get_tour_info(tour_id):
    conn = psycopg2.connect(CONN_STR)
    cursor = conn.cursor()
    cursor.callproc("zuev_g.get_tour_info", (tour_id,))
    tour_info = cursor.fetchone()
    cursor.close()
    conn.close()
    return tour_info


def get_five_star_hotels():
    conn = psycopg2.connect(CONN_STR)
    cursor = conn.cursor()
    cursor.callproc('zuev_g.get_five_star_hotels')
    hotels = cursor.fetchall()
    cursor.close()
    conn.close()
    return hotels


def get_pricelist_on_date(date):
    conn = psycopg2.connect(CONN_STR)
    cursor = conn.cursor()
    cursor.callproc("zuev_g.get_pricelist_on_date", (date,))
    pricelist = cursor.fetchone()
    cursor.close()
    conn.close()
    return pricelist


def hotel_data(date):
    conn = psycopg2.connect(CONN_STR)
    cursor = conn.cursor()
    cursor.callproc("zuev_g.concatenate_hotel_data", (date,))
    data = cursor.fetchone()
    cursor.close()
    conn.close()
    return data


def add_tour(tour_name, tour_type, duration, transportation, departure_point, destination_id):
    conn = psycopg2.connect(CONN_STR)
    cursor = conn.cursor()
    cursor.callproc('zuev_g.insert_tour',
                    [tour_name, tour_type, duration, transportation, departure_point, destination_id])
    conn.commit()
    cursor.close()
    conn.close()


def delete_tour(tour_id):
    conn = psycopg2.connect(CONN_STR)
    cursor = conn.cursor()
    cursor.callproc("zuev_g.concatenate_hotel_data", (tour_id,))
    conn.commit()
    cursor.close()
    conn.close()


def change_transport(tour_id, new_transportation):
    conn = psycopg2.connect(CONN_STR)
    cursor = conn.cursor()
    cursor.callproc('zuev_g.update_tour_transportation', (tour_id, new_transportation))
    conn.commit()
    cursor.close()
    conn.close()


def search_tours_by_phrase(phrase):
    conn = psycopg2.connect(CONN_STR)
    cursor = conn.cursor()
    cursor.callproc("zuev_g.search_tours_by_phrase", (phrase,))
    tours = cursor.fetchall()
    cursor.close()
    conn.close()
    return tours


def run():
    choice = 0
    choices = {
        1: lambda: print(get_tour_info(int(input('Введите id: ')))),
        2: lambda: add_tour(input('Введите название: '), input('Введите тип: '),
                            int(input('Введите продолжительность: ')), input('Введите транспорт: '),
                            input('Введите пункт отправки: '), int(input('Введите id пункта назначения: '))),
        3: lambda: delete_tour(int(input('Введите id: '))),
        4: lambda: change_transport(int(input('Введите id: ')), input('Введите новый транспорт: ')),
        5: lambda: print(search_tours_by_phrase(input('Введите фразу: '))),
        6: lambda: print(hotel_data(input('id: '))),
        7: lambda: print(get_five_star_hotels()),
        8: lambda: print(get_pricelist_on_date(input('дата типа 2025-01-05: '))),
    }
    while choice != 9:
        print('1. print tour info')
        print('2. add tour')
        print('3. delete tour')
        print('4. change tour transport')
        print('5. search tour by phrase')
        print('6. hotel data')
        print('7. 5 star hotels')
        print('8. price list by date')
        print('9. EXIT')
        print('choose: ')
        choice = int(input())
        if choice in choices:
            choices[choice]()


if __name__ == '__main__':
    run()
