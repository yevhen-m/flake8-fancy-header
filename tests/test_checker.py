import ast
import unittest

from flake8_fancy_header import FancyHeaderChecker


class CheckerTestCase(unittest.TestCase):

    def test_empty_module(self):
        module = ast.parse('')
        checker = FancyHeaderChecker(tree=module, filename='spam.py')
        self.assertEqual(len(list(checker.run())), 1)

    def test_module_with_docstring(self):
        module = ast.parse('"Spam module."')
        checker = FancyHeaderChecker(tree=module, filename='spam.py')
        self.assertEqual(len(list(checker.run())), 1)

    def test_module_without_docstring(self):
        module = ast.parse('class C: pass')
        checker = FancyHeaderChecker(tree=module, filename='spam.py')
        self.assertEqual(len(list(checker.run())), 1)

    def test_module_with_invalid_header(self):
        module = ast.parse('''\
"""
===
foo
===
"""\
        ''')
        checker = FancyHeaderChecker(tree=module, filename='spam.py')
        self.assertEqual(len(list(checker.run())), 1)

    def test_module_with_valid_header(self):
        module = ast.parse('''\
"""
====
spam
====
"""\
        ''')
        checker = FancyHeaderChecker(tree=module, filename='spam.py')
        self.assertEqual(len(list(checker.run())), 0)

    def test_valid_header_in_submodule(self):
        module = ast.parse('''\
"""
========
foo.spam
========
"""\
        ''')
        checker = FancyHeaderChecker(tree=module, filename='foo/spam.py')
        self.assertEqual(len(list(checker.run())), 0)
