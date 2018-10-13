from keecrypt.kdbx.models import KeePassModelBase


class EntryTimes(KeePassModelBase):
    def __init__(self, **kwargs):
        self.creation_time = kwargs.get('creation_time', None)
        self.last_modification_time = kwargs.get('last_modification_time', None)
        self.last_access_time = kwargs.get('last_access_time', None)
        self.expiry_time = kwargs.get('expiry_time', None)
        self.usage_count = kwargs.get('usage_count', None)
        self.location_changed = kwargs.get('location_changed', None)
