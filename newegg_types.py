# -*- coding: utf-8 -*-


class Category(object):
    """NewEgg store category."""

    def __init__(self, **kwargs):
        """A new Category can accept arguments as attributes."""
        self.products = None
        for k, v in kwargs.items():
            setattr(self, k, v)

    def parent(self):
        """Return the parent Category object, if exists."""
        pass

    def siblings(self):
        """Return list of sibling Category"""
        pass

    def __str__(self):
        return unicode(self).encode('utf-8')

    def __unicode__(self):
        return self.text
