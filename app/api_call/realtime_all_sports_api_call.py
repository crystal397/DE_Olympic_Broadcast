import requests
from confluent_kafka import Producer, Consumer, KafkaException
import json
import time

'''
sport = 'tabletennis'
urn_season = 'sr%3Aseason%3A105599'  # 올림픽 토너먼트 탁구 단식 남자 2024 sr:season:105599
urn_season = 'sr%3Aseason%3A105603'  # 올림픽 토너먼트 탁구 단식 여자 2024 sr:season:105603
urn_season = 'sr%3Aseason%3A105601'  # 올림픽 토너먼트 탁구 복식 남자 2024 sr:season:105601
urn_season = 'sr%3Aseason%3A105605'  # 올림픽 토너먼트 탁구 복식 여자 2024 sr:season:105605

sport = 'beachvolleyball'
urn_season = 'sr%3Aseason%3A105521'  # 올림픽 토너먼트 비치 발리볼 남자 2024 sr:season:105521
urn_season = 'sr%3Aseason%3A105523'  # 올림픽 토너먼트 비치 발리볼 여자 2024 sr:season:105523
urn_season = 'sr%3Aseason%3A105521'  # 올림픽 토너먼트 비치 발리볼 남자 2024 sr:season:105521
urn_season = 'sr%3Aseason%3A105523'  # 올림픽 토너먼트 비치 발리볼 여자 2024 sr:season:105523

sport = 'badminton'
urn_season = 'sr%3Aseason%3A105549'  # 올림픽 토너먼트 배드민턴 단식 남자 2024 sr:season:105549
urn_season = 'sr%3Aseason%3A105515'  # 올림픽 토너먼트 배드민턴 단식 여자 2024 sr:season:105515
urn_season = 'sr%3Aseason%3A119999'  # 올림픽 토너먼트 배드민턴 복식 남자 2024 sr:season:119999
urn_season = 'sr%3Aseason%3A105551'  # 올림픽 토너먼트 배드민턴 복식 여자 2024 sr:season:105551
urn_season = 'sr%3Aseason%3A105553'  # 올림픽 토너먼트 배드민턴 복식 혼성 2024 sr:season:105553

sport = 'handball'
urn_season = 'sr%3Aseason%3A105529'  # 올림픽 토너먼트 핸드볼 남자 2024 sr:season:105529
urn_season = 'sr%3Aseason%3A105531'  # 올림픽 토너먼트 핸드볼 여자 2024 sr:season:105531
'''

sports = ['tabletennis', 'beachvolleyball', 'badminton', 'handball']
urn_season_codes = {
    'tabletennis': ['sr%3Aseason%3A105599', 'sr%3Aseason%3A105603', 'sr%3Aseason%3A105601', 'sr%3Aseason%3A105605'],
    'beachvolleyball': ['sr%3Aseason%3A105521', 'sr%3Aseason%3A105523', 'sr%3Aseason%3A105521', 'sr%3Aseason%3A105523'],
    'badminton': ['sr%3Aseason%3A105549', 'sr%3Aseason%3A105515', 'sr%3Aseason%3A119999', 'sr%3Aseason%3A105551', 'sr%3Aseason%3A105553'],
    'handball': ['sr%3Aseason%3A105529', 'sr%3Aseason%3A105531']
}

KAFKA_TOPIC = 'airflow2kafka0'
KAFKA_BOOTSTRAP_SERVERS = '172.31.14.224:9092'

def api_call(sport: str, urn_season: str) -> dict:
    # date = datetime.now().strftime('%Y-%m-%d')
    # date = '2024-07-30'

    api_key = "v2N0vnCAYCa1O6kJNvua38itKyxguVzln2MVwcAd"
    locale = 'ko'
    offset = '0'
    limit = '5'
    start = '0'

    url = f"https://api.sportradar.com/{sport}/trial/v2/{locale}/seasons/{urn_season}/summaries?offset={offset}&limit={limit}&start={start}&api_key={api_key}"
    headers = {"accept": "application/json"}
    response = requests.get(url, headers=headers)
    data = response.json()  # data: Dict
    # data = response.text
    return data


def send_data_to_kafka1(data: dict) -> None:
    producer = Producer({'bootstrap.servers': KAFKA_BOOTSTRAP_SERVERS})

    def delivery_report(err, data):
        if err is not None:
            print('Message delivery failed: {}'.format(err))
        else:
            print('Message delivered to {}'.format(data))

    producer.produce(KAFKA_TOPIC, value=json.dumps(data), callback=delivery_report)
    # value : str
    producer.poll(1)
    producer.flush()


if __name__ == '__main__':
    try:
        while True:
            for sport in sports:
                for urn_season in urn_season_codes[sport]:
                    data = api_call(sport, urn_season)
                    send_data_to_kafka1(data)
                    print(data)
                    time.sleep(1)
    except KeyboardInterrupt:
        print("프로그램이 중지되었습니다.")
