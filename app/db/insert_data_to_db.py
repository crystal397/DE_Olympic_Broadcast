from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta
import requests
from confluent_kafka import Producer, Consumer, KafkaException
import json
import pendulum
import psycopg2
from psycopg2 import sql


def insert_sport_event_query(data: dict) -> None:
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
                INSERT INTO sport_event (
                    id, start_time, start_time_confirmed, sport_name, category_name,
                    competition_name, competition_gender, season_name, season_start_date,
                    season_end_date, stage_order, stage_type, stage_phase, round_number,
                    group_id, group_name, status, match_status, home_score, away_score, winner_id
                ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                """
            )

            # competitors 데이터를 데이터베이스에 삽입
            for event in data['summaries']:
                sport_event = event['sport_event']
                sport_event_context = sport_event['sport_event_context']
                sport_event_status = sport_event['sport_event_status']
                cursor.execute(insert_query, (
                    sport_event['id'],
                    sport_event['start_time'],
                    sport_event['start_time_confirmed'],
                    sport_event_context['sport']['name'],
                    sport_event_context['category']['name'],
                    sport_event_context['competition']['name'],
                    sport_event_context['competition']['gender'],
                    sport_event_context['season']['name'],
                    sport_event_context['season']['start_date'],
                    sport_event_context['season']['end_date'],
                    sport_event_context['stage']['order'],
                    sport_event_context['stage']['type'],
                    sport_event_context['stage']['phase'],
                    sport_event_context['round']['number'],
                    sport_event_context['groups'][0]['id'],
                    sport_event_context['groups'][0]['name'],
                    sport_event_status['status'],
                    sport_event_status['match_status'],
                    sport_event_status['home_score'],
                    sport_event_status['away_score'],
                    sport_event_status['winner_id']
                ))

                connection.commit()


    except (Exception, psycopg2.Error) as error:
        print("Error while inserting to PostgreSQL", error)
    finally:
        if connection:
            connection.close()


def insert_competitors_query(data: dict) -> None:
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
                INSERT INTO competitors (
                    competitor_id, event_id, name, country, country_code,
                    abbreviation, qualifier, gender
                ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                """
            )

            # competitors 데이터를 데이터베이스에 삽입
            for event in data['summaries']:
                sport_event = event['sport_event']
                for competitor in sport_event['competitors']:
                    cursor.execute(insert_query, (
                        competitor['id'],
                        sport_event['id'],
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


def insert_venue_query(data: dict) -> None:
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
                INSERT INTO venue (
                    id, name, city_name, country_name, map_coordinates, country_code, timezone
                ) VALUES (%s, %s, %s, %s, %s, %s, %s)
                """
            )

            # competitors 데이터를 데이터베이스에 삽입
            for event in data['summaries']:
                venue = event['sport_event']['venue']
                cursor.execute(insert_query, (
                    venue['id'],
                    venue['name'],
                    venue['city_name'],
                    venue['country_name'],
                    venue['map_coordinates'],
                    venue['country_code'],
                    venue['timezone']
                ))
                connection.commit()


    except (Exception, psycopg2.Error) as error:
        print("Error while inserting to PostgreSQL", error)
    finally:
        if connection:
            connection.close()


def insert_period_scores_query(data: dict) -> None:
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
                INSERT INTO period_scores (
                    event_id, period_number, home_score, away_score, period_type
                ) VALUES (%s, %s, %s, %s, %s)
                """
            )

            # competitors 데이터를 데이터베이스에 삽입
            for event in data['summaries']:
                sport_event_id = event['sport_event']['id']
                period_scores = event['sport_event']['sport_event_status']['period_scores']
                for period_score in period_scores:
                    cursor.execute(insert_query, (
                        sport_event_id,
                        period_score['number'],
                        period_score['home_score'],
                        period_score['away_score'],
                        period_score['type']
                    ))
                connection.commit()


    except (Exception, psycopg2.Error) as error:
        print("Error while inserting to PostgreSQL", error)
    finally:
        if connection:
            connection.close()
