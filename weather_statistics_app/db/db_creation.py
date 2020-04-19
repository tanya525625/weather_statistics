import sqlite3
import pandas as pd
import os


conn = sqlite3.connect("cities.db")
cursor = conn.cursor()


def create_city_table(conn, cursor):
    cursor.execute('CREATE TABLE city (name STRING UNIQUE, PRIMARY KEY (name))')
    cities_list = ('Берлин', 'Владивосток', 'Екатеринбург', 'Минск', 'Москва',
                   'Нижний Новгород', 'Омск', 'Осло',  'Пермь', 'Прага',
                   'Ростов-на-Дону', 'Самара', 'Санкт-Петербург', 'Хельсинки', 'Челябинск')
    for city in cities_list:
        cursor.execute(f'INSERT INTO city (name) VALUES ("{city}")')

    conn.commit()


def create_year_table(conn, cursor):
    cities = get_posts('city')
    cursor.execute("CREATE TABLE year (id INTEGER PRIMARY KEY NOT NULL, "
                   "year INTEGER, "
                   "city_name STRING REFERENCES city (name))")
    values = []
    id = 0
    for city in cities:
        for year in range(2010, 2020):
            values.append((id, year, city[0]))
            id += 1
    cursor.executemany("INSERT INTO year VALUES (?,?,?)", values)
    conn.commit()


def create_day_table(conn, cursor):
    cities = get_posts('city')
    years = tuple(range(2010, 2020))

    cursor.execute("DROP TABLE day")
    cursor.execute("CREATE TABLE day (id INTEGER PRIMARY KEY NOT NULL, time DATETIME, temperature STRING, "
                   "winder_direction STRING, winder_speed DOUBLE, precipitation STRING, "
                   "city_name STRING REFERENCES city (name), year INTEGER REFERENCES year (year));")

    id = 0
    dir_path = os.path.join('..', 'cities')
    for city in cities:
        for year in years:
            file_path = os.path.join(dir_path, city[0], f'{year}.csv')
            df = pd.read_csv(file_path, sep=";")
            df_rows_count = len(df.index)
            df.columns = ['time', 'temperature', 'winder_direction', 'winder_speed', 'precipitation']
            df.index = list(range(id, id + df_rows_count))
            df.reset_index(level=0, inplace=True)
            df = df.assign(city=[city[0]] * df_rows_count)
            df = df.assign(year=[year] * df_rows_count)
            cursor.executemany("INSERT INTO day VALUES (?,?,?,?,?,?,?,?)", df.values.tolist())
            id = id + df_rows_count


    conn.commit()


def get_posts(table_name):
    with conn:
        cursor.execute(f"SELECT * FROM {table_name}")
        return cursor.fetchall()


create_day_table(conn, cursor)

