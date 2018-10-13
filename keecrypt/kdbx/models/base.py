from xml.etree import ElementTree


class KeePassModelBase:
    @classmethod
    def from_xml_element(cls, element: ElementTree.Element):
        pass

    @classmethod
    def to_xml_element(cls):
        return ElementTree.Element()



