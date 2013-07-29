# -*- coding: utf-8 -*-
from __future__ import division, absolute_import
from bs4 import BeautifulSoup
import requests
import re
from newegg_types import Category


"""
    Soup selectors and extraction for
    http://www.newegg.com/Open-Box/Store?Type=OPENBOX
"""


def get_categories(URL):
    r = requests.get(URL)

    soup = BeautifulSoup(r.text)
    soup_list = soup.find("div", class_='blaNavigation') \
                    .find('dl', class_='categoryList') \
                    .find_all('dd')

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
