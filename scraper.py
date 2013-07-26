# -*- coding: utf-8 -*-
from __future__ import division, absolute_import
from bs4 import BeautifulSoup

import grequests
import requests
from pprint import pprint

URL = 'http://www.newegg.com'
URL = 'http://www.newegg.com/Open-Box/Store?Type=OPENBOX'


class Product(object):

    def __init__(self, tag):
        self.tag = tag
        pass

    def get_desc(self):
        return self.tag.find('span', class_='itemDescription') \
            .text \
            .rsplit('Open Box: ', 1)[1]

    def __str__(self):
        return unicode(self).encode('utf-8')

    def __unicode__(self):
        return self.get_desc()


def get_products(URL):
    r = requests.get(URL).text
    soup = BeautifulSoup(r)
    return soup.select(".itemCell")


def get_product_categories(URL):
    r = requests.get(URL).text
    soup = BeautifulSoup(r)
    soup_list = soup.find("div", class_='blaNavigation') \
                    .find('dl', class_='categoryList') \
                    .find_all('dd')
    import re
    for c in soup_list:
        quantity = int(
            re.match(
                '\((\d+)\)',
                c.find('span', class_='grey')
                .get_text(strip=True)
            )
            .group(1)
        )

        yield {
            'text': next(c.a.stripped_strings),
            'href': c.a['href'],
            'quantity': quantity
        }


products = list()

for category in get_product_categories(URL):
    products.extend(
        [Product(product) for product in get_products(category['href'])]
    )

for product in products:
    try:
        pprint(str(product))
    except UnicodeEncodeError:
        import chardet
        pprint(chardet.detect(product))
