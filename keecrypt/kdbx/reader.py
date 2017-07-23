from io import BytesIO

from xml.etree import ElementTree

from keecrypt.kdbx.parser import KDBXParser


class KDBXReader:
    def __init__(self, filename=None, fileobj=None):
        if filename:
            with open(filename, 'rb') as f:
                self.input_buffer = BytesIO(f.read())
        elif fileobj:
            self.input_buffer = BytesIO(fileobj.read())

        self.parser = KDBXParser(self.input_buffer)
        self.file_data = None

    def decrypt(self, password):
        self.file_data = self.parser.decrypt(password)
        root = ElementTree.fromstring(self.file_data)  # type: ElementTree.Element
        # print(self.blocks[0].decode('utf-8'))
        for group in root.findall('Root/Group'):
            self.parse_group(group)

    @staticmethod
    def parse_group(group):
        __class__.print_group(group)
        for innergroup in group.findall('Group'):
            __class__.parse_group(innergroup)

    @staticmethod
    def print_group(group):
        print('Group: ', group.find('Name').text)
        for entry in group.findall('Entry'):
            print('Entry: ', entry.find('String[Key=\'Title\']/Value').text)

