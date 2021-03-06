class StrictDict(dict):
    class Meta:
        required_keys=set()
        at_least_one_required_keys=set()
        cannot_coexist_keys=set()
        allowed_keys=set()
        item_type={}

    def __init__(self, iterable={}, **kwargs):
        super(StrictDict, self).__init__({})
        keys = set(iterable.keys()).union(kwargs.keys())
        self.validate_required_keys(keys)
        self.validate_at_least_one_required_keys(keys)
        for key, val in iterable.iteritems():
            self.__setitem__(key, val)
        for key, val in kwargs.iteritems():
            self.__setitem__(key, val)

    def __setitem__(self, key, value):
        self.validate_attr_is_allowed(attr=key, value=value)
        self.validate_attr_cannot_coexist(attr=key, value=value)
        self.validate_attr_class(attr=key, value=value)
        # self[key] = value
        super(StrictDict, self).__setitem__(key, value)

    def __getattr__(self, attr):
        # Allows getting via dot notation
        return self.__getitem__(attr)

    def __setattr__(self, attr, value):
        # Allows setting via dot notation
        self.__setitem__(attr, value)

    def update(self, iterable={}, **kwargs):
        for key, val in iterable.iteritems():
            self.__setitem__(key, val)
        for key, val in kwargs.iteritems():
            self.__setitem__(key, val)
        super(StrictDict, self).update({})

    def get_class_name(self):
        return self.__class__.__name__

    def validate_required_keys(self, keys):
        required_keys = getattr(self.Meta, "required_keys", set())
        if len(list(required_keys.difference( keys ))) > 0:
            raise AttributeError(self.get_class_name() + " requires: "
                + str([str(key) for key in required_keys]))

    def validate_at_least_one_required_keys(self, keys):
        at_least_one_required_keys = getattr(self.Meta, "at_least_one_required_keys", set())
        if at_least_one_required_keys and len(list(at_least_one_required_keys.intersection( keys ))) < 1:
            raise AttributeError(self.get_class_name() + " requires at least one of: "
                + str([str(key) for key in at_least_one_required_keys]))

    def validate_attr_cannot_coexist(self, attr, value):
        keys = set(self.keys())
        # validate cannot coexist
        cannot_coexist_keys = getattr(self.Meta, "cannot_coexist_keys", set())
        if attr in cannot_coexist_keys and len(list(keys.intersection(cannot_coexist_keys))) >= 1:
            raise AttributeError(self.get_class_name() + " members cannot coexist: "
                + str([str(key) for key in cannot_coexist_keys]))

    def validate_attr_is_allowed(self, attr, value):
        keys = set(self.keys())
        # validate allowed keys (union with other sets if present)
        allowed_keys = getattr(self.Meta, "allowed_keys", set())
        required_keys = getattr(self.Meta, "required_keys", set())
        at_least_one_required_keys = getattr(self.Meta, "at_least_one_required_keys", set())
        cannot_coexist_keys = getattr(self.Meta, "cannot_coexist_keys", set())
        if allowed_keys:
            all_allowed_keys = allowed_keys\
                .union( required_keys )\
                .union( at_least_one_required_keys )\
                .union( cannot_coexist_keys )
            if attr not in all_allowed_keys:
                raise AttributeError(self.get_class_name() + " does not allow member " + attr + "."\
                + " Allowed members: " + str([str(key) for key in all_allowed_keys]))

    def validate_attr_class(self, attr, value):
        item_type = getattr(self.Meta, "item_type", None)
        if not item_type:
            return

        msg_part = self.get_class_name() + " member '" + attr + "'"\
            + " be of type "

        # Case where a single type is declared for all dict values
        if not isinstance(item_type, dict):
            AttrClass = item_type
            if not isinstance(value, item_type):
                raise TypeError(msg_part + str(AttrClass))
            return

        # Case where an type map was declared but this attr not present in map
        if not attr in item_type.keys():
            return

        # The item from the type map
        mapped_item_type = item_type.get(attr)

        # Case where a single type is declared for this attribute
        if not isinstance(mapped_item_type, dict):
            AttrClass = mapped_item_type
            if not isinstance(value, AttrClass):
                raise TypeError(msg_part + str(AttrClass))
            return

        # Case where a complex dict with members "type" and "nullable" declared for this attribute
        AttrClass = mapped_item_type.get("type")
        nullable = mapped_item_type.get("nullable", False)

        if (nullable and value == None) or isinstance(value, AttrClass):
            return

        msg = msg_part + str(AttrClass)
        if nullable:
            msg += " or None"
        raise TypeError(msg)

class StrictList(list):
    class Meta:
        item_type = basestring

    def __init__(self, *args):
        # super(StrictList, self).__init__()
        for item in (list(args)):
            self.append(item)

    def get_class_name(self):
        return self.__class__.__name__

    def append(self, item):
        if not isinstance(item, self.Meta.item_type):
            raise TypeError(self.get_class_name() + " items must be of type " +\
                  str(self.Meta.item_type))
        super(StrictList, self).append(item)