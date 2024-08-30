import requests
import pika
import json
from datetime import datetime, timedelta


def fetch_weather_data():
    latitude = 55.7558
    longitude = 37.6173
    start_date = (datetime.now() - timedelta(days=30)).strftime('%Y-%m-%d')
    end_date = datetime.now().strftime('%Y-%m-%d')

    url = f"https://api.open-meteo.com/v1/forecast?latitude={latitude}&longitude={longitude}&daily=temperature_2m_max,"\
          f"temperature_2m_min,apparent_temperature_max,apparent_temperature_min,precipitation_sum,wind_speed_10m_max,"\
          f"wind_gusts_10m_max,wind_direction_10m_dominant,sunrise,sunset&timezone=Europe%2FMoscow&" \
          f"start_date={start_date}&end_date={end_date}"

    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Failed to fetch data: {response.status_code}")
        return None


def send_to_rabbitmq(data):
    # credential = pika.PlainCredentials('user', 'password')
    connection = pika.BlockingConnection(pika.ConnectionParameters('rabbitmq', port=5672))
    print(222222222222222222)
    channel = connection.channel()

    channel.queue_declare(queue='weather_data')

    channel.basic_publish(exchange='',
                          routing_key='weather_data',
                          body=json.dumps(data))

    print(" [x] Sent data to RabbitMQ")
    connection.close()


if __name__ == "__main__":
    weather_data = fetch_weather_data()
    if weather_data:
        send_to_rabbitmq(weather_data)
        # Сохраняем данные в файл weather_data.json
        # with open('weather_data.json', 'w') as json_file:
        #     json.dump(weather_data, json_file, indent=4)
        # print("Данные о погоде успешно сохранены в weather_data.json")
        # send_to_rabbitmq(weather_data)
