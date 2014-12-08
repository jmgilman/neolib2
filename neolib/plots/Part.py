from neolib.NeolibBase import NeolibBase
from neolib.plots.Step import Step


class Part(NeolibBase):

    _links = []
    _steps = []

    def setup(self):
        pass

    def run(self, index=0):

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
        if 'form' in self._links[link]:
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
