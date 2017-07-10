import os
from functools import partial

from PyQt5 import uic
from PyQt5.pyrcc import RCCResourceLibrary


def build_rcc(src_dir, output_path):
    for base, sub_dirs, files in os.walk(src_dir):
        for file in files:
            if os.path.splitext(file)[1] == '.qrc':
                library = RCCResourceLibrary()
                library.setInputFiles([os.path.join(base, file)])
                library.setResourceRoot('')
                if library.readFiles():
                    output_name = os.path.splitext(file)[0] + '_rc.py'
                    library.output(os.path.join(output_path, 'resources', output_name))


def build_ui(src_dir, output_path):
    uic.compileUiDir(src_dir,
                     recurse=True,
                     map=partial(map_ui, output_path=output_path),
                     from_imports=True,
                     import_from='..resources')


def map_ui(module_name, ui_file, output_path):
    output_path = os.path.join(output_path, 'ui/')
    ui_file = '_' + os.path.splitext(ui_file)[0] + '_ui.py'
    print(output_path, ui_file)
    return output_path, ui_file


def clean(root):
    clean_with = ['_rc.py', '_ui.py']
    for base, sub_dirs, files in os.walk(root):
        for file in files:
            for end in clean_with:
                if file.endswith(end):
                    os.unlink(os.path.join(base, file))
