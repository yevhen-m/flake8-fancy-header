import sys

major, minor = sys.version_info[0], sys.version_info[1]
PY_37_OR_GREATER = (major, minor) >= (3, 7)

if PY_37_OR_GREATER:
    from .checker import FancyHeaderChecker
else:
    from .checker import FancyHeaderCheckerBefore37 as FancyHeaderChecker
