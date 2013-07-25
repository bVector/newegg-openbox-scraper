from bs4 import BeautifulSoup

import grequests
import requests

URL = 'http://www.newegg.com'
URL = 'http://www.newegg.com/Open-Box/Store?Type=OPENBOX'



#products_soup = [BeautifulSoup(p) for p in products]
#print list(products_soup)[0]

#print products[0]
class Product(object):

    def __init__(self, URL):
        r = requests.get(URL).text
        soup = BeautifulSoup(r)
        self.products_soup = soup.select(".productCells .unit_gallery .wrap_inner")

    def get_desc(self, tags):
        for tag in tags:
            yield tag.find('div', class_='wrap_description') \
                .find('span', class_='descText') \
                .text \
                .rsplit('Open Box: ', 1)[1]

    def get_products(self):
        return self.get_desc(self.products_soup)

    def __str__(self):
        return '\n'.join(self.get_products())

    def __unicode__(self):
        return ''.join(self.get_products)

#descs = get_desc(products)
#print list(descs)

s = Product(URL)
#print list(s.get_products())
print s
#desc = descblock.find('span', class_='descText').text

#print soup.prettify()
