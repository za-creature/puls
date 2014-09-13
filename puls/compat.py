# coding=utf-8
"""Python 2 to 3 compatibility module. It redefines base symbols to their py3k
equivalent (str becomes unicode and so on), and handles the importing of
updated standard library symbols. At some point after we drop support for
python 2, it will be completely removed and all non-global symbols will be
imported directly when needed as their python 3 import variants.

Don't bother linting this module. Just imagine it's called 'compat.py  # noqa'.
"""
from __future__ import absolute_import, unicode_literals, division

import sys

if sys.version_info < (3,):
    # python 2 imports
    from urllib import quote_plus, unquote_plus
    import urlparse
    import __builtin__ as builtins

    # redefine python 2 symbols to their py3k equivalent
    str = unicode
    range = xrange
else:
    # python 3 imports
    from urllib.parse import quote_plus, unquote_plus
    import urllib.parse as urlparse
    import builtins

    # python 3 symbols are already defined, but are not directly importable
    str = str
    range = range
