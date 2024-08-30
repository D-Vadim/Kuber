import psycopg2
from psycopg2 import sql
from config import DATABASE


conn = psycopg2.connect(
    dbname=DATABASE['dbname'],
    user=DATABASE['user'],
    password=DATABASE['password'],
    host=DATABASE['host'],
    port=DATABASE['port']
)

cursor = conn.cursor()

# Создание таблицы monthly_data
cursor.execute("""
CREATE TABLE IF NOT EXISTS monthly_data
(
"time" text NOT NULL,
"temperature_2m_max" numeric NOT NULL,
"temperature_2m_min" numeric NOT NULL,
"apparent_temperature_max" numeric NOT NULL,
"apparent_temperature_min" numeric NOT NULL,
"precipitation_sum" numeric NOT NULL,
"wind_speed_10m_max" numeric NOT NULL,
"wind_gusts_10m_max"numeric NOT NULL,
"wind_direction_10m_dominant" integer NOT NULL,
"sunrise" text NOT NULL,
"sunset" text NOT NULL,
CONSTRAINT pk_monthly_data PRIMARY KEY ("time")
);
""")

conn.commit()
cursor.close()
conn.close()
