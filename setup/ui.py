import os

try:
    from PyQt5 import uic
    from PyQt5.pyrcc import RCCResourceLibrary
except ImportError:
    uic = None
    RCCResourceLibrary = None
    NO_PYQT5 = True
else:
    NO_PYQT5 = False


def build_rcc(src_dir, output_path):
    for base, _sub_dirs, files in os.walk(src_dir):
        for file in files:
            if os.path.splitext(file)[1] == '.qrc':
                library = RCCResourceLibrary()
                library.setInputFiles([os.path.join(base, file)])
                library.setResourceRoot('')
                if library.readFiles():
                    output_name = os.path.splitext(file)[0] + '_rc.py'
                    output_path = os.path.join(output_path, 'resources', output_name)
                    print('building', os.path.join(base, file), '->', output_path)
                    library.output(output_path)


def build_ui(src_dir, output_path):
    for base, _sub_dirs, files in os.walk(src_dir):
        for file in files:
            if os.path.splitext(file)[1] == '.ui':
                module = os.path.relpath(base, src_dir)
                ui_name = os.path.join(base, file)
                py_name = os.path.join(output_path, 'ui', module,
                                       os.path.splitext(file)[0] + '_ui.py')

                print('building', ui_name, '->', py_name)
                with open(ui_name, 'r') as ui_file:
                    with open(py_name, 'w') as py_file:
                        uic.compileUi(ui_file, py_file,
                                      from_imports=True,
                                      import_from='keecrypt.gui.resources')


def clean(root):
    clean_with = ['_rc.py', '_ui.py']
    for base, _sub_dirs, files in os.walk(root):
        for file in files:
            for end in clean_with:
                if file.endswith(end):
                    os.unlink(os.path.join(base, file))
