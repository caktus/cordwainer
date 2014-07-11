import six


def encode_list(list_, encoding):
    if encoding:
        return [s.encode(encoding) for s in list_]
    return list_


def decode_list(list_, encoding):
    if encoding:
        return [s.decode(encoding) for s in list_]
    return list_


def decode_thing(thing, encoding):
    if not encoding:
        return thing
    if isinstance(thing, six.binary_type):
        return thing.decode(encoding)
    if hasattr(thing, '__iter__'):
        return decode_list(thing, encoding)
    # Punt
    return thing.decode(encoding)


def encode_thing(thing, encoding):
    if not encoding:
        return thing
    if isinstance(thing, six.text_type):
        return thing.encode(encoding)
    if hasattr(thing, '__iter__'):
        return encode_list(thing, encoding)
    return thing.encode(encoding)


def change_encoding(item, from_, to):
    if from_ == to:
        return item
    return encode_thing(decode_thing(item, from_), to)


class RecodingReader(six.Iterator):
    def __init__(self, stream, from_, to):
        self.stream = stream
        self.from_ = from_
        self.to = to

    def __next__(self):
        return change_encoding(six.next(self.stream), self.from_, self.to)

    def __iter__(self):
        return self
