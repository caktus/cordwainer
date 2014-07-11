Cordwainer
==========

A better CSV library

Features
--------

* Lets you program in both Python 2 and Python 3 as if you had the
  Python 3 CSV module.

 * Under Python 2, provides a Python 3 compatible `csv` module.
 * Under Python 3, passes through transparently.

* Lets your CSV files be encoded any way you want.

Python 3 compatibility
----------------------

``import cordwainer.csv as csv`` ought to be equivalent to importing the
Python 3 `csv` module, whether running with Python 2 or 3. See the
`Python 3 csv module documentation
<https://docs.python.org/3/library/csv.html>`_

CSV file encoding
-----------------

The Python 2 csv module expects file handles passed to it to
return data encoded in ASCII or UTF-8, and writes it to files
the same way.

The Python 3 csv module expects handles passed to it to return text
data, already decoded, and writes un-encoded text data to them. It's
your responsiblity to arrange for conversion when you open the file,
or pipe your stream through some kind of conversion.

Using Cordwainer, you can just pass an extra ``encoding`` parameter
to say that your stream is providing or expecting binary data
with the specified encoding, and Cordwainer will take care of
all necessary conversions.

If ``encoding`` is omitted or ``None``, Cordwainer assumes the
provided stream will provide or expect un-encoded text data, just
like Python 3's csv module.

Suppose you need to read a .CSV file that was written using `cp720`
encoding.  In Python 2, you would have to arrange to read it in,
decode the data to characters, then encode it again to `utf-8` before
you could pass it to the csv module.  To write out an updated file,
you have to do all that in reverse.

In Python 3, you still have to arrange to read it in and decode it
before passing to csv, and encode the output.

With Cordwainer, just pass in the encoding::

    import cordwainer.csv as csv

    f = open("cp720file.csv", "rb")
    reader = csv.reader(f, encoding="cp720")

    f = open("newcp270file.csv", "wb")
    writer = csv.writer(f, encoding="cp720")

Misc. Usage Notes
-----------------

The ``encoding`` parameter is *only* applied for reading from and
writing to streams.

String arguments should always be passed to the API
as characters, and results are always characters.

E.g.:

* Pass fieldnames to DictWriter as characters
* Pass data in rows to writerow() as characters
* next() returns rows in characters

Intended (eventually) features
------------------------------

* Optional header row
* Validate expected fields, types (probably specify a Django form
  to do the validation)
* Verbose error handling - say what the problem was on what line,
  for every line that has an error
* Optionally stop processing after N errors
* Optionally import the lines that are valid while skipping invalid
  ones
* Optionally do the whole thing in one transaction
* Optionally ignore any extra columns
* Optionally save uploaded file and then process it in a background
  task (to not delay the HTTP request)
* For Excel, be flexible in deciding what sheet to import - or even
  import from multiple sheets from one upload
