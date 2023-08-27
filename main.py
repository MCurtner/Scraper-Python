import requests
from bs4 import BeautifulSoup
from concurrent.futures import ThreadPoolExecutor

import database_manager


def get_all_product_categories():
    """
    Get all the product main category links
    :return: Array of urls
    """
    url = 'https://shop.iglobus.cz/cs/outlet'
    response = requests.get(url)
    html = response.text
    soup = BeautifulSoup(html, 'lxml')
    list_items = soup.find_all('div', class_='toggler-item__title-wrapper')

    list_set = []
    prepend_url = 'https://shop.iglobus.cz'
    for item in list_items:
        item_url = item.find('button').get('data-url')

        if item_url.count('/') == 2:
            list_set.append(prepend_url + item_url)

    return list_set


def get_total_pages(url):
    """
    Get the total number of pages for url processing.
    :param url: The url of the page which contains the pagination.
    :return: The total number of pages.
    """
    response = requests.get(url)
    html = response.text
    soup = BeautifulSoup(html, 'lxml')

    page_items = soup.find_all('li', class_='pagination__item-cz')
    last_page_item = page_items[len(page_items) - 1]
    page_url = last_page_item.find('a').get('href')

    # Return the substring of last page number
    return page_url[-2:-1]


def get_all_products(url):
    """
    Get all products and parse items.
    :param url: Url of the page.
    :return:
    """
    response = requests.get(url)
    html = response.text
    soup = BeautifulSoup(html, 'lxml')
    product_items = soup.find_all('product-item')

    prepend_url = 'https://shop.iglobus.cz'
    for product in product_items:
        image_link = product.find('a').get('href')
        product_name = product.find('div', class_='product-item__info').find('a').text.strip()
        sale_volume = product.find('div', class_='product-item__sale-volume').find('span').text.strip()
        money_price = product.find('span', class_='money-price').find('span').text.strip()

        """
        print(image_link)
        print(product_name)
        print(sale_volume)
        print(money_price)
        print('-----------')
        """

        product_name = product_name.replace("'", "")

        database_manager.insert_values(product_name, prepend_url + image_link, money_price, sale_volume)


def worker(url):
    """
    Worker for parallel execution.
    :param url: The URL of the webpage
    :return:
    """
    total_pages = int(get_total_pages(f'{url}?ipp=72&page=1#'))
    for page in range(1, total_pages):
        print(f'Page: {page} of {total_pages}------------------------------')
        get_all_products(f'{url}?ipp=72&page={x}#')


if __name__ == '__main__':
    print('starting...')

    # Create the DB.
    database_manager.create_database_table()

    # Store the number of threads to created based
    # on the number of categories.
    category_urls = get_all_product_categories()

    # Create a thread pool for execution.
    pool = ThreadPoolExecutor(len(category_urls))

    # Execute the worker via threads
    for x in range(len(category_urls)):
        pool.submit(worker, category_urls[x])
