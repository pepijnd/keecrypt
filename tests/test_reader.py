from keecrypt.kdbx.parser import KDBXParser
from tests.utils import get_file


class TestParser:
    def test_decrypt_payload(self):
        test_file = open(get_file('valid_aes_gzip.kdbx'), 'rb')
        parser = KDBXParser(test_file)
        assert parser.decrypt('test_file')

