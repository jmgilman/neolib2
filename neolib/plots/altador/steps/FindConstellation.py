from collections import namedtuple

from neolib.plots.Step import Step


class FindConstellation(Step):

    link = [
        'http://www.neopets.com/altador/astro.phtml?get_star_data=1',
        'http://www.neopets.com/altador/astro.phtml?star_submit=',
    ]

    _const = ''

    _X_OFFSETS = [60, 120, 130, 190, 110]
    _Y_OFFSETS = [-20, 0, 40, 60, -90]

    _OFFSETS = {
        'sleeper': ((40, -30), (80, -60), (120, -60), (160, -30), (200, 0)),
        'dreamer': ((60, -20), (120, 0), (130, 40), (190, 60), (110, -90)),
        'first_to_rise': ((20, 60), (80, 80), (160, 0), (140, -60), (80, -80)),
        'farmer': ((140, -30), (10, -80), (120, -60), (160, -70), (80, 60)),
        'dancer': ((60, -30), (120, 0), (0, 140), (60, 170), (120, 140)),
        'wave': ((50, 70), (170, 40), (200, 0), (190, -90), (140, -10)),
        'gladiator': ((70, 30), (140, 0), (40, -120), (70, -140), (100, -120)),
        'collector': ((10, -50), (100, -130), (100, 10), (190, -50), (200, 0)),
        'thief': ((40, 40), (20, -40), (40, -80), (-50, -10), (-60, 120)),
        'gatherer': ((40, -70), (-30, -140), (10, -200), (110, -170), (120, -90)),
        'protector': ((-70, 0), (70, 0), (0, -70), (0, 70), (-130, 90)),
        'hunter': ((10, -140), (120, -60), (160, -190), (170, -20), (200, 0)),
    }

    def __init__(self, usr, const):
        super().__init__(usr, '', '', False)

        self.link = [
            'http://www.neopets.com/altador/astro.phtml?get_star_data=1',
            'http://www.neopets.com/altador/astro.phtml?star_submit=',
        ]

        self._const = const

    def execute(self, last_pg=None):
        # Fetch the star data
        pg = self._usr.get_page(self.link[0])

        # Clear garbage
        pg.content = pg.content.split(':')[0]

        # Separate the cords
        str_cords = pg.content.split('|')

        # Make this more meaningful
        Point = namedtuple('Point', ['x', 'y'])
        cords = []
        for cord in str_cords:
            d = cord.split(',')

            p = Point(int(d[0]), int(d[1]))
            cords.append(p)

        # Starting from the first point the proceeding points always follow
        # the same offsets as defined in _OFFSETS
        for cord in cords:
            matches = []
            for p in self._OFFSETS[self._const]:
                if Point(cord.x + p[0], cord.y + p[1]) in cords:
                    matches.append(Point(cord.x + p[0], cord.y + p[1]))

            if len(matches) == 5:
                matches = [cord] + matches
                break

        # There should be 6 points if we found the constellation
        if len(matches) != 6:
            return False

        # Now we have to connect the points to each other
        url = self._connect_all(matches, self._const)
        print('URL: ' + url)

        # Submit the points
        pg = self._usr.get_page(url)

        # Check the result
        print('Content: ' + pg.content)
        if '0' not in pg.content:
            return True
        else:
            return False

    def _connect_all(self, points, const):
        if const is 'sleeper':
            line1 = self._connect(points[0], points[1]) + '|'
            line1 += self._connect(points[1], points[0]) + '|'
            line1 += self._connect(points[1], points[2]) + '|'
            line1 += self._connect(points[2], points[1]) + '|'

            line2 = self._connect(points[3], points[4]) + '|'
            line2 += self._connect(points[4], points[3]) + '|'
            line2 += self._connect(points[4], points[5]) + '|'
            line2 += self._connect(points[5], points[4])

            return self.link[1] + line1 + line2
        elif const is 'dreamer':
            line = self._connect(points[0], points[1]) + '|'
            line += self._connect(points[1], points[0]) + '|'
            line += self._connect(points[1], points[2]) + '|'
            line += self._connect(points[2], points[1]) + '|'
            line += self._connect(points[2], points[3]) + '|'
            line += self._connect(points[3], points[2]) + '|'
            line += self._connect(points[3], points[4]) + '|'
            line += self._connect(points[4], points[3]) + '|'

            point = self._p_to_str(points[5])

            return self.link[1] + line + point
        elif const is 'first_to_rise':
            line1 = self._connect(points[0], points[1]) + '|'
            line1 += self._connect(points[1], points[0]) + '|'
            line1 += self._connect(points[1], points[2]) + '|'
            line1 += self._connect(points[2], points[1]) + '|'

            line2 = self._connect(points[3], points[4]) + '|'
            line2 += self._connect(points[4], points[3]) + '|'
            line2 += self._connect(points[4], points[5]) + '|'
            line2 += self._connect(points[5], points[4])

            return self.link[1] + line1 + line2
        elif const is 'farmer':
            line = self._connect(points[0], points[1]) + '|'
            line += self._connect(points[1], points[0]) + '|'

            line += self._connect(points[2], points[3]) + '|'
            line += self._connect(points[3], points[2]) + '|'

            line += self._connect(points[3], points[4]) + '|'
            line += self._connect(points[4], points[3]) + '|'

            line += self._connect(points[1], points[4]) + '|'
            line += self._connect(points[4], points[1]) + '|'

            line += self._connect(points[1], points[5]) + '|'
            line += self._connect(points[5], points[1])

            return self.link[1] + line

    def _connect(self, point1, point2):
        return self._p_to_str(point1) + ';' + self._p_to_str(point2)

    def _p_to_str(self, point):
        return str(point.x) + ',' + str(point.y)
