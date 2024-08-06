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

![image (5)](https://github.com/user-attachments/assets/7a3cd3a8-962e-4fa4-aa2c-2a6b5bb94a62)
