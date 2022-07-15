import requests
import fake_useragent
from bs4 import BeautifulSoup

# выбираем категорию для запроса из cat_id
# Что парсим:
# name - Название на английском и русском(строка
# genres_list - Жанры(список)
# description - Описание(строка)
# image - Обложка тайтла(выгружается в папку)

user = fake_useragent.UserAgent().random

header = {
    'user-agent': user
}

url = 'https://shikimori.one/collections/5919-interaktiv-top-lyubimyh-anime-po-10-zhanram-chast-1'
response = requests.get(url, headers=header).text
text_response = BeautifulSoup(response, 'lxml')

cat_id = {
    'Комедия': '1',
    'Приключения': '2',
    'Фэнтези': '3',
    'Фантастика': '4',
    'Драма': '5',
    'Школа': '6',
    'Экшен': '7',
    'Повесдневность': '8',
    'Романтика': '9',
    'Детектив': '10',
}

block = text_response.find('div', attrs={'class': 'cc-collection-groups to-process', 'data-index': cat_id['Школа']})
block_divs = block.find_all('div', class_='cover linkeable anime-tooltip')
block_a = block.find_all('a', class_='cover anime-tooltip')

titles_urls = list()
for a in block_divs:
    titles_urls.append(a['data-href'])
for a in block_a:
    titles_urls.append(a['href'])

for href in titles_urls:
    title_response = requests.get(href, headers=header).text
    text_title_response = BeautifulSoup(title_response, 'lxml')
    date = text_title_response.find('span', attrs={'class': 'b-tooltipped dotted mobile unprocessed', 'data-direction': 'right'}).text
    name = text_title_response.find('h1').text
    title = name.split('/')[1].strip()
    genres = text_title_response.find_all('span', class_='genre-ru')
    genres_list = [x.text for x in genres]
    description = text_title_response.find('div', class_='b-text_with_paragraphs').text
    image = text_title_response.find('img', attrs={'alt': title}).get('src')
    image_bytes = requests.get(image, headers=header).content
    img_title = title.replace(':', '-')
    with open(f'images/{img_title}.jpg', 'wb') as img:
        img.write(image_bytes)
    print(name)
    if 'г' in date:
        print(date)
    print(genres_list)
    print(description)
    print('------------------------')

