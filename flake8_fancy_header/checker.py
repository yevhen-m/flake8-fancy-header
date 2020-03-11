"""
===========================
flake8_fancy_header.checker
===========================
"""

__version__ = '0.3.0'


import ast

from os import getcwd
from os.path import exists, dirname, join, normpath, splitext

PROJECT_ROOT_MARKERS = [
    '.git',
    'setup.cfg',
    'setup.py',
]


class BaseChecker(object):
    name = 'flake8-fancy-header'
    version = __version__

    message_missing = 'S011 Fancy header. Missing.'
    message_invalid = 'S012 Fancy header. Invalid.'

    def __init__(self, tree, filename):
        self.tree = tree
        self.filename = filename

    def get_project_root_dir(self, current_dir=None):
        if current_dir == '/':
            # Reached fs root, fallback to cwd
            return getcwd()

        if current_dir is None:
            current_dir = getcwd()

        for marker in PROJECT_ROOT_MARKERS:
            if exists(join(current_dir, marker)):
                return current_dir

        return self.get_project_root_dir(current_dir=dirname(current_dir))

    def get_header_value(self):
        filename = (
            normpath(join(getcwd(), self.filename))
            .split(self.get_project_root_dir() + '/', 1)[1]
        )
        import_path = splitext(filename)[0].replace('/', '.')
        if import_path.endswith('__init__'):
            import_path = import_path.rsplit('.', 1)[0]
        border = '=' * len(import_path)
        return '\n'.join(('', border, import_path, border, ''))


class FancyHeaderCheckerBefore37(BaseChecker):
    def run(self):
        body = self.tree.body
        if not body:
            return

        if not isinstance(body[0], ast.Expr):
            yield (
                1, 1, self.message_missing, type(self),
            )
            return

        if not isinstance(body[0].value, ast.Str):
            yield (
                1, 1, self.message_missing, type(self),
            )
            return

        if not body[0].value.s.startswith(self.get_header_value()):
            yield (
                1, 1, self.message_invalid, type(self),
            )


class FancyHeaderChecker(BaseChecker):
    def run(self):
        docstring = ast.get_docstring(self.tree, clean=False)
        if not docstring:
            if not self.tree.body:
                return

            yield (
                1, 1, self.message_missing, type(self),
            )
            return

        if not docstring.startswith(self.get_header_value()):
            yield (
                1, 1, self.message_invalid, type(self),
            )
