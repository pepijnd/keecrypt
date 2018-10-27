from io import BytesIO

from construct import Int8ul, Int32ul, Int64ul, Int32sl, Int64sl

from keecrypt.exception import KDBXException


class VariantDictionary:
    types = {
        b'\x04': Int32ul.parse,
        b'\x05': Int64ul.parse,
        b'\x08': lambda x: bool(x != b'\x00'),
        b'\x0C': Int32sl.parse,
        b'\x0D': Int64sl.parse,
        b'\x18': lambda x: x.decode('utf-8'),
        b'\x42': lambda x: x
    }

    def __init__(self, data):
        self.data = data
        self.items = {}
        self.version = (0, 0)

        self.decode()

    def decode(self):
        if not self.data:
            return
        buffer = BytesIO(self.data)
        version_minor = Int8ul.parse(buffer.read(1))
        version_major = Int8ul.parse(buffer.read(1))
        self.version = (version_major, version_minor)
        if self.version[0] != 1:
            raise KDBXException('invalid variantdict version')

        while True:
            value_type = buffer.read(1)
            if value_type == b'\x00':
                break
            value_parser = self.types[value_type]
            key_length = Int32ul.parse(buffer.read(4))
            key_name = buffer.read(key_length).decode('utf-8')
            value_length = Int32ul.parse(buffer.read(4))
            value = value_parser(buffer.read(value_length))
            self.items[key_name] = value

    def __getitem__(self, item):
        if item in self.items:
            return self.items[item]
        else:
            raise KeyError()
