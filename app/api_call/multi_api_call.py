from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta
import requests
from confluent_kafka import Producer
import json
import pendulum

# airflow 실행
# nohup airflow webserver --port 8880 > ~/airflow/logs/webserver.log 2>&1 &
# nohup airflow scheduler > ~/airflow/logs/scheduler.log 2>&1 &

# Kafka 설정
KAFKA_TOPIC = 'airflow2kafka0'
KAFKA_BOOTSTRAP_SERVERS = '172.31.14.224:9092'

def api_call(param):
    # 핸드볼 api로 바꿔야 할 부분
    api_key = "CgFIFfP8hc5XngDXfvNE26zWyoZH8PSx8JQH6hHG"
    schedules_live_timelines_url = f'{param}{api_key}'
    headers = {"accept": "application/json"}
    response = requests.get(schedules_live_timelines_url, headers=headers)
    data = response.json()
    return data

params = ['https://api.sportradar.com/handball/production/v2/ko/schedules/live/summaries?api_key=',
          'https://api.sportradar.com/handball/production/v2/en/schedules/live/timelines?api_key=']

def send_data_to_kafka(**kwargs):
    ti = kwargs['ti']
    all_data = []
    for i, param in enumerate(params):
        data = ti.xcom_pull(task_ids=f'task-{i}')
        all_data.append(data)

    producer = Producer({'bootstrap.servers': KAFKA_BOOTSTRAP_SERVERS})

    def delivery_report(err, msg):
        if err is not None:
            print('Message delivery failed: {}'.format(err))
        else:
            print('Message delivered to {} [{}]'.format(msg.topic(), msg.partition()))

    # producer.produce(KAFKA_TOPIC, key=str(record['id']), value=json.dumps(data), callback=delivery_report)
    producer.produce(KAFKA_TOPIC, value=json.dumps(all_data), callback=delivery_report)
    producer.poll(1)

    producer.flush()


default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

with DAG(
    dag_id='olympicGamesParis2024_handball',
    schedule=None,
    start_date=pendulum.datetime(2024, 7, 24, tz="Asia/Seoul"),
    catchup=False,
    default_args=default_args,
) as dag:

    tasks = []
    for i, param in enumerate(params):
        task_id = f'task-{i}'
        task = PythonOperator(
            task_id=task_id,
            python_callable=api_call,
            op_kwargs={'param': param},
            dag=dag,
        )
        tasks.append(task)

    send_data_task = PythonOperator(
        task_id='send_data_to_kafka',
        python_callable=send_data_to_kafka,
        provide_context=True,
        dag=dag,
    )

    for task in tasks:
        task >> send_data_task