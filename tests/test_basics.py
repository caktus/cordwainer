# -*- encoding: utf8 -*-
# Test the basic functions in the unicode-handling samples
# in the Python doc for CSV

# (Does not try to test the underlying csv library; leave that
# to the Python developers.)
from __future__ import unicode_literals
import codecs
import os.path
from unittest import TestCase
import six

import cordwainer.csv as csv3


class BasicsTest(TestCase):
    def setUp(self):
        this_dir = os.path.dirname(__file__)
        self.data_dir = os.path.join(this_dir, "test_data")
        self.rows = [
            ["head1", "hüad2", "head3"],
            ["4", "5", "6"],
            ["a b", "c d", "الأولى"]
        ]

    def test_reader(self):
        fname = os.path.join(self.data_dir, "utf8.csv")
        with open(fname, "rb") as f_binary:
            f = codecs.getreader("utf-8")(f_binary)
            reader = csv3.reader(f)
            rows = [row for row in reader]
            self.assertEqual(self.rows, rows)

    def test_reader_utf8(self):
        fname = os.path.join(self.data_dir, "utf8.csv")
        with open(fname, "rb") as f_binary:
            reader = csv3.reader(f_binary, encoding='utf-8')
            rows = [row for row in reader]
            self.assertEqual(self.rows, rows)

    def test_writer(self):
        # Get the output
        output = six.StringIO()
        w = csv3.writer(output, quoting=csv3.QUOTE_MINIMAL)
        w.writerow(["head1", "hüad2", "head3"])
        w.writerow(["a b", "c d", "الأولى"])
        result = output.getvalue()
        self.assertEqual("head1,hüad2,head3\r\na b,c d,الأولى\r\n", result)

    def test_writer_dialect(self):
        output = six.StringIO()
        delimiter = b'x' if six.PY2 else 'x'
        w = csv3.writer(output, quoting=csv3.QUOTE_ALL, delimiter=delimiter)
        dialect = w.dialect
        self.assertEqual(csv3.QUOTE_ALL, dialect.quoting)
        self.assertEqual(delimiter, dialect.delimiter)
        w = csv3.writer(output, quoting=csv3.QUOTE_NONE)
        dialect = w.dialect
        self.assertEqual(csv3.QUOTE_NONE, dialect.quoting)

    def test_writer_encodings(self):
        for encoding in ['utf-8']:
            output = six.BytesIO()
            w = csv3.writer(output, encoding=encoding,
                            lineterminator='\n')
            for row in self.rows:
                w.writerow(row)
            result = output.getvalue()
            chars = result.decode(encoding)
            fname = os.path.join(self.data_dir, "utf8.csv")
            expected = open(fname, "rb").read().decode('utf-8')
            self.assertEqual(expected, chars)
