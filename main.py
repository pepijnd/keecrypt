from tests.utils import get_file
from keecrypt.kdbx.reader import KDBXReader
from keecrypt.gui import mainwindow


def main():
    mainwindow.run()
    with open(get_file('valid_aes_gzip.kdbx'), 'rb') as f:
        KDBXReader(fileobj=f).decrypt('test_file')


if __name__ == '__main__':
    main()
