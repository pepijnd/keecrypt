from Crypto.Cipher import AES, Salsa20

from keecrypt.common import sha256


class Decryptor:

    def __init__(self, payload, key, transform_seed, iv, rounds, master_seed):
        self.payload = payload
        self.key = key
        self.transform_seed = transform_seed
        self.iv = iv
        self.rounds = rounds
        self.master_seed = master_seed

        assert len(self.master_seed) == 32

    def decrypt(self):
        cipher = AES.new(self.transform_seed, AES.MODE_ECB)
        transform_key = self.key
        for n in range(self.rounds):
            transform_key = cipher.encrypt(transform_key)
        transform_key = sha256(transform_key)
        master_key = sha256(self.master_seed + transform_key)
        cipher = AES.new(master_key, AES.MODE_CBC, self.iv)
        return cipher.decrypt(self.payload)





