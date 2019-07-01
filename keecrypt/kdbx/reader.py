from io import BytesIO
from xml.etree import ElementTree

from construct import Int32ul

from keecrypt.kdbx.parser import KDBXParser
from keecrypt.kdbx.models import KeepassFile


class KDBXReader:
    def __init__(self, file):
        if isinstance(file, str):
            with open(file, 'rb') as f:
                self.input_buffer = BytesIO(f.read())
        else:
            self.input_buffer = BytesIO(file.read())

        self.parser = KDBXParser(self.input_buffer)
        self.file_data = None
        self.file_version = (0, 0)

        self.inner_random_stream_id = b''
        self.inner_random_stream_key = b''

    def decrypt(self, password):
        self.file_data = self.parser.decrypt(password)
        if self.parser.file_version[0] >= 4:
            buffer = BytesIO(self.file_data)
            item_type = None
            attachments = []
            while item_type != b'\x00':
                item_type = buffer.read(1)
                item_size = Int32ul.parse(buffer.read(4))
                item_data = buffer.read(item_size)

                if item_type == b'\x01':
                    self.inner_random_stream_id = item_data
                elif item_type == b'\x02':
                    self.inner_random_stream_key = item_data
                elif item_type == b'\x03':
                    flag = item_data[0]
                    attachment = item_data[1:]
                    attachments.append((flag, attachment))
            self.file_data = buffer.read()
        root = ElementTree.fromstring(self.file_data)

        return KeepassFile.from_xml_element(root)


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
