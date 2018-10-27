from xml.etree import ElementTree

from keecrypt.kdbx.models import KeePassModelBase, StringValue


class Entry(KeePassModelBase):
    def __init__(self, uuid, strings):
        super().__init__()
        self.uuid = uuid
        self._strings = strings

    def __getitem__(self, item):
        for string in self._strings:
            if string.key == item:
                return string.get_value()
        else:
            raise KeyError(item)

    @classmethod
    def from_xml_element(cls, element: ElementTree.Element):
        uuid = element.findtext('UUID')
        strings = [StringValue.from_xml_element(string) for string in element.findall('String')]

        return cls(uuid, strings)
