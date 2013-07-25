from bs4 import BeautifulSoup

import grequests
import requests

URL = 'http://www.newegg.com'
URL = 'http://www.newegg.com/Open-Box/Store?Type=OPENBOX'


class Product(object):

    def __init__(self, tag):
        self.tag = tag
        pass

    def get_desc(self):
        return self.tag.find('div', class_='wrap_description') \
            .find('span', class_='descText') \
            .text \
            .rsplit('Open Box: ', 1)[1]

    def __str__(self):
        return self.get_desc()

    def __repr__(self):
        return self.get_desc()


def get_products(URL):
    r = requests.get(URL).text
    soup = BeautifulSoup(r)
    return soup.select(".productCells .unit_gallery .wrap_inner")


def get_product_tree(URL):
    r = requests.get(URL).text
    soup = BeautifulSoup(r)
    soup_list = soup.find("div", class_='blaNavigation') \
                    .find('dl', class_='categoryList') \
                    .find_all('dd')

    for c in soup_list:
        yield next(c.a.stripped_strings)
        #yield c.a.get_text(strip=True)


from pprint import pprint
#products = [Product(product) for product in get_products(URL)]
tree = get_product_tree(URL)
#pprint(products)
pprint(list(tree))
