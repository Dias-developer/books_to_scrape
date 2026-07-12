import requests
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
import csv


headers = {
    'User-Agent': UserAgent().random,
}
url = 'https://books.toscrape.com/'
books = []
while True:
    response = requests.get(url, headers=headers, timeout=(3, 6))
    if response.status_code != 200:
        break

    soup = BeautifulSoup(response.text, 'lxml')

    blocks = soup.find_all('article', class_='product_pod')
    for block in blocks:
        name = block.find('h3').find('a').get('title')
        price = block.find('div', class_='product_price').find('p').text
        rating = block.find('p').get('class')[1]
        link = 'https://books.toscrape.com/catalogue/' + block.find('h3').find('a').get('href')

        if name and price and rating and link:
            books.append({'title': name,
                          'price': price.replace('Â', ''),
                          'rating': rating,
                          'link': link})
    next_btn = soup.find('li', class_='next').find('a').get('href')
    if next_btn:
        url = 'https://books.toscrape.com/' + next_btn
    else:
        break

with open('stuff.csv', 'w', newline='', encoding='utf-8') as csvfile:
    writer = csv.DictWriter(csvfile, fieldnames=['title', 'price', 'rating', 'link'], delimiter=";")
    writer.writeheader()
    writer.writerows(books)