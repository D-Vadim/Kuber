import psycopg2
from psycopg2 import sql, errors
from config import DATABASE


def get_db_connection():
    conn = psycopg2.connect(
        dbname=DATABASE['dbname'],
        user=DATABASE['user'],
        password=DATABASE['password'],
        host=DATABASE['host'],
        port=DATABASE['port']
    )

    return conn


# Функция для сохранения данных в базу данных
def save_weather_data_to_db(json_data):
    conn = get_db_connection()
    cursor = conn.cursor()

    daily_data = json_data['daily']

    print(" [x] Data start saving to DB")

    for i in range(len(daily_data['time'])):
        try:
            cursor.execute("""
                INSERT INTO public.monthly_data VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                """, (
                daily_data['time'][i],
                daily_data['temperature_2m_max'][i],
                daily_data['temperature_2m_min'][i],
                daily_data['apparent_temperature_max'][i],
                daily_data['apparent_temperature_min'][i],
                daily_data['precipitation_sum'][i],
                daily_data['wind_speed_10m_max'][i],
                daily_data['wind_gusts_10m_max'][i],
                daily_data['wind_direction_10m_dominant'][i],
                daily_data['sunrise'][i][-5:],
                daily_data['sunset'][i][-5:]
            ))
        except errors.UniqueViolation:
            print(f"Entry for date {daily_data['time'][i]} already exists. Skipping insert.")
            conn.rollback()  # Отмена текущей транзакции перед продолжением

    # Сохранение изменений и закрытие соединения
    conn.commit()
    cursor.close()
    conn.close()


# Функция для получения данных из базы данных
def get_data_from_db(sql_query):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(sql_query)
    data = cursor.fetchall()
    conn.commit()
    cursor.close()
    conn.close()
    return data


'''
# Функция для получения данных из базы данных
def get_data_in_one_day_from_db(sql_query):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(sql_query)
    data = cursor.fetchall()
    conn.commit()
    cursor.close()
    conn.close()
    return data
'''


# Функция для очистки данных из базы данных
def clear_db():
    sql_query = "DELETE FROM monthly_data;"
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(sql_query)
    conn.commit()
    cursor.close()
    conn.close()
