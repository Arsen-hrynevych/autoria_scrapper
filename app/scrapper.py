from bs4 import BeautifulSoup
import requests
from re import compile, search

from env_utils import MAX_PAGES


def get_soup(url):
    """Gets the HTML code of a page from a URL."""
    response = requests.get(url)
    if response.status_code == 200:
        return BeautifulSoup(response.text, 'html.parser')
    print(f'Error when receiving a page {url}')
    return None


def get_phone_number(advertisement_id, data_hash, data_expires):
    """Gets the phone number of the advert."""
    phone_link = f'https://auto.ria.com/users/phones/{advertisement_id}?hash={data_hash}&expires={data_expires}'
    phone_response = requests.get(phone_link)
    if phone_response.status_code == 200:
        json_data = phone_response.json()
        formatted_phone_number = json_data.get('formattedPhoneNumber')
        digits = ''.join(filter(str.isdigit, formatted_phone_number))
        return int(digits)
    return None


def get_ad_data(ad_link):
    """Gets the data of the advert."""
    ad_soup = get_soup(ad_link)
    if ad_soup is None:
        return None

    title = ad_soup.find(class_='head').text.strip()
    script_tag = ad_soup.find('script', class_=compile(r'js-user-secure-\d+'))
    data_hash = script_tag['data-hash']
    data_expires = script_tag['data-expires']
    advertisement_id = search(r'(\d+)\.html$', ad_link).group(1)
    phone_number = get_phone_number(advertisement_id, data_hash, data_expires)
    price_usd = int(
        search(r'\d+', ad_soup.find(class_='price_value').text.replace('$', '').replace(' ', '')).group())
    odometer = int(ad_soup.find(class_='base-information').text.split()[0]) * 1000
    username = ad_soup.find(class_='seller_info_name').text.strip()
    image_url = ad_soup.find('img', class_='outline m-auto')['src']
    image_count = int(search(r'\d+', ad_soup.find('a', class_='show-all link-dotted').text).group())
    car_number_tag = ad_soup.find(class_='state-num')
    car_number = search(r'[A-Z]{2} \d{4} [A-Z]{2}',
                        car_number_tag.text.strip()).group() if car_number_tag else "Номер машини не вказано"
    car_vin_tags = ad_soup.find_all(class_=['label-vin', 'vin-code'])
    car_vin = next((tag.text.strip() for tag in car_vin_tags if tag), None)

    return {
        'url': ad_link,
        'title': title,
        'phone_number': phone_number,
        'price_usd': price_usd,
        'odometer': odometer,
        'username': username,
        'image_url': image_url,
        'images_count': image_count,
        'car_number': car_number,
        'car_vin': car_vin,
    }


def scrape_site(start_url):
    """Goes through all pages of the site, extracts information about the advert."""
    page_number = 1
    data = []
    while page_number <= MAX_PAGES:
        url = start_url if page_number == 1 else f'{start_url}?page={page_number}'
        soup = get_soup(url)
        if soup is None:
            return

        ad_titles = soup.select('.ticket-title')
        if not ad_titles:  # if there are no ads, it means that we have reached the last page
            break

        for ad_title in ad_titles:
            ad_link = ad_title.find('a')['href']
            ad_data = get_ad_data(ad_link)
            if ad_data is not None:
                data.append(ad_data)

        page_number += 1  # move to the next page
    return data
