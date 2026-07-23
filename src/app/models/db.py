import os
import time

import pymysql


def get_conn(retries=5, delay=2):
    last_error = None
    for attempt in range(retries):
        try:
            return pymysql.connect(
                host=os.environ.get("DB_HOST", "mariadb"),
                port=int(os.environ.get("DB_PORT", "3306")),
                user=os.environ.get("DB_USER", "playgrounds"),
                password=os.environ.get("DB_PASSWORD", "playgrounds"),
                database=os.environ.get("DB_NAME", "playgrounds"),
                charset="utf8mb4",
                autocommit=True,
            )
        except pymysql.MySQLError as error:
            last_error = error
            if attempt < retries - 1:
                time.sleep(delay)
    raise last_error
