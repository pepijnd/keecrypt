from xml.etree import ElementTree

from keecrypt.kdbx.models import KeePassModelBase, StringValue, Message, MessageType


class Entry(KeePassModelBase):
    def __init__(self, uuid, strings, parent, root):
        super().__init__(parent, root)
        self.uuid = uuid
        self._strings = strings

    def __getitem__(self, item):
        for string in self._strings:
            if string.key == item:
                return string.get_value()
        else:
            raise KeyError(item)

    def __setitem__(self, key, value):
        for string in self._strings:
            if string.key == key:
                string.set_value(value)
                break
        else:
            raise KeyError(key)

    @classmethod
    def from_xml_element(cls, element: ElementTree.Element, parent, root):
        uuid = element.findtext('UUID')
        elem = cls(uuid, [], parent, root)
        strings = [StringValue.from_xml_element(string, elem, root) for string in element.findall('String')]
        elem._strings = strings
        return elem
