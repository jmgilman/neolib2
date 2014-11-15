import json

import lxml.html
import requests

from neolib.http.HTMLForm import HTMLForm


class Page:
    """Represents a HTML web page

    This class is used to encapsulate a HTML web page into a Python object. Not
    all of the attributes a HTML web page can have are present in this class.
    The primary purpose of this class is for creating an encapsulation that
    can be passed around the library for uniformity. The secondary purpose is
    to tie in the requests and lxml libraries into one easy-to-use object.

    Attributes:
        | **url**: The originating URL for this web page

        | **request**: A :class:`Request` object representing the HTTP request
        | **response**: A :class:`Response` object representing the HTTP response

        | **headers**: A dictionary containing the response headers
        | **content**: The HTML content of the web page
        | **json**: If the returned content is JSON this will be loaded

        | **post_data**: Optional dictionary containing any POST data sent
        | **header_values**: Optional dictionary with any header values overriden

        | **usr**: Optional :class:`.User` object used to request this page

        | **document**: An instance of the root element of this HTML page
        | **forms**: A list of :class:`.HTMLForm` objects for forms on this page
    """

    url = ''

    request = None
    response = None

    headers = None
    content = ''
    json = {}

    post_data = {}
    header_values = {}

    usr = None

    document = None
    forms = []

    def __init__(self, url, usr=None, post_data=None,
                 header_values=None, proxy=None):
        """Initializes the page with the given request details

        Args:
            | **url**: The URL of the page to request
            | **usr**: Optional :class:`.User` object to make the request with
            | **post_data**: Optional dictionary of data to POST with (name -> value)
            | **header_values**: Optional dictionary of header values to override the
                request headers with.
            | **proxy**: Optional proxy to use with the request
        """
        # Set class attributes
        self.url = url
        self.post_data = post_data
        self.header_values = header_values

        # Determine if this request is using an existing user
        if usr:
            if post_data:
                r = usr.session.post(url, data=post_data,
                                     headers=header_values, proxies=proxy)
            else:
                r = usr.session.get(url, headers=header_values, proxies=proxy)
        else:
            if post_data:
                r = requests.post(url, data=post_data, headers=header_values,
                                  proxies=proxy)
            else:
                r = requests.get(url, headers=header_values, proxies=proxy)

        # Setup attributes based on response
        self.request = r.request
        self.response = r
        self.headers = r.headers

        # Check what this is
        if r.headers['Content-Type'] == 'application/ajax':
            self.content = r.text
            self.json = json.loads(r.text)
        elif 'text/html' in r.headers['Content-Type']:
            # Prep the html parser
            self.content = r.text
            self.document = lxml.html.document_fromstring(self.content)

            # Process forms
            self.forms = []
            for form in self.xpath('//form'):
                self.forms.append(HTMLForm(url, form))
        else:
            self.content = r.content

    def form(self, **kwargs):
        """Searches for forms this page holds using the given keyword args

        Args:
            **kwargs: The keyword arguments to search for

        Returns:
            A list of :class:`.HTMLForm` instances that match the original query

        Example:
            `form = pg.form(action='/login.phtml')`
        """
        matches = []
        # Loop through all forms and associated attributes looking for
        # supplied keyword arguments
        for form in self.forms:
            for key in kwargs.keys():
                try:
                    value = getattr(form, key)
                    if kwargs[key] == value:
                        matches.append(form)
                except Exception:
                    continue
        return matches

    def xpath(self, query):
        """Queries the current page using the given XPath query

        Args:
            **query**: The XPath query to use

        Returns:
            A list of elements resulting from the XPath query
        """
        return self.document.xpath(query)

    def __repr__(self):
        return "Page <" + self.url + ">"
