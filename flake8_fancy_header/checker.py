__version__ = '0.1.0'


import ast
import os.path
import sys


class BaseChecker(object):
    name = 'flake8-fancy-header'
    version = __version__

    message_missing = 'S011 Fancy header. Missing.'
    message_invalid = 'S012 Fancy header. Invalid.'

    def __init__(self, tree, filename):
        self.tree = tree
        self.filename = filename

    def get_header_value(self):
        import_path = os.path.splitext(self.filename)[0].replace('/', '.')
        if import_path.endswith('__init__'):
            import_path = import_path.rsplit('.', 1)[0]
        border = '=' * len(import_path)
        return '\n'.join(('', border, import_path, border, ''))


class FancyHeaderCheckerBefore37(BaseChecker):
    def run(self):
        body = self.tree.body
        if not body:
            yield (
                1, 1, self.message_missing, type(self),
            )
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
        docstring = self.tree.docstring
        if not docstring:
            yield (
                1, 1, self.message_missing, type(self),
            )
            return

        if not docstring.startswith(self.get_header_value()):
            yield (
                1, 1, self.message_invalid, type(self),
            )
