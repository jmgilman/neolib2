import random
import re
import time
from functools import reduce

from lxml import etree, html
from lxml.etree import _ElementUnicodeResult
from neolib import log, REGEX, URLS, XPATH
from neolib.http.Page import Page

# Neopets base URL
BASE_URL = 'http://www.neopets.com'

# Standard indicator for Neopets error pages
ERROR_TEXT = 'red_oops.gif'


def xpath(path, subject, as_html=False):
    """ Applies an xpath query to the given subject

    Args:
        | **path**: Can either be a valid xpath query or the path name to an
            existing xpath query as stored in xpath.json
        | **object**: Can be an lxml HTML element or a Page
        | **as_html**: Optional value to determine if any resulting HTML
            elements should be returned as strings instead

    Returns:
        A list of results from querying the object with the xpath query
    """
    # Find the query
    query = get_query(path, XPATH)

    # Test and return
    if type(subject) is Page:
        subject = subject.document

    result = subject.xpath(query)

    # Provide a friendly warning if nothing was returned
    if len(result) < 1:
        log.warning('Query `' + path + '` failed to find anything!')

    # Convert unicode results to strings
    for r in result:
        if type(r) is _ElementUnicodeResult:
            result[result.index(r)] = str(r)

    if as_html:
        return to_html(result[0])
    else:
        return result


def match(exp, subject, all=False):
    """ Matches a regular expression to the given subject

    Args:
        | **exp**: Can either be a valid regular exp or the path name to an
            existing regular exp as stored in regex.json
        | **subject**: Can be a Page, lxml HTML element, or string

    Returns:
        A list of results from the match
    """
    # Find the query
    query = get_query(exp, REGEX)

    # Test and return
    if type(subject) is Page:
        subject = subject.content
    elif type(subject) is html.HtmlElement:
        subject = to_html(subject)

    if all:
        return re.findall(query, subject, re.DOTALL)
    else:
        return re.findall(query, subject)


def to_html(element):
    """ Converts an lxml HTML element into a string """
    return etree.tostring(element).decode('utf-8')


def from_html(html):
    """ Converts an html string into an lxml HTML element """
    return html.document_fromstring(html)


def check_error(pg):
    """ Checks if the current page contains the standard Neopet's error message

    Args:
        | **pg**:

    Returns:
        Boolean value indicating if there was an error
    """
    if ERROR_TEXT in pg.content:
        return True
    else:
        return False


def get_query(name, queries):
    """ Fetches a query using the given name and dictionary of queries

    Args:
        | **name**: The string name of the query to reduce to

    Returns:
        The associated query
    """
    query = ''
    try:
        query = reduce(dict.__getitem__, name.split('/'), queries)
    except:
        log.warning('Using undocumented query: ' + query)
        query = name

    return query


def get_url(name):
    """ Returns the url using the given name

    Args:
        | **name**: The name of the url to return

    Returns:
        The url associated with the given name
    """
    return get_query(name, URLS)


def is_init(val):
    """ Tests if the given value can be safely casted to an integer

    Returns:
        Boolean value indicating if it can be safely casted
    """
    try:
        int(val)
        return True
    except Exception:
        return False


def remove_strs(subject, strings):
    """ Removes the given strings from the given subject

    Args:
        | **subject**: The subject to remove in
        | **strings**:  The strings to remove

    Returns:
        Modified subject with strings removed
    """
    for string in strings:
        subject = subject.replace(string, '')

    return subject


def format_nps(nps):
    """ Formats common neopoint strings into an integer value

    Args:
        | **nps**: The neopoints string to format

    Returns:
        Integer representing the neopoint string
    """
    return int(remove_strs(nps, [',', 'NP', ' ', 'np']))


def wait_random(max=10):
    """ Waits a random number of seconds up to the max number of seconds given

    Args:
        | **max**: The maximum number of seconds to wait
    """
    if max == 0:
        return

    min = max / 2
    delay = round(random.uniform(min, max), 2)

    time.sleep(delay)
