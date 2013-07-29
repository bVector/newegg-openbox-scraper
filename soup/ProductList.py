# -*- coding: utf-8 -*-
from __future__ import division, absolute_import
from decimal import Decimal
from bs4 import BeautifulSoup
import requests
import re
from newegg_types import Category


def categories(URL):
    """
        Return a list of Category' by downloading and parsing with bs4.

        Example URL is Product/ProductList.aspx page:
          http://www.newegg.com/Product/ProductList.aspx...
    """
    r = requests.get(URL)

    soup = BeautifulSoup(r.text)
    soup_list = soup.find("div", id='blaNavigation') \
                    .find('dl', class_='main') \
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


def description(tag):
    """Return the item name (description)"""
    return tag.find('span', class_='itemDescription') \
        .text \
        .rsplit('Open Box: ', 1)[1]


def price_before(tag):
    """Return the 'before price'"""
    try:
        return tag.find('li', class_='price-was') \
            .get_text(strip=True) \
            .rsplit('$', 1)[1] \
            .replace(",", "")  # remove commas
    except IndexError:
        return None


def price_now(tag):
    """Return a decimal of the current price"""
    tag = tag.find('li', class_='price-current')
    currency = tag.find('span', class_='price-current-label') \
        .get_text(strip=True)
    dollars = tag.find('strong').get_text(strip=True)
    cents = tag.find('sup').get_text(strip=True)

    price = ''.join([currency, dollars, cents])
    price = price.replace(",", "")  # remove commas

    return Decimal(price)


def product_tags(URL):
    """
        Return a list of bs4 tags by downloading the page and parsing
    """
    r = requests.get(URL).text
    soup = BeautifulSoup(r)
    return soup.select(".itemCell")
