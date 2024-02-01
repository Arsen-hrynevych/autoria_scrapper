import schedule
import time

from app.models import Base
from app.scheduler import job
from database.session import engine
from database.database_saver import dump_database

if __name__ == "__main__":
    Base.metadata.create_all(engine)

    schedule.every().day.at("12:00").do(job)
    schedule.every().day.at("00:00").do(dump_database)

    while True:
        now = time.localtime()
        next_run = schedule.next_run()
        next_run_timetuple = next_run.timetuple() if next_run else now
        sleep_duration = time.mktime(next_run_timetuple) - time.mktime(now)

        if sleep_duration > 0:
            print(f'Next run scheduled at: {next_run.strftime("%Y-%m-%d %H:%M:%S")}')
            time.sleep(sleep_duration)
        else:
            print('Running scheduled tasks...')
            schedule.run_pending()
