def source_for_autocomplete(source, marker="/*POINT*/"):
    for row, line in enumerate(source.split("\n"), start=1):
        if marker in line:
            col = line.index(marker) + 1
            return (row, col), source.replace(marker, "")


class CFuncDescriptor(object):
    """
    Descriptor protocol implementation to
    declare a libclang-function which is
    lazy-loaded
    """

    def __init__(self, name, restype, argtypes, errcheck):
        self.name = name
        self.restype = restype
        self.argtypes = argtypes
        self.errcheck = errcheck


    def __get__(self, instance, clazz):
        assert clazz.LIB is not None, "You must invoke setup with a valid libclang.dylib first!"
        f = getattr(clazz.LIB, self.name)
        f.restype = self.restype
        f.argtypes = self.argtypes
        if self.errcheck is not None:
            f.errcheck = self.errcheck
        # replace ourselves with the
        # actual function to speed up
        # a little
        setattr(clazz, self.name, f)
        return f


def cfunc(restype, arglist, errcheck=None):

    def d(func):
        fname = func.func_name
        return CFuncDescriptor(fname, restype, arglist, errcheck)

    return d

