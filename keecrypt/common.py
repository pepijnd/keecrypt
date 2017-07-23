import hashlib
import hmac
from io import BytesIO


def sha256(s):
    return hashlib.sha256(s).digest()


def sha512(s):
    return hashlib.sha512(s).digest()


def hmac_sha256(k, v):
    return hmac.new(k, v, hashlib.sha256).digest()


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
