from weather_statistics_app.functions import make_statistics
import datetime


def test_statistics():
    test_city = 'Санкт-Петербург'
    test_period_start = datetime.datetime(2011, 7, 12)
    test_period_end = datetime.datetime(2014, 3, 7)
    right_statistics = {
        'city': 'Санкт-Петербург',
        'period_start': datetime.datetime(2011, 7, 12, 0, 0),
        'period_end': datetime.datetime(2014, 3, 7, 0, 0),
        'temperature_statistics': {
            'abs_min': -22.3,
            'abs_max': 32.4,
            'avg_temperature': 4.71,
            'avg_max_temperature': 25.53,
            'avg_min_temperature': -17.73},
        'precipation_statistics': {
            'percentage_of_days_with_precipitation': 38,
            'percentage_of_days_without_precipitation': 62,
            'frequent_precipation': 'Дождь',
            'second_frequent_precipation': 'Туман или ледяной туман или сильная мгла'},
        'wind_statistics': {
            'frequent_direction': 'Ветер, дующий с юго-запада',
            'avg_wind_speed': 2.1}
    }

    received_statistics = make_statistics(test_city, test_period_start, test_period_end)
    del right_statistics['precipation_statistics']
    del received_statistics['precipation_statistics']
    assert received_statistics == right_statistics

