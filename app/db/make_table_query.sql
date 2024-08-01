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
    winner_id VARCHAR
);
-- ALTER TABLE sport_event ADD CONSTRAINT unique_sport_event_id UNIQUE (id);


-- 참가자 정보 테이블
CREATE TABLE competitors (
    competitor_id VARCHAR,
    event_id VARCHAR, -- REFERENCES sport_event(id),
    name VARCHAR,
    country VARCHAR,
    country_code VARCHAR,
    abbreviation VARCHAR,
    qualifier VARCHAR,
    gender VARCHAR,
    PRIMARY KEY (competitor_id, event_id)
);
-- ALTER TABLE competitors ADD CONSTRAINT unique_competitor_id UNIQUE (competitor_id, event_id);

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
-- ALTER TABLE venue ADD CONSTRAINT unique_venue_id UNIQUE (id);

-- 세부 점수 테이블
CREATE TABLE period_scores (
    id SERIAL PRIMARY KEY,
    event_id VARCHAR, -- REFERENCES sport_event(id),
    period_number INTEGER,
    home_score INTEGER,
    away_score INTEGER,
    period_type VARCHAR
);
-- ALTER TABLE period_scores ADD CONSTRAINT unique_period_scores_id UNIQUE (id);

-- drop table sport_event, competitors, venue, period_scores;
