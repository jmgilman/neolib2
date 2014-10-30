import lxml.html
import requests

from neolib2.http.HTMLForm import HTMLForm

class Page:
    url = ""

    request = None
    response = None

    headers = None
    content = ""

    post_data = {}
    header_values = {}

    usr = None

    document = None
    forms = []

    def __init__(self, url, usr=None, session=None, post_data=None, header_values=None, proxy=None):
        # Set class attributes
        self.url, self.post_data, self.header_values = url, post_data, header_values

        # Determine if this request is using an existing user or session and act accordingly
        if usr:
            if post_data:
                r = usr.session.post(url, data=post_data, headers=header_values, proxies=proxy)
            else:
                r = usr.session.get(url, headers=header_values, proxies=proxy)
        elif session:
            if post_data:
                r = session.post(url, data=post_data, headers=header_values, proxies=proxy)
            else:
                r = session.get(url, headers=header_values, proxies=proxy)
        else:
            # Was there post data attached to this request
            if post_data:
                r = requests.post(url, data=post_data, headers=header_values, proxies=proxy)
            else:
                r = requests.get(url, headers=header_values, proxies=proxy)

        # Setup attributes based on response
        self.request = r.request
        self.response = r
        self.headers = r.headers
        self.content = r.text

        # Prep the html parser
        self.document = lxml.html.document_fromstring(self.content)

        # Process forms
        for form in self.xpath("//form"):
            self.forms.append(HTMLForm(url, form))

    def form(self, **kwargs):
        matches = []
        # Loop through all forms and associated attributes looking for
        # supplied keyword arguments
        for form in self.forms:
            for key in kwargs.keys():
                try:
                    value = getattr(form, key)
                    if kwargs[key] == value: matches.append(form)
                except Exception:
                    continue
        return matches

    def xpath(self, query):
        return self.document.xpath(query)
