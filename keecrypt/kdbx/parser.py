import gzip
from io import BytesIO

from construct import Int32ul, Int16ul, Int8ul, Bytes

from keecrypt.crypto import key, payload
from keecrypt.common import sha256, sha512, hmac_sha256, BufferedBytesIO
from keecrypt.exception import KDBXException, KDBXInvalidMasterKey, KDBXBlockIntegrityError
from keecrypt.kdbx import HmacBlockStream, VariantDictionary, KDBXHeaders


class KDBXParser:
    signature_primary = b'\x03\xD9\xA2\x9A'
    signature_secondary = b'\x67\xFB\x4B\xB5'

    def __init__(self, input_data):
        if isinstance(input_data, Bytes):
            self.input_buffer = BufferedBytesIO(input_data)
        else:
            self.input_buffer = BufferedBytesIO(input_data.read())

        self.file_version = (0, 0)
        self.headers = KDBXHeaders()
        self.payload_start = 0

        self.kdf_parameters = None
        self.public_custom_data = None

        self.parse()

    def parse(self):
        self.check_identifiers()
        self.read_file_version()
        self.read_headers()

    def get_transformed_keys(self, composite_key):
        kdf_uuid = self.kdf_parameters['$UUID']
        if kdf_uuid == b'\xEF\x63\x6D\xDF\x8C\x29\x44\x4B\x91\xF7\xA9\xA4\x03\xE3\x0A\x0C':
            intervals = self.kdf_parameters['I']
            memory = self.kdf_parameters['M'] // 1024
            parallelism = self.kdf_parameters['P']
            salt = self.kdf_parameters['S']
            version = self.kdf_parameters['V']
            master_key, hmac_key = composite_key.transform_argon2(salt, intervals, memory, parallelism, version)
        else:
            raise KDBXException('invalid key derivative function')
        return master_key, hmac_key

    def check_header_hash(self, hmac_key):
        header_hash = sha256(self.header_data)
        header_hash_file = self.input_buffer.read(32)
        if header_hash_file != header_hash:
            raise KDBXException('Invalid header data')
        header_hmac_file = self.input_buffer.read(32)
        header_hmac_key = sha512(b'\xFF' * 8 + hmac_key)
        header_hmac = hmac_sha256(header_hmac_key, self.header_data)
        if header_hmac_file != header_hmac:
            raise KDBXException('Invalid password')

    def read_data_blocks(self, block_stream, master_key):
        file_buffer = BytesIO()
        for block in block_stream.blocks:
            block_data = payload.decrypt(block.block_data, master_key,
                                         self.headers.ENCRYPTIONIV,
                                         self.headers.CIPHERID)
            block_data = block_data.strip(b'\x06')

            if self.headers.COMPRESSIONFLAGS != 0:
                block_data = gzip.decompress(block_data)
            file_buffer.write(block_data)
        return file_buffer.getvalue()

    def decrypt(self, password):
        password_key = key.PasswordKey(password)
        composite_key = key.CompositeKey(self.headers.MASTERSEED)
        composite_key.add_key(password_key)

        if not self.file_version[0] >= 4:
            return self.decrypt_kdbx3(composite_key)

        master_key, hmac_key = self.get_transformed_keys(composite_key)
        self.check_header_hash(hmac_key)

        hmac_block_stream = HmacBlockStream(self.input_buffer.read())
        hmac_block_stream.check_hmac(hmac_key)

        return self.read_data_blocks(hmac_block_stream, master_key)

    def check_identifiers(self):
        sig_bytes = self.input_buffer.read(len(self.signature_primary))
        if __class__.signature_primary != sig_bytes:
            raise KDBXException("Not a valid KDBX file")
        sig_bytes_2 = self.input_buffer.read(len(self.signature_secondary))
        if __class__.signature_secondary != sig_bytes_2:
            raise KDBXException("Invalid Version of KDBX file")
        return True

    def read_file_version(self):
        minor_version = Int16ul.parse(self.input_buffer.read(2))
        major_version = Int16ul.parse(self.input_buffer.read(2))
        self.file_version = (major_version, minor_version)
        return self.file_version

    def read_headers(self):
        header_size_length = 4 if self.file_version[0] >= 4 else 2
        header_size_type = Int32ul if self.file_version[0] >= 4 else Int16ul
        header_id = None
        while header_id is None or header_id != KDBXHeaders.END.type_id:
            header_id = Int8ul.parse(self.input_buffer.read(1))
            header_size = header_size_type.parse(self.input_buffer.read(header_size_length))
            header_data = self.input_buffer.read(header_size)
            if header_id != 0:
                self.headers.set_header(header_id, header_data)

        if self.file_version[0] >= 4:
            self.kdf_parameters = VariantDictionary(self.headers.KDFPARAMETERS)
            self.public_custom_data = VariantDictionary(self.headers.PUBLICCUSTOMDATA)

        self.header_data = self.input_buffer.reset_buffer()

        return self.headers

    # kdb3 specific stuff
    def decrypt_kdbx3(self, composite_key):
            master_key = composite_key.transform_aeskdf(self.headers.TRANSFORMSEED,
                                                        self.headers.TRANSFORMROUNDS)[0]

            payload_data = payload.decrypt(self.input_buffer.read(), master_key,
                                           self.headers.ENCRYPTIONIV,
                                           self.headers.CIPHERID)
            payload_buffer = BytesIO(payload_data)
            start_bytes_length = len(self.headers.STREAMSTARTBYTES)
            if payload_buffer.read(start_bytes_length) != self.headers.STREAMSTARTBYTES:
                raise KDBXInvalidMasterKey('invalid master key')

            file_data = BytesIO()
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
                    file_data.write(block_data)
            return file_data.getvalue()





