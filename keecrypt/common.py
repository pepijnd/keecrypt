import hashlib
import hmac
from io import BytesIO


def sha256(string):
    return hashlib.sha256(string).digest()


def sha512(string):
    return hashlib.sha512(string).digest()


def hmac_sha256(key, value):
    return hmac.new(key, value, hashlib.sha256).digest()


class BufferedBytesIO(BytesIO):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.__buffer = BytesIO()

    def read(self, *args, **kwargs):
        data = super().read(*args, **kwargs)
        self.__buffer.write(data)
        return data

    @property
    def buffer(self):
        return self.__buffer

    @property
    def buffer_data(self):
        return self.__buffer.getvalue()

    def reset_buffer(self):
        buffer = self.buffer_data
        self.__buffer = BytesIO()
        return buffer
