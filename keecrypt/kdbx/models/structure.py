from xml.etree import ElementTree

from keecrypt.kdbx.models import KeePassModelBase, Group


class KeepassFile(KeePassModelBase):
    def __init__(self, meta, root_group):
        super().__init__(None, self)
        self.meta = meta
        self.root_group = root_group

    @property
    def groups(self):
        return self.root_group.groups

    @classmethod
    def from_xml_element(cls, element: ElementTree.Element, parent=None, root=None):
        elem = cls(None, None)
        meta = Meta.from_xml_element(element.find('Meta'), elem, elem)
        root_group = Root.from_xml_element(element.find('Root'), elem, elem)
        elem.meta = meta
        elem.root_group = root_group
        return elem


class Meta(KeePassModelBase):
    def __init__(self, parent, root):
        super().__init__(parent, root)
        self._ = None


class Root(KeePassModelBase):
    def __init__(self, groups, parent, root):
        super().__init__(parent, root)
        self.groups = groups

    @classmethod
    def from_xml_element(cls, element: ElementTree.Element, parent, root):
        root_group = cls([], parent, root)
        groups = [Group.from_xml_element(group, root_group, root)
                  for group in element.findall('Group')]
        root_group.groups = groups
        return root_group
