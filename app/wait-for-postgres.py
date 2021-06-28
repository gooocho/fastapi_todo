import psycopg2
import time

DATABASE_URL = "postgresql://postgres:postgres@fastapi_todo_db:5432/fastapi_todo"


def main():
    count = 0
    cursor = None
    while count < 10:
        try:
            print(f"try {count}")
            cursor = psycopg2.connect(DATABASE_URL)
            print(cursor)
            break
        except psycopg2.OperationalError:
            count += 1
            time.sleep(5)


if __name__ == "__main__":
    main()
