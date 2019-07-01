class KDBXException(Exception):
    pass


class KDBXInvalidMasterKey(KDBXException):
    pass


class KDBXBlockIntegrityError(KDBXException):
    pass


class KDBXUnsupportedError(KDBXException):
    pass
