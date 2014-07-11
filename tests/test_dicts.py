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


class DictsTest(TestCase):
    def setUp(self):
        this_dir = os.path.dirname(__file__)
        self.data_dir = os.path.join(this_dir, "test_data")

    def test_dictreader(self):
        fname = os.path.join(self.data_dir, "utf8.csv")
        with open(fname, "rb") as f_binary:
            f = codecs.getreader('utf-8')(f_binary)
            reader = csv3.DictReader(f)
            rows = [row for row in reader]
            self.assertEqual(["head1", "hüad2", "head3"], reader.fieldnames)
            obj1 = dict(zip(["head1", "hüad2", "head3"], ["4", "5", "6"]))
            self.assertEqual(obj1, rows[0])
            obj2 = dict(zip(["head1", "hüad2", "head3"],
                            ["a b", "c d", "الأولى"]))
            self.assertEqual(obj2, rows[1])

    def test_dictreader_encodings(self):
        for encoding in ['utf-8']:
            fname = os.path.join(self.data_dir, "utf8.csv")
            with open(fname, "rb") as f_binary:
                data = f_binary.read().decode('utf-8')
            encoded_data = data.encode(encoding)
            input = six.BytesIO(encoded_data)
            reader = csv3.DictReader(input, encoding=encoding)
            rows = [row for row in reader]
            self.assertEqual(["head1", "hüad2", "head3"], reader.fieldnames)
            obj1 = dict(zip(["head1", "hüad2", "head3"], ["4", "5", "6"]))
            self.assertEqual(obj1, rows[0])
            obj2 = dict(zip(["head1", "hüad2", "head3"],
                            ["a b", "c d", "الأولى"]))
            self.assertEqual(obj2, rows[1])

    def test_dictwriter(self):
        output = six.StringIO()
        fieldnames = ["head1", "hüad2", "head3"]
        w = csv3.DictWriter(output, fieldnames)
        obj1 = dict(zip(["head1", "hüad2", "head3"],
                        ["4", "5", "6"]))
        obj2 = dict(zip(["head1", "hüad2", "head3"],
                        ["a b", "c d", "الأولى"]))
        w.writeheader()
        w.writerow(obj1)
        w.writerow(obj2)
        result = output.getvalue()
        self.assertEqual("head1,hüad2,head3\r\n4,5,6\r\na b,c d,الأولى\r\n",
                         result)

    def test_dictwriter_encodings(self):
        for encoding in ['utf-8', 'cp720']:
            output = six.BytesIO()
            fieldnames = ["head1", "head2", "head3"]
            w = csv3.DictWriter(output,
                                fieldnames,
                                encoding=encoding)
            obj1 = dict(zip(fieldnames,
                            ["4", "5", "6"]))
            obj2 = dict(zip(fieldnames,
                            ["a b", "c d", "الأولى"]))
            w.writeheader()
            w.writerow(obj1)
            w.writerow(obj2)
            data = output.getvalue()
            result = data.decode(encoding)
            self.assertEqual("head1,head2,head3\r\n"
                             "4,5,6\r\n"
                             "a b,c d,الأولى\r\n",
                             result)
