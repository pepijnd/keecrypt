import os

from distutils.command.build import build
from distutils.command.clean import clean
from distutils.command.install import install
from distutils.core import Command
from setuptools import setup, find_packages
from setuptools.command.test import test

from setup import ui
import keecrypt

root = os.path.dirname(__file__)
packages = find_packages(exclude=[('setup',), ('tests',)])


class PyTestCommand(test):
    user_options = []

    def __init__(self, dist, **kw):
        super().__init__(dist, **kw)
        self.test_args = None
        self.test_suite = None

    def initialize_options(self):
        super().initialize_options()

    def finalize_options(self):
        super().finalize_options()
        self.test_args = []
        self.test_suite = True

    def run_tests(self):
        return


class BuildUiCommand(Command):
    description = 'compile all ui and resource files to python'
    user_options = [
        ('gui-src=', 's', 'path to gui source files'),
        ('output-path', 'o', 'output path for python files')
    ]

    def initialize_options(self):
        self.gui_src = os.path.join(root, 'gui_src/')
        self.output_path = os.path.join(root, 'keecrypt/gui/')

    def finalize_options(self):
        if self.gui_src:
            assert os.path.exists(self.gui_src)
        if self.output_path:
            assert os.path.exists(self.output_path)

    def run(self):
        if ui.NO_PYQT5:
            raise ImportError("Can't build ui without pyqt5. run pip install pyqt5 to install")
        ui.build_rcc(self.gui_src, self.output_path)
        ui.build_ui(self.gui_src, self.output_path)


class CleanUiCommand(Command):
    description = 'clean compiled ui and resource files'
    user_options = []

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        ui.clean(os.path.join(root, '.'))


class Install(install):
    def run(self):
        self.run_command('build_qt')
        super().run()


class Build(build):
    def run(self):
        self.run_command('build_qt')
        super().run()


class Clean(clean):
    def run(self):
        self.run_command('clean_qt')
        super().run()


requirements = [
    'construct',
    'pycryptodome',
    'PyQt5',
    'argon2-cffi'
]

setup(
    name=keecrypt.__title__,
    version=keecrypt.__version__,
    description=keecrypt.__description__,
    long_description=open('README.md', 'r').read(),
    author=keecrypt.__author__,
    author_email=keecrypt.__author_email__,
    url=keecrypt.__url__,
    license=keecrypt.__license__,
    packages=packages,
    package_data={'': ['LICENSE' 'README.md']},
    package_dir={'keecrypt': 'keecrypt'},
    install_requires=requirements,
    setup_requires=['PyQt5'],
    cmdclass={
        'install': Install,
        'build': Build,
        'build_qt': BuildUiCommand,
        'clean': Clean,
        'clean_qt': CleanUiCommand,
        'test': PyTestCommand
    },
    zip_safe=False
)
