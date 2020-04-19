import os
import datetime
import operator

import sqlalchemy as sa


def make_datetime_with_dot(date: str):
    date_list = date.split('.')
    return datetime.datetime(int(date_list[2]), int(date_list[1]),
                             int(date_list[0]))


def make_float_from_str(data):
    data = str(data)
    if data[0] == '-':  # if temperature is negative
        return float(data.replace(',', '.').strip("-")) * (-1)
    return float(data.replace(',', '.'))


def make_datetime(date: str):
    date_list = date.split('-')
    return datetime.datetime(int(date_list[0]), int(date_list[1]),
                             int(date_list[2]))


def get_info_from_db(db_path, city, period_start, period_end):
    engine = sa.create_engine(f'sqlite:///{db_path}', echo=True)
    meta = sa.MetaData()
    conn = engine.connect()
    days = sa.Table(
        'day', meta,
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('time', sa.String),
        sa.Column('temperature', sa.String),
        sa.Column('winder_direction', sa.String),
        sa.Column('winder_speed', sa.Float),
        sa.Column('precipitation', sa.String),
        sa.Column('city_name', sa.String),
        sa.Column('year', sa.Integer)
    )
    time, temperature, winder_direction = sa.Column("time"), sa.Column("temperature"), \
                                          sa.Column("winder_direction")
    winder_speed, precipitation = sa.Column("winder_speed"), sa.Column("precipitation")
    stmt = sa.select([time, temperature, winder_direction, winder_direction, winder_speed, precipitation])
    s = stmt.where(
        (days.c.city_name == city) &
        (sa.between(days.c.year, period_start.year, period_end.year)))
    result = conn.execute(s)
    return result


def make_statistics(city: str, period_start: datetime, period_end: datetime):
    start_date_req = datetime.datetime(2010, 1, 1)
    end_data_req = datetime.datetime(2019, 7, 13)
    root_dir = os.getcwd()
    db_path = os.path.join(root_dir, 'weather_statistics_app', 'db', 'cities.db')
    statistics = {
        'city': city,
        'period_start': period_start,
        'period_end': period_end,
        'temperature_statistics': {
            'abs_min': None,
            'abs_max': None,
            'avg_temperature': None
        },
        'precipation_statistics': {
            'percentage_of_days_with_precipitation': None,
            'percentage_of_days_without_precipitation': None,
            'frequent_precipation': None,
            'second_frequent_precipation': None
        },
        'wind_statistics': {
            'frequent_direction': None,
            'avg_wind_speed': None
        }
    }

    if (period_start >= start_date_req) and (period_end <= end_data_req) and \
            (period_start <= period_end):
        result = get_info_from_db(db_path, city, period_start, period_end)
        statistics = prepare_statistics(result, period_start, period_end, statistics)

    return statistics


def prepare_statistics(db_rows, period_start, period_end, statistics):
    max_temperatures = []
    min_temperatures = []
    avg_temperatures = []
    wind_speed = []
    wind_directions_set = set()
    wind_directions = []
    curr_year_temperatures = []
    is_precipitation = []
    precipation_set = set()
    precipation_list = []

    prev_year = period_start.year
    for row in db_rows:
        date = make_datetime_with_dot(row[0].split()[0])
        if period_start <= date <= period_end:
            curr_year = date.year

            # temparature statistics
            if row[1] is not None:
                curr_year_temperatures.append(make_float_from_str(row[1]))
                if curr_year > prev_year:
                    prev_year = curr_year
                    min_temperatures.append(min(curr_year_temperatures))
                    max_temperatures.append(max(curr_year_temperatures))
                    avg_temperatures.append(average(curr_year_temperatures))
                    curr_year_temperatures.clear()

            # wind directions statistics
            if row[2] is not None:
                wind_directions_set.add(row[2])
                wind_directions.append(row[2])
            if row[3] is not None:
                wind_speed.append(float(row[3]))

            # precipation statistics
            if row[4] is not None:
                precipation_set.add(row[4])
                precipation_list.append(row[4])
                is_precipitation.append(1)
            else:
                is_precipitation.append(0)

    if (period_end.year - period_start.year) > 1:
        statistics['temperature_statistics']['avg_max_temperature'] = \
            round(average(max_temperatures), 2)
        statistics['temperature_statistics']['avg_min_temperature'] = \
            round(average(min_temperatures), 2)
    else:
        min_temperatures = curr_year_temperatures
        max_temperatures = curr_year_temperatures
        avg_temperatures = curr_year_temperatures

    statistics['temperature_statistics']['abs_min'] = min(min_temperatures)
    statistics['temperature_statistics']['abs_max'] = max(max_temperatures)
    statistics['temperature_statistics']['avg_temperature'] = round(average(avg_temperatures), 2)
    statistics['wind_statistics']['avg_wind_speed'] = \
        round(average(wind_speed), 2)
    wind_directions_dict = dict.fromkeys(frozenset(wind_directions_set))
    for direction in wind_directions_dict.keys():
        wind_directions_dict[direction] = wind_directions.count(direction)
    statistics['wind_statistics']['frequent_direction'] = max(
        wind_directions_dict.items(), key=operator.itemgetter(1))[0]

    path_to_prec_stats = statistics['precipation_statistics']
    percent_of_days_with_precip = int(round(sum(is_precipitation) /
                                            len(is_precipitation), 2) * 100)
    path_to_prec_stats['percentage_of_days_without_precipitation'] = \
        100 - percent_of_days_with_precip
    path_to_prec_stats['percentage_of_days_with_precipitation'] = \
        percent_of_days_with_precip
    if precipation_set:
        precip_dict = dict.fromkeys(frozenset(precipation_set))
        for precipation in precip_dict.keys():
            precip_dict[precipation] = precipation_list.count(direction)
        freq_precipation = max(precip_dict.items(),
                               key=operator.itemgetter(1))[0]
        path_to_prec_stats['frequent_precipation'] = freq_precipation
        precip_dict.pop(freq_precipation)
        if precip_dict.keys():
            path_to_prec_stats['second_frequent_precipation'] = \
                max(precip_dict.items(), key=operator.itemgetter(1))[0]
        else:
            path_to_prec_stats['frequent_precipation'] = "Нет осадков"
    else:
        path_to_prec_stats['frequent_precipation'] = "Нет осадков"
        path_to_prec_stats['second_frequent_precipation'] = "Нет осадков"

    return statistics


def average(lst):
    return sum(lst) / len(lst)