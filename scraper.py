from bs4 import BeautifulSoup

import grequests
import requests

URL = 'http://www.newegg.com'
URL = 'http://www.newegg.com/Open-Box/Store?Type=OPENBOX'

r = requests.get(URL).text
soup = BeautifulSoup(r)

products = soup.select(".productCells .unit_gallery .wrap_inner")
#products_soup = [BeautifulSoup(p) for p in products]
#print list(products_soup)[0]

#print products[0]


def get_desc(tags):
    for tag in tags:
        yield tag.find('div', class_='wrap_description') \
            .find('span', class_='descText') \
            .text \
            .rsplit('Open Box: ', 1)[1]

descs = get_desc(products)
print list(descs)
#desc = descblock.find('span', class_='descText').text

#print soup.prettify()
