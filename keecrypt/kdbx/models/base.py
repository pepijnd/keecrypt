from xml.etree import ElementTree

from keecrypt.kdbx.models.notify import Message, MessageType, Observer


class KeePassModelBase:
    def __init__(self, parent, root):
        self.parent = parent
        self.root = root
        self.observers = []

    def notify(self, *args, **kwargs):
        for item in self.observers:
            item.notify(self, *args, **kwargs)
        if self.parent is not None:
            self.parent.notify(*args, **kwargs)

    def on_update(self, func):
        item = Observer(func, self.observers)
        self.observers.append(item)
        return item

    @classmethod
    def from_xml_element(cls, element: ElementTree.Element, parent, root):
        return cls(parent, root)

    def to_xml_element(self):
        pass


class StringValue(KeePassModelBase):
    def __init__(self, key, value, protected, parent, root):
        super().__init__(parent, root)
        self.key = key
        self.value = value
        self.protected = protected

    def get_value(self):
        return self.value

    def set_value(self, value):
        old_value = self.value
        self.value = value
        self.notify(Message(MessageType.UPDATE,
                            object=self,
                            key=self.key,
                            value=value,
                            old_value=old_value))

    @classmethod
    def from_xml_element(cls, element: ElementTree.Element, parent, root):
        key = element.findtext('Key')
        value = element.findtext('Value')
        v = element.find('Value')
        protected = False if 'Protected' not in v.attrib else v.attrib['Protected'] is True
        return cls(key, value, protected, parent, root)
