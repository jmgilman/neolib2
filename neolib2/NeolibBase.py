import logging
import re

from lxml import etree


class NeolibBase:
    log_name = 'neolib'
    logger = None

    urls = {}
    paths = {}
    regex = {}

    base_url = 'http://www.neopets.com'

    def __init__(self):
        self.logger = logging.getLogger(self.log_name)

    def _search(self, query, string, all=False):
        if all:
            return re.findall(query, string, re.DOTALL)
        else:
            return re.findall(query, string)

    def _to_html(self, element):
        return etree.tostring(element).decode('utf-8')
