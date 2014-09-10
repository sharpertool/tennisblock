import inspect

class Choice(object):
    class __metaclass__(type):
        def __init__(cls, *args, **kwargs):
            print "I am alive!"
            print cls

            cls._data = []

            for name,value in inspect.getmembers(cls):
                if not name.startswith("_") and not inspect.isfunction(value):
                    if isinstance(value,tuple) and len(value) > 1:
                        data = value
                    else:
                        data = (value, " ".join([x.capitalize() for x in name.split("_")]),)
                    cls._data.append(data)
                    setattr(cls, name, data[0])

            cls._hash = dict(cls._data)

        def __iter__(self):
            for value, data in self._data:
                yield value, data

    @classmethod
    def get_value(cls, key):
        return cls._hash[key]


class UserLevels(Choice):
    USER = 1
    MODERATOR = 2
    ADMIN = 3, "Super"
    NEW_FANGLED_USER = 4


print list(UserLevels)
print("Admin user level:{}".format(UserLevels.ADMIN))
print(Choice.get_value(3))


def print_this(self):
    print "Welcome to my world! Value:{}".format(self.value)

class my_metaclass(type):
    def __new__(cls, class_name, parents, attributes):
        print "- my_metaclass.__new__ - Creating class instance of type", cls
        return super(my_metaclass, cls).__new__(cls,
                                                class_name,
                                                parents,
                                                attributes)

    def __init__(cls, class_name, parents, attributes):
        print "- my_metaclass.__init__ - Initializing the class instance", cls
        super(my_metaclass, cls).__init__(class_name, parents,attributes)
        setattr(cls,'pt',print_this)

    def __call__(self, *args, **kwargs):
        print "- my_metaclass.__call__ - Creating object of type ", self
        return super(my_metaclass, self).__call__(*args, **kwargs)



class Validator(object):
    pass

class ValidateSize(Validator):
    pass

class MyBaseClass(object):
    __metaclass__ = my_metaclass

    def __new__(cls):
        print("Creating new class {}".format(cls))
        new_cls = (super(MyBaseClass,cls).__new__(cls))
        return new_cls


class MyClass(MyBaseClass):

    prop1 = ValidateSize()
    prop2 = ValidateSize()

    def __init__(self):
        self.value = "This is my class"

print("Starting off")
c = MyClass()
c.pt()

print("Done")

