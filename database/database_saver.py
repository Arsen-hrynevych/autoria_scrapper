import subprocess
from datetime import date
from os import makedirs, path, getcwd

from app.models import Car
from database.session import Session
from env_utils import DATABASE_URL


def save_to_database(data):
    session = Session()
    for item in data:
        car = Car(**item)
        session.add(car)
    session.commit()
    session.close()


def dump_database():
    current_datetime = date.today().strftime("%d_%m_%Y")
    dump_dir = path.join(getcwd(), 'database', 'dumps')
    dump_file_path = path.join(dump_dir, f'data_dump_{current_datetime}.sql')

    makedirs(dump_dir, exist_ok=True)

    command = f'pg_dump {DATABASE_URL} > {dump_file_path}'

    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(f'Result: {result.stdout}')

        print(f'Database dump created: {dump_file_path}')
    except subprocess.CalledProcessError as e:
        print(f'Error creating database dump: {e}')



