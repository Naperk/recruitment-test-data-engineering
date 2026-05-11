#!/usr/bin/env python3

import csv
import time
import pymysql


def connect(retries=10, delay=3):
    for attempt in range(retries):
        try:
            return pymysql.connect(
                host='database',
                user='codetest',
                password='swordfish',
                database='codetest',
                charset='utf8mb4',
            )
        except pymysql.Error as e:
            if attempt < retries - 1:
                print(f"DB not ready ({e}), retrying in {delay}s...")
                time.sleep(delay)
            else:
                raise


def load_places(cursor):
    with open('/data/places.csv', encoding='utf-8') as f:
        for row in csv.DictReader(f):
            cursor.execute(
                "INSERT IGNORE INTO places (city, county, country) VALUES (%s, %s, %s)",
                (row['city'], row['county'], row['country']),
            )


def load_people(cursor):
    with open('/data/people.csv', encoding='utf-8') as f:
        for row in csv.DictReader(f):
            cursor.execute(
                """
                INSERT INTO people (given_name, family_name, date_of_birth, place_of_birth)
                SELECT %s, %s, %s, id FROM places WHERE city = %s
                """,
                (row['given_name'], row['family_name'], row['date_of_birth'], row['place_of_birth']),
            )


def main():
    conn = connect()
    try:
        with conn.cursor() as cur:
            load_places(cur)
            load_people(cur)
        conn.commit()
        print("Ingest complete.")
    finally:
        conn.close()


if __name__ == '__main__':
    main()
