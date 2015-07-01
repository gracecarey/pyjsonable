class StrictDict(dict):
    class Meta:
        required_keys=set()
        at_least_one_required_keys=set()
        cannot_coexist_keys=set()
        allowed_keys=set()

    def __init__(self, iterable={}, **kwargs):
        super(StrictDict, self).__init__({})
        for key, val in iterable.iteritems():
            self.__setitem__(key, val)
        for key, val in kwargs.iteritems():
            self.__setitem__(key, val)

    def update(self, iterable={}, **kwargs):
        for key, val in iterable.iteritems():
            self.__setitem__(key, val)
        for key, val in kwargs.iteritems():
            self.__setitem__(key, val)
        super(StrictDict, self).update({})

    def __setitem__(self, key, value):
        super(StrictDict, self).__setitem__(key, value)

    def __getattr__(self, attr):
        return self[attr]

    def __setattr__(self, attr, value):
        self[attr] = value