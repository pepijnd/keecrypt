from xml.etree import ElementTree

from keecrypt.kdbx.models import KeePassModelBase, Group


class KeepassFile(KeePassModelBase):
    def __init__(self, meta, root):
        super().__init__()
        self.meta = meta
        self._root = root

    @property
    def groups(self):
        return self._root.groups

    @classmethod
    def from_xml_element(cls, element: ElementTree.Element):
        meta = Meta.from_xml_element(element.find('Meta'))
        root = Root.from_xml_element(element.find('Root'))
        return cls(meta, root)


class Meta(KeePassModelBase):
    def __init__(self):
        super().__init__()


class Root(KeePassModelBase):
    def __init__(self, groups):
        super().__init__()
        self.groups = groups

    @classmethod
    def from_xml_element(cls, element: ElementTree.Element):
        groups = [Group.from_xml_element(group) for group in element.findall('Group')]
        return cls(groups)
