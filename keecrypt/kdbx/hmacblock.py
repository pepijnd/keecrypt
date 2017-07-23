from io import BytesIO

from construct import Int32ul, Int64ul

from keecrypt.common import sha512, hmac_sha256
from keecrypt.exception import KDBXException


class HmacBlockStream:
    def __init__(self, buffer_data):
        self.buffer = BytesIO(buffer_data)
        self.blocks = self.read_blocks()

    def read_blocks(self):
        blocks = []
        block_id = 0
        while True:
            block_hmac = self.buffer.read(32)
            block_size = Int32ul.parse(self.buffer.read(4))
            if block_size > 0:
                block_data = self.buffer.read(block_size)
            else:
                break
            blocks.append(HmacBlock(block_hmac, block_id,  block_size, block_data))
        return blocks

    def check_hmac(self, hmac_key):
        for block in self.blocks:
            block.check_hmac(hmac_key)


class HmacBlock:
    def __init__(self, block_hmac, block_id, block_size, block_data):
        self.block_hmac = block_hmac
        self.block_id = block_id
        self.block_size = block_size
        self.block_data = block_data

    def check_hmac(self, hmac_key):
        block_hmac_key = sha512(Int64ul.build(self.block_id) + hmac_key)
        block_hmac_digest = hmac_sha256(block_hmac_key,
                                        Int64ul.build(self.block_id) +
                                        Int32ul.build(self.block_size) +
                                        self.block_data)
        if block_hmac_digest != self.block_hmac:
            raise KDBXException('Block {} is invalid'.format(self.block_id))


