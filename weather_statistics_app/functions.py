import datetime
import os
import operator


def make_statistics(city: str, period_start: datetime, period_end: datetime):
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

    start_date_req = datetime.datetime(2010, 1, 1)
    end_data_req = datetime.datetime(2019, 7, 13)
    if (period_start >= start_date_req) and (period_end <= end_data_req) and \
            (period_start <= period_end):
        for year in range(period_start.year, period_end.year + 1):
            root_dir = os.getcwd()
            cities_path = os.path.join(root_dir, 'weather_statistics_app', 'cities')
            filename = os.path.join(cities_path, city, str(year))
            filename = f'{filename}.csv'
            opened_file = open(filename)
            file_content = opened_file.readlines()
            opened_file.close()
            info_about_every_day = str(file_content).split("\\n',")

            curr_year_temperatures.clear()
            for day in range(len(info_about_every_day)):
                weather_info = info_about_every_day[day].split(';')
                date_without_time = str(weather_info[0]).replace("'", '')
                date_without_time = date_without_time.split(' ')
                curr_date = date_without_time[0]
                if curr_date == '':
                    curr_date = date_without_time[1]
                curr_date = str(curr_date).replace(' ', '').replace('[', '')

                curr_date_datetime = make_datetime_with_dot(curr_date)
                if curr_date_datetime >= period_start and \
                        curr_date_datetime <= period_end:
                    #  temperature_information
                    if weather_info[1] != '':
                        curr_temperature = make_float_from_str(weather_info[1])
                        curr_year_temperatures.append(curr_temperature)
                    #  wind_information
                    if weather_info[3] != '':
                        wind_speed.append(float(weather_info[3]))
                    if weather_info[2] != '':
                        wind_directions_set.add(weather_info[2])
                        wind_directions.append(weather_info[2])
                    #  precipitation_information
                    if weather_info[4] == '' or \
                            weather_info[4] == '\\n\']':
                        is_precipitation.append(0)
                    else:
                        is_precipitation.append(1)
                        curr_precipation = weather_info[4].replace('.', '')
                        precipation_list.append(curr_precipation.rstrip(',').
                                                replace('\\n\']', ''))
                        precipation_set.add(curr_precipation)

            min_temperatures.append(min(curr_year_temperatures))
            max_temperatures.append(max(curr_year_temperatures))
            avg_temperatures.append(round(sum(curr_year_temperatures) /
                                          len(curr_year_temperatures), 2))

        if (period_end.year - period_start.year) > 1:
            statistics['temperature_statistics']['avg_max_temperature'] = \
                round(sum(max_temperatures) / len(max_temperatures), 2)
            statistics['temperature_statistics']['avg_min_temperature'] = \
                round(sum(min_temperatures) / len(min_temperatures), 2)
        statistics['temperature_statistics']['abs_min'] = min(min_temperatures)
        statistics['temperature_statistics']['abs_max'] = max(max_temperatures)
        statistics['temperature_statistics']['avg_temperature'] = round(sum(
            avg_temperatures) / len(avg_temperatures), 2)

        statistics['wind_statistics']['avg_wind_speed'] = \
            round(sum(wind_speed) / len(wind_speed), 2)
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


def make_datetime(date: str):
    date_list = date.split('-')
    return datetime.datetime(int(date_list[0]), int(date_list[1]),
                             int(date_list[2]))


def make_datetime_with_dot(date: str):
    date_list = date.split('.')
    return datetime.datetime(int(date_list[2]), int(date_list[1]),
                             int(date_list[0]))


def make_float_from_str(data):
    if data[0] == '-':  # if temperature is negative
        return float(data.replace(',', '.').strip("-")) * (-1)
    return float(data.replace(',', '.'))