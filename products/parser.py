import requests
from bs4 import BeautifulSoup

URL = 'https://www.citilink.ru/catalog/noutbuki/'
HEADERS = {'user_agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.81 Safari/537.36 Edg/94.0.992.50',
            'accept': '*/*'}

def get_html(url, params=None):
    r = requests.get(url, headers=HEADERS, params=params)
    return r

def parse():
    html = get_html(URL)
    if html.status_code == 200:
        return get_content(html.text)
    
def get_content(html):
    soup = BeautifulSoup(html, 'html.parser')
    items = soup.findAll('div', class_='product_data__gtm-js')
    products = []
    category = soup.find('h1', class_='Subcategory__title').get_text(strip=True)
    base_category = soup.find('a', { 'class' : 'Breadcrumbs__link-default'}).find('span', recursive=False).get_text(strip=True)
    for item in items:
        products.append(
            {
                'title': item.find('a', class_='ProductCardHorizontal__title').get_text(strip=True),
                'price': item.find('span', class_='ProductCardHorizontal__price_current-price').get_text(strip=True),
                'image_url': item.find('img', class_='ProductCardHorizontal__image').get('src'),
                'category': category,
                'parent_category': base_category
            }
        )
    return products