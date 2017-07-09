import gzip
from io import BytesIO

from construct import Int64ul, Int32ul, Int16ul, Int8ul, Bytes, GreedyBytes

from keecrypt.crypto import key, payload
from keecrypt.common import sha256

from keecrypt.exception import KDBXException
from keecrypt.exception import KDBXInvalidMasterKey
from keecrypt.exception import KDBXBlockIntegrityError


class KDBXParser:
    signature_primary = b'\x03\xD9\xA2\x9A'
    signature_secondary = b'\x67\xFB\x4B\xB5'

    def __init__(self, input_buffer):
        self.input_buffer = BytesIO()
        self.payload_data = BytesIO
        self.input_buffer = input_buffer
        self.file_version = (0, 0)
        self.headers = KDBXHeaders()
        self.payload_start = 0

        self.parse()

    def parse(self):
        self.check_identifiers()
        self.read_file_version()
        self.read_headers()

    def decrypt(self, password):
        password_key = key.PasswordKey(password)
        composite_key = key.CompositeKey()
        composite_key.add_key(password_key)
        master_key = composite_key.transform(self.headers.TRANSFORMSEED,
                                             self.headers.MASTERSEED,
                                             self.headers.TRANSFORMROUNDS)

        payload_data = payload.decrypt(self.read_payload(), master_key,
                                       self.headers.ENCRYPTIONIV,
                                       self.headers.CIPHERID)
        payload_buffer = BytesIO(payload_data)
        start_bytes_length = len(self.headers.STREAMSTARTBYTES)
        if payload_buffer.read(start_bytes_length) != self.headers.STREAMSTARTBYTES:
            raise KDBXInvalidMasterKey('invalid master key')

        blocks = {}
        block_size = -1
        while block_size != 0:
            block_id = Int32ul.parse(payload_buffer.read(4))
            block_hash = Bytes(32).parse(payload_buffer.read(32))
            block_size = Int32ul.parse(payload_buffer.read(4))
            if block_size != 0:
                block_data = payload_buffer.read(block_size)
                if sha256(block_data) != block_hash:
                    raise KDBXBlockIntegrityError
                if self.headers.COMPRESSIONFLAGS == 1:
                    block_data = gzip.decompress(block_data)
                blocks[block_id] = block_data
        return blocks

    def read_payload(self):
        self.input_buffer.seek(self.payload_start)
        return self.input_buffer.read()

    def check_identifiers(self):
        self.input_buffer.seek(0)
        sig_bytes = self.input_buffer.read(len(__class__.signature_primary))
        if __class__.signature_primary != sig_bytes:
            raise KDBXException("Not a valid KDBX file")
        sig_bytes_2 = self.input_buffer.read(len(__class__.signature_secondary))
        if __class__.signature_secondary != sig_bytes_2:
            raise KDBXException("Invalid Version of KDBX file")
        return True

    def read_file_version(self):
        self.input_buffer.seek(8)
        major_version = Int16ul.parse(self.input_buffer.read(2))
        minor_version = Int16ul.parse(self.input_buffer.read(2))
        self.file_version = (major_version, minor_version)
        return self.file_version

    def read_headers(self):
        self.input_buffer.seek(12)

        header_id = None
        while header_id is None or header_id != KDBXHeaders.END.type_id:
            header_id = Int8ul.parse(self.input_buffer.read(1))
            header_size = Int16ul.parse(self.input_buffer.read(2))
            header_data = self.input_buffer.read(header_size)
            if header_id != 0:
                self.headers.set_header(header_id, header_data)
        self.payload_start = self.input_buffer.tell()

        return self.headers


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

    def __init__(self):
        self.headers = {}

    def __getattribute__(self, item):
        item = super().__getattribute__(item)
        if isinstance(item, KDBXHeaderType):
            try:
                return self.headers[item.type_id]
            except KeyError:
                raise AttributeError(item)
        else:
            return item

    @classmethod
    def type_from_id(cls, type_id):
        for name, item in cls.__dict__.items():
            if isinstance(item, KDBXHeaderType):
                if item.type_id == type_id:
                    return item

    def set_header(self, type_id, data):
        header_type = self.type_from_id(type_id).value_type
        if header_type is not None:
            value = header_type.parse(data)
            self.headers[type_id] = value