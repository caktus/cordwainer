# -*- encoding: utf8 -*-
# Some code used in this module was taken from the python documentation and
# can be found in http://docs.python.org/2/library/csv.html
# Modified by Caktus.
from __future__ import unicode_literals, absolute_import


__all__ = ["DictReader", "DictWriter"]


from csv import DictReader as BaseDictReader, DictWriter as BaseDictWriter


class DictReader(BaseDictReader):
    def __init__(self, f, fieldnames=None, restkey=None, restval=None,
                 dialect="excel",
                 encoding=None,
                 *args, **kwds):
        BaseDictReader.__init__(self, f=f, fieldnames=fieldnames,
                                restkey=restkey, restval=restval,
                                dialect=dialect,
                                *args, **kwds)
        from .csv import reader
        self.reader = reader(f, dialect=dialect,
                             encoding=encoding,
                             **kwds)


class DictWriter(BaseDictWriter):
    def __init__(self, f, fieldnames, restval="", extrasaction="raise",
                 dialect="excel",
                 encoding=None,
                 *args, **kwds):
        from .csv import Writer

        BaseDictWriter.__init__(self, f=f, fieldnames=fieldnames,
                                restval=restval, extrasaction=extrasaction,
                                dialect=dialect, *args, **kwds)
        self.writer = Writer(csvfile=f, dialect=dialect, encoding=encoding,
                             **kwds)
        self.encoding = encoding
