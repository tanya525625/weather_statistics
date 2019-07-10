from copy import copy
import operator
import datetime


def make_statistics(city: str, period_start: datetime, period_end: datetime):
    
    max_temperatures = []
    min_temperatures = []
    avg_temperatures = []
    wind_speed = []
    wind_directions_set = set()
    wind_directions = []
    curr_year_temperatures = []
    
    for year in range(period_start.year, period_end.year + 1):
        filename = '.\\' + city + '\\' + str(year) + '.csv'
        opened_file = open(filename)
        file_content = opened_file.readlines()
        opened_file.close()
        info_about_every_day_from_the_period = str(file_content).split("\\n',")

        curr_year_temperatures.clear()
        for day in range(len(info_about_every_day_from_the_period)):
            curr_date_weather_info = info_about_every_day_from_the_period[day].split(';')
            date_without_time_list = str(curr_date_weather_info[0]).replace("'", '').split(' ')
            curr_date = date_without_time_list[0]
            if curr_date == '':
                curr_date = date_without_time_list[1]
            curr_date = str(curr_date).replace(' ', '').replace('[', '')
  
            curr_date_datetime = make_datetime(curr_date)
            if curr_date_datetime.day >= period_start.day and curr_date_datetime.month >= period_start.month and \
                curr_date_datetime.day <= period_end.day and curr_date_datetime.month <= period_end.month:
                #temperature_information
                curr_temperature = make_float_from_str(curr_date_weather_info[1])
                curr_year_temperatures.append(curr_temperature)
                #wind_information
                wind_speed.append(float(curr_date_weather_info[3]))
                wind_directions_set.add(curr_date_weather_info[2])
                wind_directions.append(curr_date_weather_info[2])

        min_temperatures.append(min(curr_year_temperatures))
        max_temperatures.append(max(curr_year_temperatures))
        avg_temperatures.append(round(sum(curr_year_temperatures)/len(curr_year_temperatures), 2))

    print(min_temperatures)
    print(max_temperatures)
    print(avg_temperatures)
    abs_min = min(min_temperatures)
    abs_max = max(max_temperatures)

    avg_wind_speed = round(sum(wind_speed)/len(wind_speed), 2)
    print(avg_wind_speed)
    wind_directions_dict = dict.fromkeys(frozenset(wind_directions_set))
    for direction in wind_directions_dict.keys():
        wind_directions_dict[direction] = wind_directions.count(direction)
    frequent_direction = max(wind_directions_dict.items(), key=operator.itemgetter(1))[0]
    print(frequent_direction)

    
       
def make_datetime(date: str):
    date_list = date.split('.')
    #print(date_list)
    return datetime.datetime(int(date_list[2]), int(date_list[1]), int(date_list[0]))

def make_float_from_str(data):
    if data[0] == '-': # if negative temperature
        return float(data.replace(',', '.').strip("-")) * (-1)
    return float(data.replace(',', '.'))


test = "10.01.2018"
test2 = "16.03.2019"
data1 = make_datetime(test)
data2 = make_datetime(test2)


make_statistics("Санкт-Петербург", data1, data2)