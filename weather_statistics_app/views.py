from django.shortcuts import render
from django.http import HttpResponse
from .forms import UserForm
import operator
import datetime
 

def index(request):
    if request.method == "POST":
        city = request.POST.get("option")
        period_start = request.POST.get("period_start")
        period_end = request.POST.get("period_end")
        period_start = make_datetime(period_start)
        period_end = make_datetime(period_end)
        statistics_info = make_statistics(city, period_start, period_end)
        return render(request, 'weather_statistics_app/statistics.html', 
                      statistics_info)
    else:
        userform = UserForm()
        return render(request, "index.html", {"form": userform})


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
    
    if (period_start.year >= 2010) and (period_end.year <= 2019):
        for year in range(period_start.year, period_end.year + 1):
            filename = '.\\weather_statistics_app\\cities\\' + city + '\\' + \
                                                        str(year) + '.csv'
            opened_file = open(filename)
            file_content = opened_file.readlines()
            opened_file.close()
            info_about_every_day = str(file_content).split("\\n',")

            curr_year_temperatures.clear()
            for day in range(len(info_about_every_day)):
                curr_date_weather_info = info_about_every_day[day].split(';')
                date_without_time_list = str(curr_date_weather_info[0]). \
                                             replace("'", '').split(' ')
                curr_date = date_without_time_list[0]
                if curr_date == '':
                    curr_date = date_without_time_list[1]
                curr_date = str(curr_date).replace(' ', '').replace('[', '')
    
                curr_date_datetime = make_datetime_with_dot(curr_date)
                if curr_date_datetime >= period_start and \
                   curr_date_datetime <= period_end:
                    #  temperature_information
                    if curr_date_weather_info[1] != '':
                        curr_temperature = make_float_from_str(curr_date_weather_info[1])
                        curr_year_temperatures.append(curr_temperature)
                    #  wind_information
                    if curr_date_weather_info[3] != '':
                        wind_speed.append(float(curr_date_weather_info[3]))
                    if curr_date_weather_info[2] != '':
                        wind_directions_set.add(curr_date_weather_info[2])
                        wind_directions.append(curr_date_weather_info[2])
                    #  precipitation_information
                    if curr_date_weather_info[4] == '' or \
                       curr_date_weather_info[4] == '\\n\']':
                        is_precipitation.append(0)
                    else:
                        is_precipitation.append(1)
                        curr_precipation = curr_date_weather_info[4].replace('.', '')
                        precipation_list.append(curr_precipation.rstrip(','). 
                                                replace('\\n\']', ''))
                        precipation_set.add(curr_precipation)
                    
            min_temperatures.append(min(curr_year_temperatures))
            max_temperatures.append(max(curr_year_temperatures))
            avg_temperatures.append(round(sum(curr_year_temperatures) /
                                    len(curr_year_temperatures), 2))
        
        if (period_end.year - period_start.year) > 1:
            statistics['temperature_statistics']['avg_max_temperature'] =\
                    round(sum(max_temperatures)/len(max_temperatures), 2)
            statistics['temperature_statistics']['avg_min_temperature'] =\
                    round(sum(min_temperatures)/len(min_temperatures), 2)
        statistics['temperature_statistics']['abs_min'] = min(min_temperatures)
        statistics['temperature_statistics']['abs_max'] = max(max_temperatures)
        statistics['temperature_statistics']['avg_temperature'] = round(sum(avg_temperatures) /
                                                                  len(avg_temperatures), 2)

        statistics['wind_statistics']['avg_wind_speed'] = round(sum(wind_speed) /
                                                          len(wind_speed), 2)
        wind_directions_dict = dict.fromkeys(frozenset(wind_directions_set))
        for direction in wind_directions_dict.keys():
            wind_directions_dict[direction] = wind_directions.count(direction)
        statistics['wind_statistics']['frequent_direction'] = max(wind_directions_dict.items(), 
                                                                  key=operator.itemgetter(1))[0]

        percentage_of_days_with_precipitation = int(round(sum(is_precipitation) /
                                                len(is_precipitation), 2) * 100)
        statistics['precipation_statistics']['percentage_of_days_without_precipitation'] =\
                                               100 - percentage_of_days_with_precipitation
        statistics['precipation_statistics']['percentage_of_days_with_precipitation'] =\
                                                percentage_of_days_with_precipitation
        if precipation_set:
            precipation_dict = dict.fromkeys(frozenset(precipation_set))
            for precipation in precipation_dict.keys():
                precipation_dict[precipation] = precipation_list.count(direction)
            frequent_precipation = max(precipation_dict.items(), key=operator.itemgetter(1))[0]
            statistics['precipation_statistics']['frequent_precipation'] = frequent_precipation
            precipation_dict.pop(frequent_precipation)
            if precipation_dict.keys():
                statistics['precipation_statistics']['second_frequent_precipation'] =\
                           max(precipation_dict.items(), key=operator.itemgetter(1))[0]
            else:
                statistics['precipation_statistics']['frequent_precipation'] = "Нет осадков"
        else:
            statistics['precipation_statistics']['frequent_precipation'] = "Нет осадков"
            statistics['precipation_statistics']['second_frequent_precipation'] = "Нет осадков"
        
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
    if data[0] == '-':  # if negative temperature
        return float(data.replace(',', '.').strip("-")) * (-1)
    return float(data.replace(',', '.'))