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
    import re
    for c in soup_list:
        quantity = [int(re.match('\((\d+)\)', text).group(1)) for text in \
                [tag.get_text(strip=True) for tag in c.find_all('span', class_='grey')]][0]
        yield {
            'text': next(c.a.stripped_strings),
            'href': c.a['href'],
            'quantity': quantity
            #'quantity': [sibling for sibling in c.a.next_siblings if sibling][1]
            #'quantity': [sibling for sibling in c.a.span if sibling]
        }
        #yield c.a.get_text(strip=True)


from pprint import pprint
#products = [Product(product) for product in get_products(URL)]
tree = get_product_tree(URL)
#pprint(products)
pprint(list(tree))
