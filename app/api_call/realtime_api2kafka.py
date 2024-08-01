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


def api_call():
    api_key = "v2N0vnCAYCa1O6kJNvua38itKyxguVzln2MVwcAd"
    # date = datetime.now().strftime('%Y-%m-%d')
    date = '2024-07-30'
    url = f"https://api.sportradar.com/handball/production/v2/ko/schedules/{date}/summaries?offset=0&limit=1&api_key={api_key}"
    headers = {"accept": "application/json"}
    response = requests.get(url, headers=headers)
    data = response.json() # data: Dict
    # data = response.text
    return data


def send_data_to_kafka(**kwargs):
    ti = kwargs['ti']
    data = ti.xcom_pull(task_ids='api_call')

    producer = Producer({'bootstrap.servers': KAFKA_BOOTSTRAP_SERVERS})

    def delivery_report(err, msg):
        if err is not None:
            print('Message delivery failed: {}'.format(err))
        else:
            print('Message delivered to {} [{}]'.format(msg.topic(), msg.partition()))

    # producer.produce(KAFKA_TOPIC, key=str(record['id']), value=json.dumps(data), callback=delivery_report)
    producer.produce(KAFKA_TOPIC, value=json.dumps(data), callback=delivery_report)
    # value : str
    producer.poll(3)

    producer.flush()



default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(seconds=10),
}

# DAG 설정
with DAG(
        dag_id='realtime_api2kafka',
        schedule=None,  # "* * * * *",
        start_date=pendulum.datetime(2024, 7, 29, tz="Asia/Seoul"),
        catchup=False,
        default_args=default_args,
) as dag:
    api_call = PythonOperator(
        task_id='api_call',
        python_callable=api_call,
    )

    send_data_to_kafka_task = PythonOperator(
        task_id='send_data_to_kafka',
        python_callable=send_data_to_kafka,
    )

    api_call >> send_data_to_kafka_task