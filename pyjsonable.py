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

    def get_class_name(self):
        return self.__class__.__name__

    def validate(self):
        keys = set(self.keys())
        # validate required keys
        if not keys.issuperset(self.Meta.required_keys):
            raise AttributeError(self.get_class_name() + " requires: "
                + str([str(key) for key in self.Meta.required_keys]))

        # validate at_least_one_required keys
        if len(list(self.Meta.at_least_one_required_keys.intersection(keys))) < 1:
            raise AttributeError(self.get_class_name() + " requires at least one of: "
                + str([str(key) for key in self.Meta.at_least_one_required_keys]))

        # validate cannot coexist
        if len(list(keys.intersection(self.Meta.cannot_coexist_keys))) > 1:
            raise AttributeError(self.get_class_name() + " members cannot coexist: "
                + str([str(key) for key in self.Meta.cannot_coexist_keys]))

        if self.Meta.allowed_keys:
            all_allowed_keys = self.Meta.allowed_keys\
                .union(self.Meta.required_keys)\
                .union(self.Meta.at_least_one_required_keys)\
                .union(self.Meta.cannot_coexist_keys)
            if len(list(keys.difference( all_allowed_keys ))) > 0:
                raise AttributeError(self.get_class_name() + " only allows members: "
                + str([str(key) for key in all_allowed_keys]))

        return

    def __setitem__(self, key, value):
        super(StrictDict, self).__setitem__(key, value)

    def __getattr__(self, attr):
        return self[attr]

    def __setattr__(self, attr, value):
        self[attr] = value