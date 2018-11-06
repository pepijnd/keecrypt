from xml.etree import ElementTree


class KeePassModelBase:
    def __init__(self, parent, root):
        self.parent = parent
        self.root = root
        self.connected = dict()
        self.conn_count = 0

    def notify(self, msg=None):
        for to_inform in self.connected:
            to_inform(self, msg)
        self.parent.notify(msg)

    def on_update(self, func):
        index = self.root.conn_count
        self.connected.update((index, func))
        self.root.conn_count += 1
        return index

    @classmethod
    def from_xml_element(cls, element: ElementTree.Element, parent, root):
        return cls(parent, root)

    def to_xml_element(self):
        return ElementTree.Element()


class StringValue(KeePassModelBase):
    def __init__(self, key, value, protected, parent, root):
        super().__init__(parent, root)
        self.key = key
        self.value = value
        self.protected = protected

    def get_value(self):
        return self.value

    @classmethod
    def from_xml_element(cls, element: ElementTree.Element, parent, root):
        key = element.findtext('Key')
        value = element.findtext('Value')
        v = element.find('Value')
        protected = False if 'Protected' not in v.attrib else v.attrib['Protected'] is True
        return cls(key, value, protected, parent, root)




