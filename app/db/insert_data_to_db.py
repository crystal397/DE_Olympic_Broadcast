import psycopg2
from psycopg2 import sql


def insert_sport_event_query(data: dict) -> None:
    try:
        connection = psycopg2.connect(
            dbname='handball0',
            user='postgres',
            password='postgres',
            host='172.31.11.125',
            port='5432'
        )

        with connection.cursor() as cursor:
            insert_query = sql.SQL(
                """
                INSERT INTO sport_event (
                    id, start_time, start_time_confirmed, sport_name, category_name,
                    competition_name, competition_gender, season_name, season_start_date,
                    season_end_date, stage_order, stage_type, stage_phase, round_number,
                    group_id, group_name, status, match_status, home_score, away_score, winner_id, venue_id
                ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                ON CONFLICT (id) DO NOTHING
                """
            )

            for event in data['summaries']:
                sport_event = event['sport_event']
                sport_event_context = sport_event['sport_event_context']
                sport_event_status = event['sport_event_status']
                cursor.execute(insert_query, (
                    sport_event.get('id'),
                    sport_event.get('start_time'),
                    sport_event.get('start_time_confirmed'),
                    sport_event_context.get('sport', {}).get('name'),
                    sport_event_context.get('category', {}).get('name'),
                    sport_event_context.get('competition', {}).get('name'),
                    sport_event_context.get('competition', {}).get('gender'),
                    sport_event_context.get('season', {}).get('name'),
                    sport_event_context.get('season', {}).get('start_date'),
                    sport_event_context.get('season', {}).get('end_date'),
                    sport_event_context.get('stage', {}).get('order'),
                    sport_event_context.get('stage', {}).get('type'),
                    sport_event_context.get('stage', {}).get('phase'),
                    sport_event_context.get('round', {}).get('number'),
                    sport_event_context.get('groups', [{}])[0].get('id'),
                    sport_event_context.get('groups', [{}])[0].get('name'),
                    sport_event_status.get('status'),
                    sport_event_status.get('match_status'),
                    sport_event_status.get('home_score'),
                    sport_event_status.get('away_score'),
                    sport_event_status.get('winner_id'),
                    sport_event.get('venue_id')
                ))

            connection.commit()

    except (Exception, psycopg2.Error) as error:
        print("Error while inserting sport_event to PostgreSQL:", error)
    finally:
        if connection:
            connection.close()


def insert_competitors_query(data: dict) -> None:
    try:
        connection = psycopg2.connect(
            dbname='handball0',
            user='postgres',
            password='postgres',
            host='172.31.11.125',
            port='5432'
        )

        with connection.cursor() as cursor:
            insert_query = sql.SQL(
                """
                INSERT INTO competitors (
                    competitor_id, event_id, name, country, country_code,
                    abbreviation, qualifier, gender
                ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                ON CONFLICT (competitor_id, event_id) DO NOTHING
                """
            )

            for event in data['summaries']:
                sport_event = event['sport_event']
                for competitor in sport_event.get('competitors', []):
                    cursor.execute(insert_query, (
                        competitor.get('id'),
                        sport_event.get('id'),
                        competitor.get('name'),
                        competitor.get('country'),
                        competitor.get('country_code'),
                        competitor.get('abbreviation'),
                        competitor.get('qualifier'),
                        competitor.get('gender')
                    ))
                connection.commit()

    except (Exception, psycopg2.Error) as error:
        print("Error while inserting competitors to PostgreSQL:", error)
    finally:
        if connection:
            connection.close()


def insert_venue_query(data: dict) -> None:
    try:
        connection = psycopg2.connect(
            dbname='handball0',
            user='postgres',
            password='postgres',
            host='172.31.11.125',
            port='5432'
        )

        with connection.cursor() as cursor:
            insert_query = sql.SQL(
                """
                INSERT INTO venue (
                    id, name, city_name, country_name, map_coordinates, country_code, timezone
                ) VALUES (%s, %s, %s, %s, %s, %s, %s)
                ON CONFLICT (id) DO NOTHING
                """
            )

            for event in data['summaries']:
                venue = event['sport_event'].get('venue', {})
                cursor.execute(insert_query, (
                    venue.get('id'),
                    venue.get('name'),
                    venue.get('city_name'),
                    venue.get('country_name'),
                    venue.get('map_coordinates'),
                    venue.get('country_code'),
                    venue.get('timezone')
                ))
            connection.commit()

    except (Exception, psycopg2.Error) as error:
        print("Error while inserting venue to PostgreSQL:", error)
    finally:
        if connection:
            connection.close()


def insert_period_scores_query(data: dict) -> None:
    try:
        connection = psycopg2.connect(
            dbname='handball0',
            user='postgres',
            password='postgres',
            host='172.31.11.125',
            port='5432'
        )

        with connection.cursor() as cursor:
            insert_query = sql.SQL(
                """
                INSERT INTO period_scores (
                    event_id, period_number, home_score, away_score, period_type
                ) VALUES (%s, %s, %s, %s, %s)
                ON CONFLICT (event_id, period_number) DO NOTHING
                """
            )

            for event in data['summaries']:
                sport_event_id = event['sport_event']['id']
                period_scores = event['sport_event_status'].get('period_scores', [])
                for period_score in period_scores:
                    cursor.execute(insert_query, (
                        sport_event_id,
                        period_score.get('number'),
                        period_score.get('home_score'),
                        period_score.get('away_score'),
                        period_score.get('type')
                    ))
            connection.commit()

    except (Exception, psycopg2.Error) as error:
        print("Error while inserting period_scores to PostgreSQL:", error)
    finally:
        if connection:
            connection.close()