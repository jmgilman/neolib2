from collections import UserList

from neolib.item.ItemList import ItemList


class WizardItemList(ItemList):
    """ Represents the results from a Shop Wizard search """

    query_types = [
        'contains',
        'startswith',
        'endswith'
        'gt',
        'lt',
    ]

    _log_name = 'neolib.item.WizardItemList'

    def buy(self):
        """ Attempts to buy all items in the current item list

        Returns:
            List of items that were purchased
        """
        success = []
        for item in self.data:
            if item.buy():
                success.append(item)

        return success

    def find(self, **kwargs):
        """ Searches the current results using keyword arguments

        Loops through each keyword argument and searches the current results
        for any item that has an attribute (key name) that matches a value
        (key value).

        Args
            **kwargs**: Keyword arguments used for searching

        Returns
            A list of items that match the search

        Example
            low = results.find(price__lt=1000)[0]
        """
        matches = []

        for item in self.data:
            match = 0
            for key in kwargs.keys():
                try:
                    # Determine if this query has extra arguments
                    if '__' in key:
                        arg = key.split('__')[1]
                        atrib = key.split('__')[0]
                        value = getattr(item, atrib)

                        if arg not in self.query_types:
                            continue

                        if arg == 'contains' and type(value) is str:
                            if kwargs[key] in value:
                                match += 1
                        elif arg == 'startswith' and type(value) is str:
                            if value.startswith(kwargs[key]):
                                match += 1
                        elif arg == 'endswith' and type(value) is str:
                            if value.endswith(kwargs[key]):
                                match += 1
                        elif arg == 'gt' and self._is_int(value):
                            if int(value) > int(kwargs[key]):
                                match += 1
                        elif arg == 'lt' and self._is_init(value):
                            if int(value) < int(kwargs[key]):
                                match += 1
                    else:
                        value = getattr(item, key)
                        if kwargs[key] == value:
                            match += 1
                except Exception:
                    continue

            if match == len(kwargs.keys()):
                matches.append(item)

        return WizardItemList(self._usr, matches)

    def __getitem__(self, item):
        result = UserList.__getitem__(self, item)
        if type(result) is list:
            if len(result) > 1:
                return WizardItemList(self._usr, result)
        else:
            return result

    def __repr__(self):
        return 'Shop Wizard Results <' + str(len(self.data)) + ' Items>'
