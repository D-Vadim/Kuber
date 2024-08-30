import json
import pika
import time
from datetime import datetime
from threading import Thread
from flask import Flask, render_template, request
from database import save_weather_data_to_db, get_data_from_db, clear_db
from controller import degrees_to_direction, start_consuming


app = Flask(__name__)


# Главная страница
@app.route('/')
def index():
    return render_template('index.html')


# Вывод погоды по конкретной дате
@app.route('/date_weather', methods=['GET', 'POST'])
def date_weather():
    if request.method == 'POST':
        date = request.form['date']
        sql_request = "SELECT * FROM monthly_data WHERE time = \'" + date + "\';"
        weather_data = get_data_from_db(sql_request)

        wind_degrees = weather_data[0][8]
        wind = f"{wind_degrees}° ({degrees_to_direction(wind_degrees)})"

        return render_template('date_weather.html', weather_data=weather_data, date=date, wind_direction=wind)

    return render_template('date_weather.html')


# Вывод погоды за последний месяц
@app.route('/month_weather')
def month_weather():
    sql_request = "SELECT * FROM monthly_data;"
    weather_data = get_data_from_db(sql_request)

    wind = []
    for day in range(len(weather_data)):
        wind.append(f"{weather_data[day][8]}° ({degrees_to_direction(weather_data[day][8])})")

    return render_template('month_weather.html',
                           weather_data=weather_data, wind_direction=wind, length=len(weather_data))


# Вывод погоды за промежуток дат
@app.route('/range_weather', methods=['GET', 'POST'])
def range_weather():
    if request.method == 'POST':
        start_date = request.form['start_date']
        end_date = request.form['end_date']
        sql_request = "SELECT * FROM monthly_data WHERE time BETWEEN \'" + start_date + "\' AND \'" \
                      + end_date + "\' ORDER BY time;"
        weather_data = get_data_from_db(sql_request)

        wind = []
        for day in range(len(weather_data)):
            wind.append(f"{weather_data[day][8]}° ({degrees_to_direction(weather_data[day][8])})")

        return render_template('range_weather.html', weather_data=weather_data,
                               start_date=start_date, end_date=end_date, wind_direction=wind, length=len(weather_data))

    return render_template('range_weather.html')


if __name__ == '__main__':
    # clear_db()

    consumer_thread = Thread(target=start_consuming)
    consumer_thread.start()

    app.run(debug=True)

    consumer_thread.join()



