"""
==================
tests.test_checker
==================
"""

import ast
import unittest

from os.path import dirname
from unittest.mock import patch, Mock

from flake8_fancy_header import FancyHeaderChecker


@patch(
    'flake8_fancy_header.checker.getcwd',
    Mock(return_value='/home/User/Project'),
)
@patch('flake8_fancy_header.checker.exists', Mock(return_value=False))
class CheckerTestCase(unittest.TestCase):

    def test_empty_module(self):
        module = ast.parse('')
        checker = FancyHeaderChecker(tree=module, filename='spam.py')
        self.assertEqual(len(list(checker.run())), 0)

        module = ast.parse('\n\n\n')
        checker = FancyHeaderChecker(tree=module, filename='spam.py')
        self.assertEqual(len(list(checker.run())), 0)

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

    def test_module_with_valid_header_2(self):
        module = ast.parse('''\
"""
====
spam
====

Some more text after the header.
"""
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

    def test_module_with_valid_header_and_leading_comment(self):
        module = ast.parse('''\
# coding: utf8
"""
====
spam
====
"""\
        ''')
        checker = FancyHeaderChecker(tree=module, filename='spam.py')
        self.assertEqual(len(list(checker.run())), 0)

    def test_module_with_valid_header_for_init_module(self):
        module = ast.parse('''\
"""
====
spam
====
"""\
        ''')
        checker = FancyHeaderChecker(tree=module, filename='spam/__init__.py')
        self.assertEqual(len(list(checker.run())), 0)

    def test_module_with_relative_filename(self):
        module = ast.parse('''\
"""
====
spam
====
"""\
        ''')
        checker = FancyHeaderChecker(
            tree=module,
            filename='./spam.py',
        )
        self.assertEqual(len(list(checker.run())), 0)

    def test_checker_with_absolute_filename(self):
        module = ast.parse('''\
"""
====
spam
====
"""\
        ''')
        checker = FancyHeaderChecker(
            tree=module,
            filename='/home/User/Project/spam.py',
        )
        self.assertEqual(len(list(checker.run())), 0)

    def test_checker_with_absolute_filename_and_submodule(self):
        module = ast.parse('''\
"""
============
package.spam
============
"""\
        ''')
        checker = FancyHeaderChecker(
            tree=module,
            filename='/home/User/Project/package/spam.py',
        )
        self.assertEqual(len(list(checker.run())), 0)


class CheckerTestCase1(unittest.TestCase):

    @patch('flake8_fancy_header.checker.exists')
    @patch('flake8_fancy_header.checker.getcwd')
    def test_checker_not_from_project_root(self, getcwd, exists):
        getcwd.return_value = '/home/User/Project/package/subpackage'
        # Pretend that project root marker was found in /home/User/Project
        exists.side_effect = lambda path: dirname(path) == '/home/User/Project'
        module = ast.parse('''\
"""
=========================
package.subpackage.module
=========================
"""
        ''')
        checker = FancyHeaderChecker(
            tree=module,
            filename='module.py',
        )
        self.assertEqual(len(list(checker.run())), 0)
