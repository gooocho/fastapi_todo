import os
import time

import psycopg2


def get_url():
    user = os.getenv("POSTGRES_USER", "postgres")
    password = os.getenv("POSTGRES_PASSWORD", "")
    server = os.getenv("POSTGRES_SERVER", "db")
    port = os.getenv("POSTGRES_PORT", "db")
    db = os.getenv("POSTGRES_DB", "app")
    return f"postgresql://{user}:{password}@{server}:{port}/{db}"


def main():
    count = 0
    cursor = None
    while count < 10:
        try:
            print(f"try {count}")
            cursor = psycopg2.connect(get_url())
            print(cursor)
            break
        except psycopg2.OperationalError:
            count += 1
            time.sleep(5)


if __name__ == "__main__":
    main()
