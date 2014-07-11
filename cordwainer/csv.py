# -*- encoding: utf8 -*-
# Some code used in this module was taken from the python documentation and
# can be found in http://docs.python.org/2/library/csv.html
# Modified by Caktus.
from __future__ import unicode_literals, absolute_import
import codecs

import six
from .utils import encode_list, decode_list, change_encoding, RecodingReader


__all__ = [ "QUOTE_MINIMAL", "QUOTE_ALL", "QUOTE_NONNUMERIC", "QUOTE_NONE",
            "Error", "Dialect", "__doc__", "excel", "excel_tab",
            "field_size_limit", "reader", "writer",
            "register_dialect", "get_dialect", "list_dialects", "Sniffer",
            "unregister_dialect", "__version__", "DictReader", "DictWriter" ]

# This file provides Python 3 compatible versions of the main tools
# in the csv module, with some added features.

# Provide everything from csv that we don't override
from csv import *  # flake8: noqa

# We want access to the stuff in csv ourselves, without getting
# confused aobut the things we've overridden
import csv

# Dicts are in another file, but let them be imported from here
from .dicts import DictReader, DictWriter


if six.PY2:
    # The built-in csv module expects streams to provide utf-8 encoded
    # data, and writes it that way to streams too.
    INTERNAL_ENCODING = 'utf-8'

if six.PY3:
    # Streams in and out of the built-in csv module are characters.
    INTERNAL_ENCODING = None


def reader(csvfile, dialect=excel, encoding=None, **kwargs):
    """
    Like Python 3's `csv.reader`, plus:

    * Can pass a byte stream and an encoding, and Reader will take
      care of decoding as it reads.
    * All results are strings
    * Can be used in Python 2.

    :param string encoding: If specified, `csvfile` is a byte stream
    with the specified encoding. `Reader` will decode it to string
    before processing it.  If None, `csvfile` is a character stream and
    `Reader` will not try to decode it.
    """
    return Reader(csvfile, dialect, encoding, **kwargs)


class Reader(six.Iterator):
    def __init__(self, csvfile, dialect=excel, encoding=None, **kwargs):
        self.line_num = 0
        self.csv_reader = csv.reader(
            RecodingReader(csvfile, from_=encoding, to=INTERNAL_ENCODING),
            dialect=dialect,
            **kwargs
        )

    def __next__(self):
        """Return next row, always as characters"""
        self.line_num += 1
        row = six.next(self.csv_reader)
        # Might need to decode it.
        return decode_list(row, INTERNAL_ENCODING)

    def __iter__(self):
        return self


class Writer(object):
    def __init__(self, csvfile, dialect='excel', encoding=None, **fmtparams):
        self.stream = csvfile
        self.queue = six.BytesIO() if six.PY2 else six.StringIO()
        self.writer = csv.writer(self.queue, dialect, **fmtparams)
        self.encoding = encoding

    @property
    def dialect(self):
        return self.writer.dialect

    def get_queue_data(self):
        """Return whatever data is in the queue, and clear out the queue"""
        data = self.queue.getvalue()
        self.queue.truncate(0)
        # You would think truncating would reset the file position,
        # but NOOOOOO......
        self.queue.seek(0)
        return data

    def writerow(self, row):
        # Write data to internal writer
        self.writer.writerow(change_encoding(row, from_=None, to=INTERNAL_ENCODING))
        # Get what it sent out
        data = self.get_queue_data()
        # Change that encoding to what we want to send to the output stream and write it
        out_data = change_encoding(data, from_=INTERNAL_ENCODING, to=self.encoding)
        self.stream.write(out_data)


def writer(csvfile, dialect='excel', encoding=None, **fmtparams):
    return Writer(csvfile, dialect, encoding, **fmtparams)
