from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta
import requests
from confluent_kafka import Producer, Consumer, KafkaException
import json
import pendulum
import psycopg2
from psycopg2 import sql

# airflow 실행(pyenv activate doto)
# nohup airflow webserver --port 8880 > ~/airflow/logs/webserver.log 2>&1 &
# nohup airflow scheduler > ~/airflow/logs/scheduler.log 2>&1 &

# Kafka 설정
KAFKA_TOPIC = 'airflow2kafka0'
KAFKA_BOOTSTRAP_SERVERS = '172.31.14.224:9092'


def send_data_kafka2db():
    conf = {
        'bootstrap.servers': f'{KAFKA_BOOTSTRAP_SERVERS}',  # Kafka 서버 주소
        'group.id': '2', # logstash
        'auto.offset.reset': 'earliest',  # 'latest', 'earliest'
        'enable.auto.commit': True,  # 오프셋 자동 커밋 설정
        # 'session.timeout.ms': 10000,  # 세션 타임아웃 설정
    }

    consumer = Consumer(conf)

    consumer.subscribe([f'{KAFKA_TOPIC}'])  # 구독할 Kafka 토픽

    while True:
        msg = consumer.poll(3.0)
        print("msg :", msg)

        if msg is None:
            continue
        if msg.error():
            print("ERROR: %s".format(msg.error()))
        else:
            pass
        data = msg.value().decode('utf-8')
        print('data :', data)
        process_message(data)
    consumer.close()


def process_message(message: str) -> None:
    data = json.loads(message)

    try:
        connection = psycopg2.connect(
            dbname='test_handball',
            user='postgres',
            password='postgres',
            host='172.31.11.125',
            port='5432'
        )

        with connection.cursor() as cursor:
            # SQL 문 구성
            insert_query = sql.SQL(
                """
                INSERT INTO competitors (competitor_id, name, country, country_code, abbreviation, qualifier, gender)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
                """
            )

            # competitors 데이터를 데이터베이스에 삽입
            for competitor in data['summaries'][0]['sport_event']['competitors']:
                cursor.execute(insert_query, (
                    competitor['id'],
                    competitor['name'],
                    competitor['country'],
                    competitor['country_code'],
                    competitor['abbreviation'],
                    competitor['qualifier'],
                    competitor['gender']
                ))
                connection.commit()


    except (Exception, psycopg2.Error) as error:
        print("Error while inserting to PostgreSQL", error)
    finally:
        if connection:
            connection.close()


if __name__ == '__main__':
    send_data_kafka2db()
