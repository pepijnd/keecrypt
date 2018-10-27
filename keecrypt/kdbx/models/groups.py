from xml.etree import ElementTree

from keecrypt.kdbx.models import KeePassModelBase, Entry


class Group(KeePassModelBase):
    def __init__(self, uuid, name, times, groups, entries):
        super().__init__()
        self.uuid = uuid
        self.name = name
        self.times = times
        self.groups = groups
        self.entries = entries

    @classmethod
    def from_xml_element(cls, element: ElementTree.Element):
        uuid = element.findtext('UUID')
        name = element.findtext('Name')
        times = element.find('Times')
        groups = []
        entries = []
        for subgroup in element.iterfind('Group'):
            groups.append(cls.from_xml_element(subgroup))
        for entry in element.iterfind('Entry'):
            entries.append(Entry.from_xml_element(entry))
        return cls(uuid, name, times, groups, entries)
