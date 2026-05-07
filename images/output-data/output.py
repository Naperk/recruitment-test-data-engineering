#!/usr/bin/env python3

import json
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


def main():
    conn = connect()
    try:
        with conn.cursor() as cur:
            cur.execute("""
                SELECT pl.country, COUNT(p.id) AS total
                FROM people p
                JOIN places pl ON p.place_of_birth = pl.id
                GROUP BY pl.country
                ORDER BY total DESC
            """)
            result = {row[0]: row[1] for row in cur.fetchall()}
    finally:
        conn.close()

    with open('/data/summary_output.json', 'w', encoding='utf-8') as f:
        json.dump(result, f, separators=(',', ':'), ensure_ascii=False)

    print("Output written to /data/summary_output.json")


if __name__ == '__main__':
    main()
