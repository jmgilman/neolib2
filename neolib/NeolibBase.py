import logging
import re
import time
import random

from lxml import etree, html
from neolib.http.Page import Page


class NeolibBase:
    """The base class for most other classes in the Neolib library

    This class should be inherited by any class that is doing work on a
    :class:`User` object in the library. It provides the established template
    for doing such work and the original template should be followed as closely
    as possible to maintain uniformity throughout the library.

    Attributes:
        | **_log_name**: The name of the log being used by the child class
        | **_logger**: A logger instance used to write to the error log

        | **_usr**: A :class:`.User` instance being used by the child class for work

        | **_urls**: A dictionary of URLs that will be used for doing work
        | **_paths**: A dictionary of XPath queries that will be used for doing
            work. This dictionary should either be in {key: expression} format
            or {key {key: expression}} format
        | **_regex**: A dictionary for regular expressions that will be used for
            doing work. This dictionary should either be in {key: expression}
            format or {key: {key: expression}} format

        | **_base_url**: The base Neopets URL
    """

    _log_name = 'neolib'
    _logger = None

    _usr = None

    _urls = {}
    _paths = {}
    _regex = {}

    _base_url = 'http://www.neopets.com'

    def __init__(self):
        """Initializes the base class by initializing the logger instance"""
        self._logger = logging.getLogger(self._log_name)

    def _search(self, query, subject, all=False):
        """Searches the given string using the given Regex query

        Args:
            | **query**: The regular expression query
            | **subject*: Instance of :class:`.Page`, :class:`HTMLElement`, or
                a string value to search
            | **all**: Whether to search with DOTALL

        Returns:
            A list of matches from the query
        """
        if type(subject) is Page:
            string = subject.content
        elif type(subject) is html.HtmlElement:
            string = self._to_html(subject)
        else:
            string = subject

        if all:
            return re.findall(query, string, re.DOTALL)
        else:
            return re.findall(query, string)

    """Converts a HTML string into a lxml element

    Args:
        **string**: The HTML string to convert
    """
    def _to_element(self, string):
        return html.document_fromstring(string)

    def _to_html(self, element):
        """Converts a html element to a string

        Args:
            **element**: The HTML element to conver to a HTML string
        """
        return etree.tostring(element).decode('utf-8')

    def _wait_random(max):
        if max == 0:
            return

        min = max / 2
        delay = random.randint(min, max)

        time.sleep(delay)
