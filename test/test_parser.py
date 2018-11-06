from keecrypt.kdbx.parser import KDBXParser
from test.utils import get_file


class TestParser:
    def test_decrypt_payload(self):
        test_file = open(get_file('valid_aeskdf_aes_gzip_kdbx31.kdbx'), 'rb')
        parser = KDBXParser(test_file)
        assert parser.decrypt('test_file')

