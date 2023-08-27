import requests
import json

prepend_url = 'https://shop.billa.cz'


def get_all_products(url):
    response = requests.get(url)
    json_object = json.loads(response.text)

    for item in json_object['results']:
        name = item['name']
        price = item['price']['regular']['value']
        amount = item['amount'] + ' ' + item['volumeLabelLong']

        print('----------------')
        print(name)
        print(price)
        print(amount)


if __name__ == '__main__':
    print('starting...')

    for page_number in range(0, 297):
        get_all_products(f'https://shop.billa.cz/api/products?page={page_number}&pageSize=30&sortBy=relevance')


