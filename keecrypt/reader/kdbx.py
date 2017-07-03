import struct

from io import BytesIO


class KDBXReader:
    def __init__(self):
        pass

    @classmethod
    def open(cls, input_file):
        pass


class KDBXParser:
    signature_primary   = b'\x03\xD9\xA2\x9A'
    signature_secondary = b'\x67\xFB\x4B\xB5'

    def __init__(self, input_file):
        self.input_file = input_file  # type: BytesIO
        self.file_version = (0, 0)
        self.headers = {}

    def parse(self):
        self.check_identifiers()
        self.file_version = self.read_file_version()
        self.headers = {(header.id, header) for header in self.read_dynamic_headers()}

        self.payload_size = struct.unpack()

    def check_identifiers(self):
        self.input_file.seek(0)
        sig_bytes = self.input_file.read(len(__class__.signature_primary))
        if __class__.signature_primary != sig_bytes:
            raise KDBXException("Not a valid KDBX file")
        sig_bytes_2 = self.input_file.read(len(__class__.signature_secondary))
        if __class__.signature_secondary != sig_bytes_2:
            raise KDBXException("Invalid Version of KDBX file")
        return True

    def read_file_version(self):
        self.input_file.seek(8)
        version_bytes = self.input_file.read(4)
        version = struct.unpack('<HH', version_bytes)
        return version

    def read_dynamic_headers(self):
        self.input_file.seek(12)

        header = None
        headers = []
        while header is None or header.id != KDBXHeader.END:
            header = self.read_dynamic_header()
            headers.append(header)

        return headers

    def read_dynamic_header(self):
        header_bytes = self.input_file.read(3)
        header = struct.unpack('<BH', header_bytes)
        if header[1] != 0:
            header_data = self.input_file.read(header[1])
        else:
            header_data = b''
        return KDBXHeader(header[0], header[1], header_data)

    def read_payload(self):
        pass



class KDBXHeader:
    END = 0
    COMMENT = 1
    CIPHERID = 2
    COMPRESSIONFLAGS = 3
    MASTERSEED = 4
    TRANSFORMSEED = 5
    TRANSFORMROUNDS = 6
    ENCRYPTIONIV = 7
    PROTECTEDSTREAMKEY = 8
    STREAMSTARTBYTES = 9
    INNERRANDOMSTREAMID = 10

    def __init__(self, id, size, data):
        self.id = id
        self.size = size
        self.data = data


class KDBXException(IOError):
    pass

