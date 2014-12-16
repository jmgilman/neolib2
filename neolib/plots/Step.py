from neolib.NeolibBase import NeolibBase


class Step(NeolibBase):
    """ Represents one step in a part of a Neopets plot

    This class should be utilized to perform a step in a Neopets plot. For
    example, navigating to a specific page and checking for a condition or
    submitting a particular form. This class can also be overriden to perform
    complex steps that involve more than just navigating to a page and checking
    for a condition.

    Attributes:
        | **link**: The url that will be navigated to for this step
        | **checks**: A list of strings to search the resulting page for to test
            if the step was successful or not
        | **form**: Whether the link provided is the action item of a form on
            the previous page or not
        | **path**: An xpath query to be used to determine the link for this
            step using the page from the previous step
    """
    link = None
    checks = []
    form = False
    path = None

    def __init__(self, usr, link, checks, form=False, path=None):
        super().__init__(usr)

        self.link = link
        self.checks = checks
        self.form = form
        self.path = path

    def execute(self, last_pg=None):
        """ Executes the step

        The method of execution depends on the provided data during
        intialization as well as the `last_pg` argument to this method. If the
        `form` attribute for this step is False and the `path` attribute is not
        set then the method will navigate to the provided `link` attribute and
        apply the strings in `checks` to the resulting page and return the
        status. If `form` is set to True and `last_pg` is provided then the method
        will search `last_pg` for a form with an action item equal to this
        step's `link` value. If a form is found it will submit the form and
        return the result. Finally, if `path` and `last_pg` are set then the
        method will search `last_pg` using the xpath query in `path` (which
        should return a URL) and then navigate to the resulting URL and apply
        the strings in `checks` to the resulting page and return the result.

        Arguments:
            **last_pg**: The page resulting from the step before this step (Optional)

        Returns:
            The resulting page of the step or None if the step failed
        """
        if not self.form and not self.path:
            pg = self._usr.get_page(self.link)
        elif self.form and self.path:
            link = last_pg.xpath(self.path)[0]
            print('Link:' + link)

            form = last_pg.form(action=link)[0]
            pg = form.submit(self._usr)
        elif self.form:
            print('Link:' + self.link)
            form = last_pg.form(action=self.link)[0]
            pg = form.submit(self._usr)
        elif self.path:
            url = self._base_url + last_pg.xpath(self.path[0])[(self.path[1])]
            pg = self._usr.get_page(url)

        f = open('test.html', 'w', encoding='utf-8')
        f.write(pg.content)
        f.close()

        for check in self.checks:
            if check in pg.content:
                return pg

        return None
