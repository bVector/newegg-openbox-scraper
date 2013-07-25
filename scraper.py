from bs4 import BeautifulSoup

import grequests
import requests

URL = 'http://www.newegg.com'
URL = 'http://www.newegg.com/Open-Box/Store?Type=OPENBOX'



#products_soup = [BeautifulSoup(p) for p in products]
#print list(products_soup)[0]

#print products[0]
def get_products(URL):
    r = requests.get(URL).text
    soup = BeautifulSoup(r)
    return soup.select(".productCells .unit_gallery .wrap_inner")


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


#descs = get_desc(products)
#print list(descs)

products = [Product(product) for product in get_products(URL)]
#s = Product(URL)
#print list(s.get_products())
from pprint import pprint
pprint(products)
#desc = descblock.find('span', class_='descText').text

#print soup.prettify()
