from neolib.NeolibBase import NeolibBase
from neolib.plots.Step import Step


class Part(NeolibBase):
    """ Represents a particular portion of a Neopets plot

    This class should be inherited to provide uniformity when it comes to
    completing a length Neopets plot. There's no standard to how many steps a
    part should have so personal discretion should be applied.
    """
    _links = []
    _steps = []

    def setup(self):
        """ Should be overriden to setup necessary steps for this part """
        pass

    def run(self, index=0):
        """ Runs all steps in this part in order

        This method loops through all of the steps provided in the setup()
        function and executes each one in order by calling the step's execute()
        method. A 5 - 10 second pause between each step is enforced for user
        safety.

        Arguments:
            | **index**: The step to start at for this part

        Returns:
            Boolean value indicating if all steps were successful or not
        """
        if index > 0:
            max = len(self._steps)
            self._steps = self._steps[index-1:max]
            i = index
        else:
            i = 1

        pg = None
        for step in self._steps:
            print('Executing step ' + str(i))

            if step.form:
                pg = step.execute(pg)
            elif step.path:
                pg = step.execute(pg)
            else:
                pg = step.execute()

            if not pg:
                self._logger.warning('Failed part one of Altador plot on step ' + str(i))
                return False

            self._wait_random(10)
            i += 1

        return False

    def _append(self, link):
        if 'form' in self._links[link] and 'path' in self._links[link]:
            self._steps.append(Step(self._usr, self._links[link]['link'],
                                    self._links[link]['checks'],
                                    form=self._links[link]['form'],
                                    path=self._links[link]['path']))
        elif 'form' in self._links[link]:
            self._steps.append(Step(self._usr, self._links[link]['link'],
                                    self._links[link]['checks'],
                                    form=self._links[link]['form']))
        elif 'path' in self._links[link]:
            self._steps.append(Step(self._usr, self._links[link]['link'],
                                    self._links[link]['checks'],
                                    path=self._links[link]['path']))
        else:
            self._steps.append(Step(self._usr, self._links[link]['link'],
                                    self._links[link]['checks']))

    def _append_existing(self, step):
        self._steps.append(step)
