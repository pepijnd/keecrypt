from xml.etree import ElementTree


class KeePassModelBase:
    def __init__(self):
        pass

    @classmethod
    def from_xml_element(cls, element: ElementTree.Element):
        return cls()

    def to_xml_element(self):
        return ElementTree.Element()


class StringValue(KeePassModelBase):
    def __init__(self, key, value, protected=False):
        super().__init__()
        self.key = key
        self.value = value
        self.protected = protected

    def get_value(self):
        return self.value

    @classmethod
    def from_xml_element(cls, element: ElementTree.Element):
        key = element.findtext('Key')
        value = element.findtext('Value')
        v = element.find('Value')
        protected = False if 'Protected' not in v.attrib else v.attrib['Protected'] is True
        return cls(key, value, protected)




