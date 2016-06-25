import os


myvariable = "yada yada yada"


def get_uname():
    return os.uname()


def walk(directory_name):
    return os.walk(directory_name)


def get_environ(variable_name):
    return os.environ[variable_name]


class myclass:

    myclassattribute = "yada yada yada"

    def instance_method(self):
        return "instance: %s" % os.uname()[1]

    @staticmethod
    def static_method():
        return "static: %s" % os.uname()[1]

    @classmethod
    def class_method(cls):
        return "class: %s" % os.uname()[1]
