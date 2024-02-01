from app.scrapper import scrape_site
from database.database_saver import save_to_database, dump_database


def job():
    start_url = 'https://auto.ria.com/car/used/'
    data = scrape_site(start_url)
    save_to_database(data)
    dump_database()

