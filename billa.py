import requests
import json
from dataclasses import dataclass, asdict

import database_manager

prepend_url = 'https://shop.billa.cz'


def get_all_products(url):
    response = requests.get(url)
    json_object = json.loads(response.text)

    for item in json_object['results']:
        name = item['name']
        image_url = item['images'][0]

        price_object = item['price']
        price = price_object['regular']['value']
        volume_price = price_object['regular']['perStandardizedQuantity']
        money_price = price_object['basePriceFactor'] + price_object['baseUnitShort']

        """
        print('----------------')
        print(name)
        print(image_url)
        print(format_price(price))
        print('Kč')
        print(format_price(volume_price))
        print('Kč/' + money_price)
        print("Billa")
        """

        name = name.strip().replace("'", "")

        database_manager.insert_values(name, image_url, format_price(price), 'Kč', format_price(volume_price),
                                       'Kč/' + money_price, 'Billa')


def format_price(price):
    price = str(price)
    return price[:-2] + ',' + price[-2:]


def main():
    # Create the DB.
    database_manager.drop_table()
    database_manager.create_database_table()

    for page_number in range(0, 297):
        get_all_products(f'https://shop.billa.cz/api/products?page={page_number}&pageSize=30&sortBy=relevance')


if __name__ == '__main__':
    print('starting...')
    main()




