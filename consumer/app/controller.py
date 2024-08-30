import json
import os
import pika
from database import save_weather_data_to_db, get_data_from_db, clear_db


def degrees_to_direction(degrees):
    directions = ["N", "NNE", "NE", "ENE", "E", "ESE", "SE", "SSE",
                  "S", "SSW", "SW", "WSW", "W", "WNW", "NW", "NNW"]
    index = round(degrees / 22.5) % 16
    return directions[index]


def callback(ch, method, properties, body):
    print(" [x] Received data from RabbitMQ")
    data = json.loads(body)
    save_weather_data_to_db(data)
    print(" [x] Data saved to DB")


def start_consuming():
    # credentials = pika.PlainCredentials('user', 'password')
    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost', port=5672))
    ### connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))

    channel = connection.channel()

    channel.queue_declare(queue='weather_data')

    channel.basic_consume(queue='weather_data',
                          on_message_callback=callback,
                          auto_ack=True)

    print(' [*] Waiting for messages. To exit press CTRL+C')
    channel.start_consuming()

