from xml.etree import ElementTree

from keecrypt.kdbx.models import KeePassModelBase, Entry


class Group(KeePassModelBase):
    def __init__(self, uuid, name, times, groups, entries, parent, root):
        super().__init__(parent, root)
        self.uuid = uuid
        self.name = name
        self.times = times
        self.groups = groups
        self.entries = entries

    @classmethod
    def from_xml_element(cls, element: ElementTree.Element, parent, root):
        uuid = element.findtext('UUID')
        name = element.findtext('Name')
        times = element.find('Times')
        elem = cls(uuid, name, times, [], [], parent, root)
        groups = []
        entries = []
        for subgroup in element.iterfind('Group'):
            groups.append(cls.from_xml_element(subgroup, elem, root))
        for entry in element.iterfind('Entry'):
            entries.append(Entry.from_xml_element(entry, elem, root))
        elem.groups = groups
        elem.entries = entries
        return elem
