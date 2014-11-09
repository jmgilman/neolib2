import logging
import random
import re
import time
from functools import reduce

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

    def __init__(self, usr=None):
        """Initializes the base class by initializing the logger instance"""
        self._logger = logging.getLogger(self._log_name)
        self._usr = usr

    def _search(self, exp, subject, all=False):
        """Searches the given string using the given expression name

        Args:
            | **exp**: The name of the expression to use for querying as stored
            in _regex. Should be in the format of 'key1/key2/key3'.
            | **subject*: Instance of :class:`.Page`, :class:`HTMLElement`, or
                a string value to search
            | **all**: Whether to search with DOTALL

        Returns:
            A list of matches from the regular expression query
        """
        if type(subject) is Page:
            string = subject.content
        elif type(subject) is html.HtmlElement:
            string = self._to_html(subject)
        else:
            string = subject

        query = reduce(dict.__getitem__, exp.split('/'), self._regex)

        if all:
            return re.findall(query, string, re.DOTALL)
        else:
            return re.findall(query, string)

    def _xpath(self, path, subject):
        """Searches the given subject using the given xpath name

        Args:
            | **path**: The name of the expression to use for querying as stored
            in _paths. Should be in the format of 'key1/key2/key3'.
            | **subject*: Instance of :class:`.Page`, or :class:`HTMLElement`

        Returns:
            A list of matches from the xpath query
        """
        if type(subject) is Page:
            ele = subject.document
        else:
            ele = subject

        query = reduce(dict.__getitem__, path.split('/'), self._paths)

        return ele.xpath(query)

    def _to_element(self, string):
        """Converts a HTML string into a lxml element

        Args:
            **string**: The HTML string to convert
        """
        return html.document_fromstring(string)

    def _to_html(self, element):
        """Converts a html element to a string

        Args:
            **element**: The HTML element to conver to a HTML string
        """
        return etree.tostring(element).decode('utf-8')

    def _path_to_html(self, path, subject):
        """Converts an xpath query to HTML

        Note that this function will fail if the xpath query returns no
        results. Furthermore, if the query returns more than one result only
        the first result will be converted to HTML and returned.

        Args:
            **path**: The name of the expression to use for querying as stored
            in _paths. Should be in the format of 'key1/key2/key3'.
            **subject**: Instance of :class:`.Page`, or :class:`HTMLElement`
        """
        return self._to_html(self._xpath(path, subject)[0])

    def _wait_random(max):
        """Wait a random time up to the max seconds given

        Takes the max seconds given and divides it by two to obtain a minimum
        wait value. Picks a random number between the max and minimum value to
        wait.

        Args:
            **max**: The max number of seconds to wait
        """
        if max == 0:
            return

        min = max / 2
        delay = random.randint(min, max)

        time.sleep(delay)
