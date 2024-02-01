# autoria_scrapper

## Setup Steps

1. Create a `.env` file in the project's root directory.

2. Fill in the fields in the `.env` file using the example from `.env.sample`.

3. Run the application using Docker Compose:

   ```bash
   docker-compose up -d
   ```

4. Wait until the task is executed.

## Additional information

The `MAX_PAGES` environment variable is used to specify how many pages you want to be parsed.

If you don't want to wait until the next day, insert this code into `main.py`:

```
import schedule
import time
from datetime import datetime, timedelta

from app.models import Base
from app.scheduler import job
from database.session import engine
from database.database_saver import dump_database

if __name__ == "__main__":
    Base.metadata.create_all(engine)

    run_time = (datetime.now() + timedelta(minutes=5)).strftime("%H:%M")

    print(f'Scheduled tasks at: {run_time}')
    
    schedule.every().day.at(run_time).do(job)
    schedule.every().day.at(run_time).do(dump_database)

    while True:
        now = time.localtime()
        next_run = schedule.next_run()
        next_run_timetuple = next_run.timetuple() if next_run else now
        sleep_duration = time.mktime(next_run_timetuple) - time.mktime(now)

        if sleep_duration > 0:
            time.sleep(sleep_duration)
        else:
            schedule.run_pending()
```