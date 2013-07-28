# -*- coding: utf-8 -*-
from __future__ import division, absolute_import
from bs4 import BeautifulSoup

import grequests
import requests
import tornado.httpclient
import tornado.ioloop
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




import gevent
from tornado import gen
def fetch_page(URL):
    http = tornado.httpclient.AsyncHTTPClient()
    fetch = http.fetch(URL, get_product_categories)
    return gen.Task(fetch)

#souped = (grequests.get(c['href']) for c in get_product_categories(URL))
class Category(object):

    def __init__(self, **kwargs):
        self.products = None
        for k, v in kwargs.items():
            setattr(self, k, v)

    def __str__(self):
        return unicode(self).encode('utf-8')

    def __unicode__(self):
        return self.text


class Categories(object):
    def __init__(self, URL):
        self.URL = URL

    def fetch(self):
        import requests
        r = requests.get(self.URL)
        return r.text

    def __iter__(self):
        return iter(self.parse())

    def parse(self):
        #r = requests.get(URL).text
        self.categories = list()
        soup = BeautifulSoup(self.fetch())
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

            self.categories.append(Category(**{
                'text': next(c.a.stripped_strings),
                'href': c.a['href'],
                'quantity': quantity
            }))

        return self.categories




products = list()
cats = Categories(URL)

def add_products_to_categories(categories):
    for c in categories:
        items = [Product(product) for product in get_products(c.href)]
        c.products = items
        yield c

cats = add_products_to_categories(cats)

for c in cats:
    print("'%s' has products attribute, type %s, with %s items" %\
            (c.text, type(c.products),\
            len(c.products)))
    try:
        print(c.text)
        for product in c.products:
            try:
                pprint(str(product))
                pass
            except UnicodeEncodeError:
                import chardet
                pprint(chardet.detect(product))
    except TypeError:
        print "no items for %s" % c.text
