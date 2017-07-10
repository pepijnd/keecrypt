import os

from distutils.command.build import build
from distutils.command.clean import clean
from distutils.core import Command
from setuptools import setup, find_packages

from setup import ui
import keecrypt

root = os.path.abspath(os.path.dirname(__file__))
packages = find_packages(exclude=[('setup',), ('tests',)])


class BuildUiCommand(Command):
    description = 'compile all ui and resource files to python'
    user_options = [
        ('gui-src=', 's', 'path to gui source files'),
        ('output-path', 'o', 'output path for python files')
    ]

    def initialize_options(self):
        self.gui_src = os.path.join(root, 'gui_src')
        self.output_path = os.path.join(root, 'keecrypt/gui/')

    def finalize_options(self):
        if self.gui_src:
            assert os.path.exists(self.gui_src)
        if self.output_path:
            assert os.path.exists(self.output_path)

    def run(self):
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
        ui.clean(root)


class Build(build):
    def run(self):
        self.run_command('build_qt')
        super().run()


class Clean(clean):
    def run(self):
        self.run_command('clean_qt')
        super().run()


setup(
    name=keecrypt.__author__,
    version=keecrypt.__version__,
    description=keecrypt.__description__,
    author=keecrypt.__author__,
    author_email=keecrypt.__author_email__,
    url=keecrypt.__url__,
    license=keecrypt.__license__,
    packages=packages,
    package_data={'': ['LICENSE']},
    package_dir={'keecrypt': 'keecrypt'},
    cmdclass={
        'build': Build,
        'build_qt': BuildUiCommand,
        'clean': Clean,
        'clean_qt': CleanUiCommand
    }
)
