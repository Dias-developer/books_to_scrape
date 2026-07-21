import requests
from bs4 import BeautifulSoup
import csv

def parsing():
    print('Start')
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                      "AppleWebKit/537.36 (KHTML, like Gecko) "
                      "Chrome/120.0 Safari/537.36",
        "Accept-Language": "ru-RU,ru;q=0.9",
    }
    books = []
    page = 1
    while True:
        response = requests.get(f"https://books.toscrape.com/catalogue/page-{page}.html", headers=headers, timeout=(3, 6))

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