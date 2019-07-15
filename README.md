**Weather statistics** 
=====================
Сайт для просмотра погодной статистики за период: 01.01.2010 - 13.07.2019.
### Запуск
Для запуска сервера необходимо ввести в командной строке: "python manage.py runserver" (требуется библиотека Django).
### Работа с сайтом
Для того чтобы посмотреть погодную статистику, необходимо выбрать город и период времени, за который требуется узнать статистику, и нажать на кнопку "Получить статистику".
###### Доступный функционал на сайте:
* Температурные характеристики (абсолютный минимум за период, средняя температура,  абсолютный максимум за период, если период длиннее 2х лет, то можно посмотреть: средний максимум по годам и средний минимум по годам);
* Информация об осадках (в процентном соотношении число дней с осадками и без осадков за указанный период и 2 самых частых вида осадков за указанный период);
* Информация о ветре (Средняя скорость и направление ветра).
### Реализация проекта
Проект реализован на языке программирования Python с использованием библиотеки Django. Для верстки сайта были использованы CSS и язык разметки HTML.
