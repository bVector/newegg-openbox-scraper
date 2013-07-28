# -*- coding: utf-8 -*-
from __future__ import division, absolute_import
from bs4 import BeautifulSoup
from pprint import pprint
import requests

#URL = 'http://www.newegg.com'
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


class Category(object):

    def __init__(self, **kwargs):
        self.products = None
        for k, v in kwargs.items():
            setattr(self, k, v)

    def __str__(self):
        return unicode(self).encode('utf-8')

    def __unicode__(self):
        return self.text


def grab_categories(URL):
    r = requests.get(URL)

    soup = BeautifulSoup(r.text)
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

        yield Category(**{
            'text': next(c.a.stripped_strings),
            'href': c.a['href'],
            'quantity': quantity
        })


def add_products_to_categories(categories):
    for c in categories:
        c.products = [Product(product) for product in get_products(c.href)]
        yield c


products = list()
cats = grab_categories(URL)
cats = list(add_products_to_categories(cats))
total_products = sum(len(c.products) for c in cats)

for c in cats:
    print("\n'%s' has %s of %s products available for discount at %s\n" %
          (c.text, len(c.products), total_products, c.href))

    try:
        for product in c.products:
            try:
                pprint(str(product))
                pass
            except UnicodeEncodeError:
                import chardet
                pprint(chardet.detect(product))
    except TypeError:
        print "no items for %s" % c.text

print("There were %s items available on newegg for openbox items." %
      total_products)
