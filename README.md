# DE_Olympic_Broadcast
2024 파리 올림픽 실시간 경기 데이터 기반 파이프라인 구축 및 스포츠 데이터 분석

## 데이터 흐름 요약 및 아키텍처 소개
### 1. API에서 데이터 호출
  - WebSocket 서버: 데이터를 Kafka와 WebSocket 클라이언트로 전송
  - Airflow: 배치 처리를 위한 데이터 호출

### 2. Kafka가 데이터 큐잉
  -  데이터를 PostgreSQL과 Logstash로 전달

### 3. PostgreSQL
  - 데이터 분석 및 쿼리에 사용할 데이터 저장

### 4. Logstash
  - Kafka에서 데이터를 수집하고 변환하여 Elastic search로 전송

### 5. Elastic search
  - 실시간 검색 및 분석을 위해 데이터를 인덱싱하고 저장

### 6. 시각화
  - Kibana: Elastic search 데이터를 시각화하여 실시간 대시보드와 리포트 제공
  - Spark/Jupyter Lab: PostgreSQL 데이터를 불러와서 데이터프레임 생성 및 시각화

![image](https://github.com/user-attachments/assets/9b495fbf-c7e9-4888-8f3a-eae1d42ccdbe)

서버1	서버2	서버3
Airflow: 8880	Elastic Search: 9200	PostgreSQL: 5432
Spark: 8080	Kibana: 5601	
Jupyter Lab: 8888		
Kafka: 9092		<img width="768" alt="image" src="https://github.com/user-attachments/assets/0ef0c145-f4e3-45b9-8a69-e1643e2029fb">
