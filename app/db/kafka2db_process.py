from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta
import requests
from confluent_kafka import Producer, Consumer, KafkaException
import json
import pendulum
import psycopg2
from psycopg2 import sql
from insert_data_to_db import insert_sport_event_query, insert_competitors_query, insert_venue_query, insert_period_scores_query
import logging

# airflow 실행(pyenv activate doto)
# nohup airflow webserver --port 8880 > ~/airflow/logs/webserver.log 2>&1 &
# nohup airflow scheduler > ~/airflow/logs/scheduler.log 2>&1 &

# Kafka 설정
KAFKA_TOPIC = 'airflow2kafka0'
KAFKA_BOOTSTRAP_SERVERS = '172.31.14.224:9092'

logging.basicConfig(level=logging.INFO)

def send_data_kafka2db():
    conf = {
        'bootstrap.servers': f'{KAFKA_BOOTSTRAP_SERVERS}',  # Kafka 서버 주소
        'group.id': '2', # logstash, 2
        'auto.offset.reset': 'latest',  # 'latest', 'earliest'
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
        message = msg.value().decode('utf-8')
        data = json.loads(message)
        print('data :', data)

        insert_sport_event_query(data)
        insert_competitors_query(data)
        insert_venue_query(data)
        insert_period_scores_query(data)
    consumer.close()


if __name__ == '__main__':
    send_data_kafka2db()
