import random
import re
import time
from functools import reduce

from lxml import etree, html
from lxml.etree import _ElementUnicodeResult
from neolib import REGEX, XPATH
from neolib.http.Page import Page

# Neopets base URL
BASE_URL = 'http://www.neopets.com'


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
    # Try it as a path name first
    query = ''
    try:
        query = reduce(dict.__getitem__, path.split('/'), XPATH)
    except:
        query = path

    # Test and return
    if type(subject) is Page:
        subject = subject.document

    result = subject.xpath(query)

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
    # Try it as a path name first
    query = ''
    try:
        query = reduce(dict.__getitem__, exp.split('/'), REGEX)
    except:
        query = exp

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
