from keecrypt.reader.kdbx import KDBXParser
from tests.utils import get_file
import struct

class TestParser:
    def test_signature_valid(self):
        test_file = open(get_file('valid_aes_gzip.kdbx'), 'rb')
        parser = KDBXParser(test_file)
        assert parser.check_identifiers()

    def test_read_version(self):
        test_file = open(get_file('valid_aes_gzip.kdbx'), 'rb')
        parser = KDBXParser(test_file)
        version = parser.read_file_version()
        assert version == (1, 3)

    def test_dynamic_headers(self):
        test_file = open(get_file('valid_aes_gzip.kdbx'), 'rb')
        parser = KDBXParser(test_file)
        headers = parser.read_dynamic_headers()

