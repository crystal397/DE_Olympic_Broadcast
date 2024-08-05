-- 경기 정보 테이블
CREATE TABLE sport_event (
    id VARCHAR PRIMARY KEY,
    start_time TIMESTAMP,
    start_time_confirmed BOOLEAN,
    sport_name VARCHAR,
    category_name VARCHAR,
    competition_name VARCHAR,
    competition_gender VARCHAR,
    season_name VARCHAR,
    season_start_date DATE,
    season_end_date DATE,
    stage_order INTEGER,
    stage_type VARCHAR,
    stage_phase VARCHAR,
    round_number INTEGER,
    group_id VARCHAR,
    group_name VARCHAR,
    status VARCHAR,
    match_status VARCHAR,
    home_score INTEGER,
    away_score INTEGER,
    winner_id VARCHAR,
    venue_id VARCHAR
);
-- CONSTRAINT fk_venue FOREIGN KEY (venue_id) REFERENCES venue(id)

-- 참가자 정보 테이블
CREATE TABLE competitors (
    competitor_id VARCHAR,
    event_id VARCHAR,
    name VARCHAR,
    country VARCHAR,
    country_code VARCHAR,
    abbreviation VARCHAR,
    qualifier VARCHAR,
    gender VARCHAR,
    PRIMARY KEY (competitor_id, event_id)
);
--     CONSTRAINT fk_event FOREIGN KEY (event_id) REFERENCES sport_event(id)

-- 경기 장소 테이블
CREATE TABLE venue (
    id VARCHAR PRIMARY KEY,
    name VARCHAR,
    city_name VARCHAR,
    country_name VARCHAR,
    map_coordinates VARCHAR,
    country_code VARCHAR,
    timezone VARCHAR
);

-- 세부 점수 테이블
CREATE TABLE period_scores (
    id SERIAL PRIMARY KEY,
    event_id VARCHAR,
    period_number INTEGER,
    home_score INTEGER,
    away_score INTEGER,
    period_type VARCHAR
);
--     CONSTRAINT fk_event FOREIGN KEY (event_id) REFERENCES sport_event(id),
--     CONSTRAINT unique_event_period UNIQUE (event_id, period_number)

-- 외래 키 설정
ALTER TABLE sport_event
ADD CONSTRAINT fk_winner FOREIGN KEY (winner_id) REFERENCES competitors(competitor_id);
