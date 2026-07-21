import requests
from bs4 import BeautifulSoup
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
import csv
import time

headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                      "AppleWebKit/537.36 (KHTML, like Gecko) "
                      "Chrome/120.0 Safari/537.36",
        "Accept-Language": "ru-RU,ru;q=0.9",
    }
start = time.perf_counter()
def make_session():
    session = requests.Session()
    session.headers.update(headers)

    retry = Retry(
        total=5,
        backoff_factor=1,  # 1s, 2s, 4s, 8s...
        status_forcelist=[429, 500, 502, 503, 504],
        allowed_methods=["GET"],
        respect_retry_after_header=True,
    )

    session.mount('https://', HTTPAdapter(max_retries=retry))
    session.mount('http://', HTTPAdapter(max_retries=retry))

    return session


def parsing():
    print('Start')
    session = make_session()
    books = []
    page = 1
    while True:
        response = session.get(f"https://books.toscrape.com/catalogue/page-{page}.html", timeout=(3, 6))

        if response.status_code == 404:
            break

        response.raise_for_status()

        soup = BeautifulSoup(response.text, 'lxml')

        blocks = soup.find_all('article', class_='product_pod')
        for block in blocks:
            book_link = block.find('h3').find('a')
            name = book_link.get('title')
            price = block.find('div', class_='product_price').find('p')
            rating = block.find('p').get('class')[1]
            link = 'https://books.toscrape.com/catalogue/' + book_link.get('href')

            books.append({
                'title': name if name else 'Not found',
                'price': price.get_text().replace('Â', '') if price else 'Not found',
                'rating': rating if rating else 'Not found',
                'link': link if link else 'Not found',
            })
        page += 1

    with open('stuff.csv', 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=['title', 'price', 'rating', 'link'], delimiter=";")
        writer.writeheader()
        writer.writerows(books)
    print('Finished!')
parsing()
end = time.perf_counter()
print(f'{end - start:.2f} seconds')