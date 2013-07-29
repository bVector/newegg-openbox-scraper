# -*- coding: utf-8 -*-
from __future__ import division, absolute_import
from pprint import pprint

"""
    soup/
        ProductList.py selectors for ProductList.aspx pages
        Store.py selectors for Open-Box/Store pages
"""


from soup.ProductList import product_tags, price_now, price_before, description
from soup.ProductList import categories

URL = 'http://www.newegg.com/Product/ProductList.aspx?Submit=ENE' \
      '&N=100017680%204809&IsNodeId=1&SpeTabStoreType=99'

products = product_tags(URL)
for p in products:
    pprint("%s %s %s" % (price_now(p), price_before(p), description(p)))


categories = categories(URL)
for c in categories:
    pprint("%s %s %s" % (c.text, c.href, c.quantity))
