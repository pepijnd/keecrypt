import hashlib

from Crypto.Cipher import AES

from keecrypt.common import sha256
from keecrypt.exception import KDBXException


class Key:
    def __init__(self):
        self.hash = b''

    def hash_key(self, key):
        self.hash = sha256(key)
        return key


class PasswordKey(Key):
    def __init__(self, password):
        super().__init__()
        if isinstance(password, str):
            password = password.encode('utf-8')
        self.hash_key(password)


class CompositeKey:
    def __init__(self):
        self.hash = hashlib.sha256()

    def add_key(self, key):
        self.hash.update(key.hash)

    def get_key(self):
        return self.hash.digest()

    def transform(self, transform_seed, master_seed, rounds):
        if len(master_seed) != 32:
            raise KDBXException('invalid master seed size')
        cipher = AES.new(transform_seed, AES.MODE_ECB)
        transform_key = self.get_key()
        for n in range(rounds):
            transform_key = cipher.encrypt(transform_key)
        transform_key = sha256(transform_key)
        master_key = sha256(master_seed + transform_key)
        return master_key
