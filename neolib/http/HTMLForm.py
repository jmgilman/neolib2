from urllib.parse import urlparse


class HTMLForm:
    """Represents a HTML form on a web page

    This class is used to encapsulate an HTML form into a Python object. It
    does so by extracting the important form attributes (action, method) as
    well as any form inputs that actually get sent back to the web server. The
    form inputs can be accessed directly by name as an attribute of this
    object (I.E form.input_name)

    Attributes
       action: The destination of the form
       method: The method in which the form is submitted
       url: The base URL this form came from
       fields: A dictionary containing all of the inputs of the field. The
           dictionary uses the input name as the key and an instance of
           :class:`HTMLFormInput` as the value.
    """

    action = ''
    method = ''
    url = ''
    fields = {}

    def __init__(self, base_url, form_element):
        """Initializes the form with the given base URL and form element

        Args:
            base_url: The base URL this form originated from
            form_element: An instance of a form element
        """
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
        """Updates the stored fields with the given fields

        Args:
            fields: A dictionary to update the currently stored fields with
        """
        for key in fields.keys():
            self.fields[key].value = fields[key]

    def submit(self, usr):
        """Submits the current form as if the user had pressed the submit button

        This method will utilize the provided :class:`User` instance to POST
        the gathered form data to the appropriate URL as determined by the base
        URL provided and the action of the form itself. It returns the result
        of the POST action.

        Args:
            usr: An instance of :class:`User` to use for submitting the form

        Returns:
            A instance of class:`Page` representing the result
        """
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
    """Represents an input element of an HTML form

    Attributes
       type: The input type
       name: The input name
       value: The input value
       x: The x-coordinate if this input is an image
       y: The y-coordinate if this input is an image
    """

    type = ''
    name = ''
    value = ''

    x = 0
    y = 0
