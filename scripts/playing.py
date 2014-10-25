
def show_args(*args,**kwargs):
    print("Args:{}".format(",".join([str(x) for x in args])))
    for k,v in kwargs:
        print("kwargs[{}] = {}".format(k,v))


class PlayClass(object):

    @staticmethod
    def static_one(*args,**kwargs):
        print("This static method takes no arguments.")
        show_args(*args,**kwargs)

    @classmethod
    def class_one(cls,*args,**kwargs):
        print("This class method takes something..")
        print("Klass name:{}".format(cls.__name__))
        show_args(*args,**kwargs)



if __name__ == "__main__":
    PlayClass.static_one(1,2,3)
    PlayClass.class_one("a","b","c")
