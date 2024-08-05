from confluent_kafka import Producer, Consumer, KafkaException
import json
from insert_data_to_tt_db import insert_sport_event_query, insert_competitors_query, insert_venue_query, insert_period_scores_query
import logging

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

        if isinstance(data, dict) and data == {'message': 'Limit Exceeded'}:
            print("오류! {'message': 'Limit Exceeded'}입니다.")
            continue
        else:
            print('data :', data)
            pass

        sport_event_context = data['summaries'][0]['sport_event']['sport_event_context']
        if sport_event_context.get('sport', {}).get('name') == '탁구':
            insert_sport_event_query(data)
            insert_competitors_query(data)
            insert_venue_query(data)
            insert_period_scores_query(data)
        else:
            print(f"핸드볼 데이터가 아닙니다. {sport_event_context.get('sport', {}).get('name')}입니다.")
    consumer.close()


if __name__ == '__main__':
    send_data_kafka2db()
