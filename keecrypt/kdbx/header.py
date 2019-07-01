from construct import Int32ul, Int64ul, GreedyBytes, Bytes

from keecrypt.exception import KDBXException


class KDBXHeaderType:
    def __init__(self, type_id, value_type):
        self.type_id = type_id
        self.value_type = value_type


class KDBXHeaders:
    END = KDBXHeaderType(0, None)  # type: None
    COMMENT = KDBXHeaderType(1, None)  # type: None
    CIPHERID = KDBXHeaderType(2, GreedyBytes)  # type: bytes
    COMPRESSIONFLAGS = KDBXHeaderType(3, Int32ul)  # type: int
    MASTERSEED = KDBXHeaderType(4, Bytes(32))  # type: bytes
    TRANSFORMSEED = KDBXHeaderType(5, GreedyBytes)  # type: bytes
    TRANSFORMROUNDS = KDBXHeaderType(6, Int64ul)  # type: int
    ENCRYPTIONIV = KDBXHeaderType(7, GreedyBytes)  # type: bytes
    PROTECTEDSTREAMKEY = KDBXHeaderType(8, GreedyBytes)  # type: bytes
    STREAMSTARTBYTES = KDBXHeaderType(9, GreedyBytes)  # type: bytes
    INNERRANDOMSTREAMID = KDBXHeaderType(10, Int32ul)  # type: int
    KDFPARAMETERS = KDBXHeaderType(11, GreedyBytes)  # type: bytes
    PUBLICCUSTOMDATA = KDBXHeaderType(12, GreedyBytes)  # type: bytes

    def __init__(self):
        self.headers = {}

    def __getattribute__(self, item):
        item = super().__getattribute__(item)
        if isinstance(item, KDBXHeaderType):
            try:
                return self.headers[item.type_id]
            except KeyError:
                return None
        else:
            return item

    @classmethod
    def type_from_id(cls, type_id):
        for _name, item in cls.__dict__.items():
            if isinstance(item, KDBXHeaderType):
                if item.type_id == type_id:
                    return item
        return None

    def set_header(self, type_id, data):
        header_type = self.type_from_id(type_id)
        if header_type:
            value = header_type.value_type.parse(data)
            self.headers[type_id] = value
        else:
            raise KDBXException('cannot set invalid header type')
