from urllib.parse import urlparse


class HTMLForm:
    html = None
    action = ''
    method = ''
    url = ''
    fields = {}

    def __init__(self, base_url, form_element):
        # Form setup
        self.url = base_url

        if len(form_element.xpath('./@action')) > 0:
            self.action = form_element.xpath('./@action')[0]
        if len(form_element.xpath('./@method')) > 0:
            self.method = form_element.xpath('./@method')[0]

        # Grab all the inputs
        self.fields = {}
        for einp in form_element.xpath('.//input'):
            # Search for any attributes and assign them as necessary
            inp = HTMLFormInput()
            for attribute in dir(inp):
                if len(einp.xpath('./@' + attribute)) > 0:
                    setattr(inp, attribute, einp.xpath('./@' + attribute)[0])
            if inp.name:
                self.fields[inp.name] = inp

    def update(self, fields):
        for key in fields.keys():
            self.fields[key].value = fields[key]

    def submit(self, usr):
        # Assemble the post data
        post_data = {}
        for key in self.fields.keys():
            post_data[key] = self.fields[key].value

        # Assemble the address to post to
        u = urlparse(self.url)
        if not self.action:
            self.action = self.url
        elif self.action == u.path:
            self.action = self.url
        else:
            if u.netloc not in self.action:
                path = '/'.join(u.path.split('/')[1:-1])
                if self.action.startswith('/'):
                    path = path + self.action
                else:
                    path = path + '/' + self.action
                self.action = 'http://' + u.netloc + '/' + path

        # Return a new page with the result of the form submission
        return usr.get_page(self.action, post_data)

    def __get__(self, key):
        return self.fields[key].value

    def __set__(self, key, value):
        self.fiedlds[key].value = value

    def __iter__(self):
        for field in self.fields:
            yield field

    def __len__(self):
        return len(self.fields)


class HTMLFormInput:
    type = ''
    name = ''
    value = ''

    x = 0
    y = 0
