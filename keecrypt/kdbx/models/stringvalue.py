from keecrypt.kdbx.models import KeePassModelBase


class StringValue(KeePassModelBase):
    def __init__(self, key, value, protected=False):
        self.key = key
        self.value = value
        self.protected = protected
